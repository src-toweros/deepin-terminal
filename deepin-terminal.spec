%global _terminals gnome-terminal mate-terminal xfce4-terminal lxterminal qterminal qterminal-qt5 terminology yakuake fourterm roxterm lilyterm termit xterm mrxvt

Name:           deepin-terminal
Version:        5.0.4.1
Release:        1
Summary:        Default terminal emulation application for Deepin
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-terminal
Source0:        %{name}_%{version}.orig.tar.xz	

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  vala-devel
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libwnck-3.0)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(vapigen)
BuildRequires:  pkgconfig(vte-2.91)
BuildRequires:  pkgconfig(gnutls)
Requires:       deepin-menu
Requires:       deepin-shortcut-viewer
Requires:       expect
Requires:       xdg-utils
Recommends:     deepin-manual
Recommends:     zssh
Requires:       %{name}-data = %{version}-%{release}

%description
%{summary}.

%package data
Summary:        Data files of Deepin Terminal
BuildArch:      noarch
Requires:       hicolor-icon-theme

%description data
The %{name}-data package provides shared data for Deepin Terminal.

%prep
%setup -q
sed -i '/ssh_login/s|lib|libexec|' lib/utils.vala CMakeLists.txt
sed -i '/stdc++/d' CMakeLists.txt
rm -rf po/es_419/
sed -i '/es_419/d' deepin-terminal.desktop

%build
%cmake -DCMAKE_BUILD_TYPE=Release \
       -DTEST_BUILD=OFF \
       -DUSE_VENDOR_LIB=OFF \
       -DVERSION=%{version} \
       .
%make_build

%install
%make_install

%find_lang %{name}

%preun
if [ $1 -eq 0 ]; then
  %{_sbindir}/alternatives --remove x-terminal-emulator %{_bindir}/%{name}
fi

%post
if [ $1 -ge 1 ]; then
  %{_sbindir}/alternatives --install %{_bindir}/x-terminal-emulator \
    x-terminal-emulator %{_bindir}/%{name} 20
fi

%triggerin -- konsole5 %_terminals
if [ $1 -ge 1 ]; then
  PRI=20
  for i in konsole %{_terminals}; do
    PRI=$((PRI-1))
    test -x %{_bindir}/$i && \
    %{_sbindir}/alternatives --install %{_bindir}/x-terminal-emulator \
      x-terminal-emulator %{_bindir}/$i $PRI &>/dev/null ||:
  done
fi

%triggerpostun -- konsole5 %_terminals
if [ $2 -eq 0 ]; then
  for i in konsole %{_terminals}; do
    test -x %{_bindir}/$i || \
    %{_sbindir}/alternatives --remove x-terminal-emulator %{_bindir}/$i &>/dev/null ||:
  done
fi

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_libexecdir}/%{name}/ssh_login.sh

%files data -f %{name}.lang
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_datadir}/applications/%{name}.desktop

%changelog
* Thu Jul 30 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.0.4.1-1
- Package init
