Summary:	GNOME Remote Desktop daemon
Summary(pl.UTF-8):	Demon zdalnego pulpitu GNOME (GNOME Remote Desktop)
Name:		gnome-remote-desktop
Version:	40.0
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	https://download.gnome.org/sources/gnome-remote-desktop/40/%{name}-%{version}.tar.xz
# Source0-md5:	1c269b3b0f30116f27cce0ca63af9eb0
URL:		https://wiki.gnome.org/Projects/Mutter/RemoteDesktop
BuildRequires:	cairo-devel
BuildRequires:	freerdp2-devel >= 2.3.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.26
BuildRequires:	libfuse3-devel >= 3.9.1
BuildRequires:	libnotify-devel
BuildRequires:	libsecret-devel
BuildRequires:	libvncserver-devel
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pipewire-devel >= 0.3.0
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libxkbcommon-devel >= 1.0.0
BuildRequires:	xz
Requires:	freerdp2-libs >= 2.3.0
Requires:	glib2 >= 1:2.26
Requires:	xorg-lib-libxkbcommon >= 1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Remote desktop daemon for GNOME using pipewire.

%description -l pl.UTF-8
Demon zdalnego pulpitu GNOME, wykorzystujący pipewire.

%prep
%setup -q

%build
%meson build \
	-Dsystemd_user_unit_dir=%{systemduserunitdir}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libexecdir}/gnome-remote-desktop-daemon
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.remote-desktop.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.remote-desktop.gschema.xml
%{systemduserunitdir}/gnome-remote-desktop.service
