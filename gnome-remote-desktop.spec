Summary:	GNOME Remote Desktop daemon
Summary(pl.UTF-8):	Demon zdalnego pulpitu GNOME (GNOME Remote Desktop)
Name:		gnome-remote-desktop
Version:	46.2
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	https://download.gnome.org/sources/gnome-remote-desktop/46/%{name}-%{version}.tar.xz
# Source0-md5:	7929e817f68064c1ca51542930fe26bb
URL:		https://wiki.gnome.org/Projects/Mutter/RemoteDesktop
BuildRequires:	cairo-devel
BuildRequires:	fdk-aac-devel
BuildRequires:	freerdp3-devel >= 3.1.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.75.0
BuildRequires:	libdrm-devel
BuildRequires:	libei-devel >= 1.2.0
BuildRequires:	libepoxy-devel >= 1.4
BuildRequires:	libfuse3-devel >= 3.9.1
BuildRequires:	libnotify-devel
BuildRequires:	libsecret-devel
BuildRequires:	libvncserver-devel
BuildRequires:	meson >= 0.58.0
BuildRequires:	ninja >= 1.5
BuildRequires:	nv-codec-headers >= 11.1.5.0
BuildRequires:	opus-devel
BuildRequires:	pipewire-devel >= 0.3.49
BuildRequires:	polkit-devel >= 122
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	systemd-units
BuildRequires:	tar >= 1:1.22
# tss2-{esys,mu,rc,tctildr}
BuildRequires:	tpm2-tss-devel
BuildRequires:	xorg-lib-libxkbcommon-devel >= 1.0.0
BuildRequires:	xz
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	freerdp3-libs >= 3.1.0
Requires:	glib2 >= 1:2.75.0
Requires:	libei >= 1.2.0
Requires:	libepoxy >= 1.4
Requires:	libfuse3 >= 3.9.1
Requires:	pipewire >= 0.3.49
Requires:	xorg-lib-libxkbcommon >= 1.0.0
Provides:	group(gnome-remote-desktop)
Provides:	user(gnome-remote-desktop)
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

install -d $RPM_BUILD_ROOT/var/lib/gnome-remote-desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 349 gnome-remote-desktop
%useradd -u 349 -d /var/lib/gnome-remote-desktop -s /bin/false -c "GNOME Remote Desktop" -g gnome-remote-desktop gnome-remote-desktop

%post
%glib_compile_schemas

%postun
%glib_compile_schemas
if [ "$1" = "0" ]; then
	%userremove gnome-remote-desktop
	%groupremove gnome-remote-desktop
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/grdctl
%attr(755,root,root) %{_libexecdir}/gnome-remote-desktop-daemon
%attr(755,root,root) %{_libexecdir}/gnome-remote-desktop-enable-service
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.remote-desktop.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.remote-desktop.gschema.xml
%{_datadir}/gnome-remote-desktop
%{_datadir}/dbus-1/system-services/org.gnome.RemoteDesktop.service
%{_datadir}/dbus-1/system.d/org.gnome.RemoteDesktop.conf
%{_datadir}/polkit-1/actions/org.gnome.remotedesktop.configure-system-daemon.policy
%{_datadir}/polkit-1/actions/org.gnome.remotedesktop.enable-system-daemon.policy
%{_datadir}/polkit-1/rules.d/20-gnome-remote-desktop.rules
%{_desktopdir}/org.gnome.RemoteDesktop.Handover.desktop
%{systemdunitdir}/gnome-remote-desktop.service
%{systemduserunitdir}/gnome-remote-desktop-handover.service
%{systemduserunitdir}/gnome-remote-desktop-headless.service
%{systemduserunitdir}/gnome-remote-desktop.service
%{systemdtmpfilesdir}/gnome-remote-desktop-tmpfiles.conf
/usr/lib/sysusers.d/gnome-remote-desktop-sysusers.conf
%attr(700,gnome-remote-desktop,gnome-remote-desktop) %dir /var/lib/gnome-remote-desktop
%{_mandir}/man1/grdctl.1*
