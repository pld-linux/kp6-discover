#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_with	fwupd		# build with fwupd
%define		kdeplasmaver	6.1.1
%define		qtver		5.15.2
%define		kpname		discover
Summary:	discover
Name:		kp6-%{kpname}
Version:	6.1.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	8b7e67b95e142de961cdad5709d3abcc
URL:		http://www.kde.org/
BuildRequires:	AppStream-qt6-devel >= 1.0
BuildRequires:	Qt6Concurrent-devel >= %{qtver}
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6Svg-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6WebView-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	Qt6Xml-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	flatpak-devel >= 1.14.5
%{?with fwupd:BuildRequires:	fwupd-devel >= 1.9.4}
BuildRequires:	kf6-extra-cmake-modules >= 1.4.0
BuildRequires:	kf6-karchive-devel
BuildRequires:	kf6-kconfig-devel
BuildRequires:	kf6-kconfigwidgets-devel
BuildRequires:	kf6-kcoreaddons-devel
BuildRequires:	kf6-kcrash-devel
BuildRequires:	kf6-kdbusaddons-devel
BuildRequires:	kf6-kdeclarative-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kiconthemes-devel
BuildRequires:	kf6-kidletime-devel
BuildRequires:	kf6-kio-devel
BuildRequires:	kf6-kitemmodels-devel
BuildRequires:	kf6-kitemviews-devel
BuildRequires:	kf6-knewstuff-devel
BuildRequires:	kf6-knotifications-devel
BuildRequires:	kf6-ktextwidgets-devel
BuildRequires:	kf6-kwallet-devel
BuildRequires:	kf6-kwidgetsaddons-devel
BuildRequires:	kf6-purpose-devel
BuildRequires:	kf6-solid-devel
BuildRequires:	libmarkdown-devel
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Suggests:	flatpak
Suggests:	fwupd
Obsoletes:	kp5-%{kpname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
discover

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang discover --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f discover.lang
%defattr(644,root,root,755)
%dir %{_libdir}/qt6/plugins/discover
%{?with fwupd:%attr(755,root,root) %{_libdir}/qt6/plugins/discover/fwupd-backend.so}
%{_desktopdir}/org.kde.discover.desktop
%attr(755,root,root) %{_bindir}/plasma-discover
%{_libdir}/plasma-discover
%{_desktopdir}/org.kde.discover.urlhandler.desktop
%{_iconsdir}/hicolor/*x*/apps/plasmadiscover.png
%{_iconsdir}/hicolor/scalable/apps/plasmadiscover.svg*
%dir %{_datadir}/kxmlgui5/plasmadiscover
%{_datadir}/kxmlgui5/plasmadiscover/plasmadiscoverui.rc
%{_datadir}/metainfo/org.kde.discover.appdata.xml
/etc/xdg/autostart/org.kde.discover.notifier.desktop
%attr(755,root,root) %{_libexecdir}/DiscoverNotifier
%{_desktopdir}/org.kde.discover.notifier.desktop
%{_datadir}/knotifications6/discoverabstractnotifier.notifyrc
%{_datadir}/qlogging-categories6/discover.categories
%attr(755,root,root) %{_bindir}/plasma-discover-update
%{_desktopdir}/org.kde.discover.snap.desktop
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_updates.so
%{_desktopdir}/kcm_updates.desktop
%dir %{_libdir}/qt6/plugins/discover-notifier
%{_libdir}/qt6/plugins/discover-notifier/FlatpakNotifier.so
%{_libdir}/qt6/plugins/discover/flatpak-backend.so
%{_libdir}/qt6/plugins/discover/kns-backend.so
%{_desktopdir}/org.kde.discover-flatpak.desktop
%{_iconsdir}/hicolor/scalable/apps/flatpak-discover.svg
%dir %{_datadir}/libdiscover
%dir %{_datadir}/libdiscover/categories
%{_datadir}/libdiscover/categories/flatpak-backend-categories.xml
%{_datadir}/metainfo/org.kde.discover.flatpak.appdata.xml
