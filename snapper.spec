%define libname %mklibname snapper
%define devname %mklibname -d snapper

%global snapper_svcs snapper-boot.service snapper-boot.timer snapper-cleanup.service snapper-cleanup.timer snapper-timeline.service snapper-timeline.timer snapperd.service

Summary:	Tool for filesystem snapshot management
Name:		snapper
Version:	0.12.0
Release:	1
License:	GPLv2+
Group:		Archiving/Backup
Url:		https://snapper.io
Source0:  https://github.com/openSUSE/snapper/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext
BuildRequires:  make
BuildRequires:  systemd-rpm-macros
BuildRequires:  xsltproc
BuildRequires:  docbook-xsl

# devels
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(libbtrfsutil)
BuildRequires:  pkgconfig(mount)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig(ext2fs)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(pam)

Requires:       diffutils
Requires:       %{libname} = %{version}-%{release}

%description
Manage filesystem snapshots and allow undo of system modifications

%package -n %{libname}
Summary:        Shared library for %{name}

%description -n %{libname}
This package contains the snapper shared library
for filesystem snapshot management.
Requires:	%{name} = %{version}-%{release}
Requires:       util-linux
Requires:       btrfs-progs

%package -n %{devname}
Summary:        Development files for %{name}
Requires:	%{libname} = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description -n %{devname}
This package contains header files and documentation for developing with snapper.

%prep
%autosetup -p1
# use libexecdir
find -type f -exec sed -i -e "s|/usr/lib/snapper|%{_libexecdir}/%{name}|g" {} ';'

%build
autoreconf -vfi
%configure \
           --enable-ext4 \
           --enable-zypp
%make_build

%install
%make_install

rm -rf %{buildroot}%{_sysconfdir}/cron.hourly
rm -rf %{buildroot}%{_sysconfdir}/cron.daily

%post
%systemd_post %{snapper_svcs}
 
%preun
%systemd_preun %{snapper_svcs}
 
%postun
%systemd_postun_with_restart %{snapper_svcs}

#{find_lang} snapper

%files
%doc %{_datadir}/doc/snapper/AUTHORS
%doc %{_datadir}/doc/snapper/COPYING
%{_bindir}/mksubvolume
%{_bindir}/snapper
%{_bindir}/snapperd
%{_sysconfdir}/logrotate.d/snapper
%{_libexecdir}/%{name}/installation-helper
%{_libexecdir}/%{name}/systemd-helper
%{_datadir}/bash-completion/completions/snapper
%{_datadir}/dbus-1/system-services/org.opensuse.Snapper.service
%{_datadir}/dbus-1/system.d/org.opensuse.Snapper.conf
%{_datadir}/snapper/config-templates/default
%{_datadir}/snapper/filters/base.txt
%{_datadir}/snapper/filters/lvm.txt
%{_datadir}/snapper/filters/x11.txt
%{_datadir}/snapper/zypp-plugin.conf
%{_datadir}/zsh/site-functions/_snapper
%{_prefix}/lib/systemd/system/snapper-backup.service
%{_prefix}/lib/systemd/system/snapper-backup.timer
%{_prefix}/lib/systemd/system/snapper-boot.service
%{_prefix}/lib/systemd/system/snapper-boot.timer
%{_prefix}/lib/systemd/system/snapper-cleanup.service
%{_prefix}/lib/systemd/system/snapper-cleanup.timer
%{_prefix}/lib/systemd/system/snapper-timeline.service
%{_prefix}/lib/systemd/system/snapper-timeline.timer
%{_prefix}/lib/systemd/system/snapperd.service
%{_prefix}/lib/pam_snapper/
%{_prefix}/lib/zypp/plugins/commit/snapper-zypp-plugin
%{_mandir}/man5/snapper-backup-configs.5.*
%{_mandir}/man5/snapper-configs.5.*
%{_mandir}/man5/snapper-zypp-plugin.conf.5.*
%{_mandir}/man8/mksubvolume.8.*
%{_mandir}/man8/pam_snapper.8.*
%{_mandir}/man8/snapper-zypp-plugin.8.*
%{_mandir}/man8/snapper.8.*
%{_mandir}/man8/snapperd.8.*
%{_mandir}/man8/snbk.8.*
# Locales here bc my mind fog...
%{_datadir}/locale/*/LC_MESSAGES/snapper.mo

%files -n %{libname}
%{_libdir}/libsnapper.so.*
%{_libdir}/security/pam_snapper.so

%files -n %{devname}
%{_libdir}/libsnapper.so
%{_libdir}/snapper/testsuite/
%{_includedir}/%{name}/
