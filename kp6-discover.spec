#
# Conditional build:
%bcond_with	tests		# test suite
%bcond_without	fwupd		# fwupd support

%define		kdeplasmaver	6.3.5
%define		qtver		5.15.2
%define		kpname		discover
Summary:	Plasma Discover - KDE Software Center
Summary(pl.UTF-8):	Odkrywca - Ośrodek programów KDE
Name:		kp6-%{kpname}
Version:	6.3.5
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	3951d212cb801598a7355d68c3049583
URL:		https://kde.org/
BuildRequires:	AppStream-qt6-devel >= 1.0
BuildRequires:	PackageKit-qt6-devel
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
%{?with_fwupd:BuildRequires:	fwupd-devel >= 1.9.4}
BuildRequires:	kf6-extra-cmake-modules >= 1.4.0
BuildRequires:	kf6-karchive-devel
BuildRequires:	kf6-kcmutils-devel
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
BuildRequires:	kf6-kirigami-addons-devel
BuildRequires:	kf6-kitemmodels-devel
BuildRequires:	kf6-kitemviews-devel
BuildRequires:	kf6-knewstuff-devel
BuildRequires:	kf6-knotifications-devel
BuildRequires:	kf6-kstatusnotifieritem-devel
BuildRequires:	kf6-ktextwidgets-devel
BuildRequires:	kf6-kwallet-devel
BuildRequires:	kf6-kwidgetsaddons-devel
BuildRequires:	kf6-purpose-devel
BuildRequires:	kf6-solid-devel
BuildRequires:	libmarkdown-devel
BuildRequires:	ninja
BuildRequires:	qcoro-qt6-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Suggests:	flatpak
Suggests:	fwupd
Requires(post,postun):	desktop-file-utils
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Discover helps you find and install applications, games, and tools.
You can search or browse by category, and look at screenshots and read
reviews to help you pick the perfect app.

%description -l pl.UTF-8
Odkrywca pozwala znajdować i instalować aplikacje, gry i narzędzia.
Można wyszukiwać i przeglądać wg kategorii, oglądać zrzuty ekranu i
czytać recenzje, aby wybrać idealną aplikację.

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

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun


%files -f discover.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/plasma-discover
%attr(755,root,root) %{_bindir}/plasma-discover-update
%dir %{_libdir}/plasma-discover
%attr(755,root,root) %{_libdir}/plasma-discover/lib*.so
%dir %{_libdir}/qt6/plugins/discover
%attr(755,root,root) %{_libdir}/qt6/plugins/discover/flatpak-backend.so
%if %{with fwupd}
%attr(755,root,root) %{_libdir}/qt6/plugins/discover/fwupd-backend.so
%endif
%attr(755,root,root) %{_libdir}/qt6/plugins/discover/kns-backend.so
%attr(755,root,root) %{_libdir}/qt6/plugins/discover/packagekit-backend.so
%dir %{_libdir}/qt6/plugins/discover-notifier
%attr(755,root,root) %{_libdir}/qt6/plugins/discover-notifier/DiscoverPackageKitNotifier.so
%attr(755,root,root) %{_libdir}/qt6/plugins/discover-notifier/FlatpakNotifier.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_updates.so
%attr(755,root,root) %{_libexecdir}/DiscoverNotifier
%{_datadir}/knotifications6/discoverabstractnotifier.notifyrc
%{_datadir}/kxmlgui5/plasmadiscover
%dir %{_datadir}/libdiscover
%dir %{_datadir}/libdiscover/categories
%{_datadir}/libdiscover/categories/flatpak-backend-categories.xml
%{_datadir}/libdiscover/categories/packagekit-backend-categories.xml
%{_datadir}/metainfo/org.kde.discover.appdata.xml
%{_datadir}/metainfo/org.kde.discover.flatpak.appdata.xml
%{_datadir}/qlogging-categories6/discover.categories
%{_desktopdir}/kcm_updates.desktop
%{_desktopdir}/org.kde.discover.desktop
%{_desktopdir}/org.kde.discover.notifier.desktop
%{_desktopdir}/org.kde.discover.snap.desktop
%{_desktopdir}/org.kde.discover.urlhandler.desktop
%{_desktopdir}/org.kde.discover-flatpak.desktop
%{_iconsdir}/hicolor/*x*/apps/plasmadiscover.png
%{_iconsdir}/hicolor/scalable/apps/flatpak-discover.svg
%{_iconsdir}/hicolor/scalable/apps/plasmadiscover.svg*
/etc/xdg/autostart/org.kde.discover.notifier.desktop
%{_datadir}/metainfo/org.kde.discover.packagekit.appdata.xml
