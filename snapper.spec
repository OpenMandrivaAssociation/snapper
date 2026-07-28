%define libname %mklibname snapper
%define devname %mklibname -d snapper

%global snapper_svcs snapper-boot.service snapper-boot.timer snapper-cleanup.service snapper-cleanup.timer snapper-timeline.service snapper-timeline.timer snapperd.service

Summary:	Tool for filesystem snapshot management
Name:		snapper
Version:	0.13.1
Release:	3
License:	GPLv2+
Group:	Archiving/Backup
Url:		https://snapper.io
Source0:  https://github.com/openSUSE/snapper/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	docbook-xsl
BuildRequires:	gettext
BuildRequires:  libtool
BuildRequires:	libtool-base
BuildRequires:	make
#BuildRequires:	slibtool
BuildRequires:	systemd-rpm-macros
BuildRequires:	xsltproc
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(libacl)
BuildRequires:	pkgconfig(libbtrfsutil)
BuildRequires:	pkgconfig(libselinux)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(mount)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(pam)
BuildRequires:	pkgconfig(zlib)
Requires:	diffutils
Requires:	logrotate
Requires:	%{libname} = %{version}-%{release}

%description
Manage filesystem snapshots and allow undo of system modifications.

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README.md
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %{_sysconfdir}/%{name}/configs
%{_bindir}/mksubvolume
%{_bindir}/%{name}
%{_bindir}/snapperd
%{_bindir}/snbk
%{_libexecdir}/%{name}/installation-helper
%{_libexecdir}/%{name}/systemd-helper
%{_datadir}/%{name}/config-templates/default
%{_datadir}/%{name}/filters/*.txt
%{_datadir}/%{name}/zypp-plugin.conf
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/bash-completion/completions/snbk
%{_datadir}/dbus-1/system-services/org.opensuse.Snapper.service
%{_datadir}/dbus-1/system.d/org.opensuse.Snapper.conf
%{_datadir}/zsh/site-functions/_%{name}
%{_unitdir}/%{name}-*.service
%{_unitdir}/%{name}-*.timer
%{_unitdir}/snapperd.service
%{_prefix}/lib/pam_%{name}/*.sh
%{_prefix}/lib/zypp/plugins/commit/%{name}-zypp-plugin
%{_mandir}/man5/%{name}-backup-configs.5.*
%{_mandir}/man5/%{name}-configs.5.*
%{_mandir}/man5/%{name}-zypp-plugin.conf.5.*
%{_mandir}/man8/mksubvolume.8.*
%{_mandir}/man8/pam_snapper.8.*
%{_mandir}/man8/%{name}-zypp-plugin.8.*
%{_mandir}/man8/%{name}.8.*
%{_mandir}/man8/snapperd.8.*
%{_mandir}/man8/snbk.8.*


%post
%systemd_post %{snapper_svcs}
 
%preun
%systemd_preun %{snapper_svcs}
 
%postun
%systemd_postun_with_restart %{snapper_svcs}

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary:		Shared library for %{name}
Group:	System/Libraries
# Circular dep
#Requires:	%%{name} = %%{version}-%%{release}
Requires:	util-linux
Requires:	btrfs-progs

%description -n %{libname}
This package contains the snapper shared library for filesystem snapshot
management.

%files -n %{libname}
%{_libdir}/libsnapper.so.*
%{_libdir}/security/pam_snapper.so

#-----------------------------------------------------------------------------

%package -n %{devname}
Summary:		Development files for %{name}
Group:	Development/C++
Requires:	%{libname} = %{version}-%{release}
#Requires:	%%{name} = %%{version}-%%{release}

%description -n %{devname}
This package contains header files and documentation for developing
with snapper.

%files -n %{devname}
%{_libdir}/libsnapper.so
%{_libdir}/snapper/testsuite/
%{_includedir}/%{name}/

#-----------------------------------------------------------------------------

%prep
%autosetup -p1

# use libexecdir
find -type f -exec sed -i -e "s|/usr/lib/snapper|%{_libexecdir}/%{name}|g" {} ';'

# Fix FSF address
sed -i 's/51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA/31 Milk Street, # 960789, Boston, MA 02196, USA/g' COPYING


%build
# Slibtool won't work with snapper
ln -sf %{_bindir}/libtoolize slibtoolize
export PATH=$PWD:$PATH
export LIBTOOLIZE=%{_bindir}/libtoolize
export LIBTOOL=%{_bindir}/libtool
autoreconf -vfi
%configure --enable-selinux

%make_build


%install
%make_install

# Install provided sysconfig file (needed by btrfs assistant GUI)
install -Dpm0644 data/sysconfig.snapper %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Create the needed dir for storing configs
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/configs

# Not interesting stuff
rm -rf %{buildroot}%{_sysconfdir}/cron.hourly
rm -rf %{buildroot}%{_sysconfdir}/cron.daily

# We pick them with our macro
rm -f %{buildroot}%{_docdir}/%{name}/AUTHORS
rm -f %{buildroot}%{_docdir}/%{name}/COPYING


%{find_lang} %{name}
