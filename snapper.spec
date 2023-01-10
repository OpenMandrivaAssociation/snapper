Summary:	Tool for filesystem snapshot management
Name:		snapper
Version:	0.10.4
Release:	1
License:	GPLv2+
Group:		Archiving/Backup
Url:		http://snapper.io
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

Requires:       diffutils

%description
Manage filesystem snapshots and allow undo of system modifications

%prep
%autosetup -p1

 
%build
autoreconf -vfi
%configure
%make_build

%install
%make_install

%files
