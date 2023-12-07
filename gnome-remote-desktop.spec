Summary:	GNOME Remote Desktop daemon
Summary(pl.UTF-8):	Demon zdalnego pulpitu GNOME (GNOME Remote Desktop)
Name:		gnome-remote-desktop
Version:	45.1
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	https://download.gnome.org/sources/gnome-remote-desktop/45/%{name}-%{version}.tar.xz
# Source0-md5:	d48fabf028b7756dcc43bf8a69483411
URL:		https://wiki.gnome.org/Projects/Mutter/RemoteDesktop
BuildRequires:	cairo-devel
BuildRequires:	fdk-aac-devel
BuildRequires:	freerdp2-devel >= 2.10.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.68
BuildRequires:	libdrm-devel
BuildRequires:	libei-devel >= 1.1
BuildRequires:	libepoxy-devel >= 1.4
BuildRequires:	libfuse3-devel >= 3.9.1
BuildRequires:	libnotify-devel
BuildRequires:	libsecret-devel
BuildRequires:	libvncserver-devel
BuildRequires:	meson >= 0.57.0
BuildRequires:	ninja >= 1.5
BuildRequires:	nv-codec-headers >= 11.1.5.0
BuildRequires:	pipewire-devel >= 0.3.49
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	systemd-units
BuildRequires:	tar >= 1:1.22
# tss2-{esys,mu,rc,tctildr}
BuildRequires:	tpm2-tss-devel
BuildRequires:	xorg-lib-libxkbcommon-devel >= 1.0.0
BuildRequires:	xz
Requires:	freerdp2-libs >= 2.10.0
Requires:	glib2 >= 1:2.68
Requires:	libepoxy >= 1.4
Requires:	libfuse3 >= 3.9.1
Requires:	pipewire >= 0.3.49
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
	-Dsystemd_user_unit_dir=%{systemduserunitdir} \
	-Dtests=false \
	-Dvnc=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/grdctl
%attr(755,root,root) %{_libexecdir}/gnome-remote-desktop-daemon
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.remote-desktop.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.remote-desktop.gschema.xml
%{_datadir}/gnome-remote-desktop
%{systemduserunitdir}/gnome-remote-desktop.service
%{_mandir}/man1/grdctl.1*
