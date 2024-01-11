%?mingw_package_header

%global underscore_version %(echo %{version} | sed 's/\\./_/g')
%global lib_version %(echo %{version} | cut -d \. -f 1)

Name:           mingw-icu
Version:        57.1
Release:        5%{?dist}
Summary:        MinGW compilation of International Components for Unicode Tools

License:        MIT and UCD and Public Domain
URL:            http://icu-project.org
Source0:        http://download.icu-project.org/files/icu4c/%{version}/icu4c-%{underscore_version}-src.tgz

# Patch to fix the build from
# https://build.opensuse.org/package/show/windows:mingw:win32/mingw32-icu
Patch0:         icu4c-56_1-crossbuild.patch

BuildArch:      noarch
ExclusiveArch: %{ix86} x86_64

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-binutils

%description
ICU is a set of C and C++ libraries that provides robust and
full-featured Unicode and locale support. The library provides calendar
support, conversions for many character sets, language sensitive
collation, date and time formatting, support for many locales, message
catalogs and resources, message formatting, normalization, number and
currency formatting, time zone support, transliteration, and word,
line, and sentence breaking, etc.


# Win32
%package -n mingw32-icu
Summary:        MinGW compilation of International Components for Unicode Tools

%description -n mingw32-icu
ICU is a set of C and C++ libraries that provides robust and
full-featured Unicode and locale support. The library provides calendar
support, conversions for many character sets, language sensitive
collation, date and time formatting, support for many locales, message
catalogs and resources, message formatting, normalization, number and
currency formatting, time zone support, transliteration, and word,
line, and sentence breaking, etc.

# Win64
%package -n mingw64-icu
Summary:        MinGW compilation of International Components for Unicode Tools

%description -n mingw64-icu
ICU is a set of C and C++ libraries that provides robust and
full-featured Unicode and locale support. The library provides calendar
support, conversions for many character sets, language sensitive
collation, date and time formatting, support for many locales, message
catalogs and resources, message formatting, normalization, number and
currency formatting, time zone support, transliteration, and word,
line, and sentence breaking, etc.


%?mingw_debug_package


%prep
%setup -q -n icu

%patch0 -p1 -b .crossbuild


%build
pushd source

mkdir -p nativebuild
pushd nativebuild
../configure --enable-static --disable-shared
make %{?_smp_mflags} || make
popd

%mingw_configure \
        --enable-shared --disable-static \
        --with-cross-build=$(pwd)/nativebuild \
        --with-data-packaging=library

%mingw_make %{?_smp_mflags}

popd

%install
pushd source
%mingw_make DESTDIR=$RPM_BUILD_ROOT install
popd

find $RPM_BUILD_ROOT -name "*.dll" -type l -delete

for i in $RPM_BUILD_ROOT%{mingw32_libdir}/*.dll ; \
        do mv $i $RPM_BUILD_ROOT%{mingw32_bindir}/; done
for i in $RPM_BUILD_ROOT%{mingw64_libdir}/*.dll ; \
        do mv $i $RPM_BUILD_ROOT%{mingw64_bindir}/; done

# remove unneded files
rm -fr $RPM_BUILD_ROOT%{mingw32_mandir}
rm -fr $RPM_BUILD_ROOT%{mingw64_mandir}

rm -fr $RPM_BUILD_ROOT%{mingw32_bindir}/icu-config
rm -fr $RPM_BUILD_ROOT%{mingw64_bindir}/icu-config
rm -fr $RPM_BUILD_ROOT%{mingw32_libdir}/icu/Makefile.inc
rm -fr $RPM_BUILD_ROOT%{mingw64_libdir}/icu/Makefile.inc
rm -fr $RPM_BUILD_ROOT%{mingw32_libdir}/icu/pkgdata.inc
rm -fr $RPM_BUILD_ROOT%{mingw64_libdir}/icu/pkgdata.inc


# Win32
%files -n mingw32-icu
%license license.html

%{mingw32_bindir}/genrb.exe
%{mingw32_bindir}/gencnval.exe
%{mingw32_bindir}/uconv.exe
%{mingw32_bindir}/gencmn.exe
%{mingw32_bindir}/makeconv.exe
%{mingw32_bindir}/genbrk.exe
%{mingw32_bindir}/gensprep.exe
%{mingw32_bindir}/pkgdata.exe
%{mingw32_bindir}/icupkg.exe
%{mingw32_bindir}/derb.exe
%{mingw32_bindir}/genccode.exe
%{mingw32_bindir}/gendict.exe
%{mingw32_bindir}/gencfu.exe
%{mingw32_bindir}/gennorm2.exe
%{mingw32_bindir}/icuinfo.exe

%{mingw32_bindir}/icuio%{lib_version}.dll
%{mingw32_bindir}/icuuc%{lib_version}.dll
%{mingw32_bindir}/icule%{lib_version}.dll
%{mingw32_bindir}/icui18n%{lib_version}.dll
%{mingw32_bindir}/icutu%{lib_version}.dll
%{mingw32_bindir}/icudata%{lib_version}.dll
%{mingw32_bindir}/iculx%{lib_version}.dll
%{mingw32_bindir}/icutest%{lib_version}.dll

%{mingw32_libdir}/libicule.dll.a
%{mingw32_libdir}/libicudata.dll.a
%{mingw32_libdir}/libicui18n.dll.a
%{mingw32_libdir}/libicuuc.dll.a
%{mingw32_libdir}/libiculx.dll.a
%{mingw32_libdir}/libicuio.dll.a
%{mingw32_libdir}/libicutest.dll.a
%{mingw32_libdir}/libicutu.dll.a
%{mingw32_libdir}/pkgconfig/icu-i18n.pc
%{mingw32_libdir}/pkgconfig/icu-io.pc
%{mingw32_libdir}/pkgconfig/icu-le.pc
%{mingw32_libdir}/pkgconfig/icu-lx.pc
%{mingw32_libdir}/pkgconfig/icu-uc.pc
%{mingw32_includedir}/layout
%{mingw32_includedir}/unicode
%{mingw32_libdir}/icu
%{mingw32_datadir}/icu

# Win64
%files -n mingw64-icu
%license license.html

%{mingw64_bindir}/genrb.exe
%{mingw64_bindir}/gencnval.exe
%{mingw64_bindir}/uconv.exe
%{mingw64_bindir}/gencmn.exe
%{mingw64_bindir}/makeconv.exe
%{mingw64_bindir}/genbrk.exe
%{mingw64_bindir}/gensprep.exe
%{mingw64_bindir}/pkgdata.exe
%{mingw64_bindir}/icupkg.exe
%{mingw64_bindir}/derb.exe
%{mingw64_bindir}/genccode.exe
%{mingw64_bindir}/gendict.exe
%{mingw64_bindir}/gencfu.exe
%{mingw64_bindir}/gennorm2.exe
%{mingw64_bindir}/icuinfo.exe

%{mingw64_bindir}/icuio%{lib_version}.dll
%{mingw64_bindir}/icuuc%{lib_version}.dll
%{mingw64_bindir}/icule%{lib_version}.dll
%{mingw64_bindir}/icui18n%{lib_version}.dll
%{mingw64_bindir}/icutu%{lib_version}.dll
%{mingw64_bindir}/icudata%{lib_version}.dll
%{mingw64_bindir}/iculx%{lib_version}.dll
%{mingw64_bindir}/icutest%{lib_version}.dll

%{mingw64_libdir}/libicule.dll.a
%{mingw64_libdir}/libicudata.dll.a
%{mingw64_libdir}/libicui18n.dll.a
%{mingw64_libdir}/libicuuc.dll.a
%{mingw64_libdir}/libiculx.dll.a
%{mingw64_libdir}/libicuio.dll.a
%{mingw64_libdir}/libicutest.dll.a
%{mingw64_libdir}/libicutu.dll.a
%{mingw64_libdir}/pkgconfig/icu-i18n.pc
%{mingw64_libdir}/pkgconfig/icu-io.pc
%{mingw64_libdir}/pkgconfig/icu-le.pc
%{mingw64_libdir}/pkgconfig/icu-lx.pc
%{mingw64_libdir}/pkgconfig/icu-uc.pc
%{mingw64_includedir}/layout
%{mingw64_includedir}/unicode
%{mingw64_libdir}/icu
%{mingw64_datadir}/icu


%changelog
* Tue Aug 14 2018 Victor Toso <victortoso@redhat.com> - 57.1-5
- ExclusiveArch: i686, x86_64
- Related: rhbz#1615874

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 57.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 57.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 57.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 24 2016 Kalev Lember <klember@redhat.com> - 57.1-1
- Update to 57.1
- Don't set group tags
- Use license macro

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 50.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 50.1.2-3
- Fix CVE-2013-2924 (RHBZ #1015595)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 16 2013 Paweł Forysiuk <tuxator@o2.pl> - 50.1.2-1
- Update to 50.1.2 to match native version
- Drop icu-config script

* Sun Jan 27 2013 Paweł Forysiuk <tuxator@o2.pl> - 49.1.2-2
- Properly package icudata library

* Sun Dec 30 2012 Pawel Forysiuk <tuxator@o2.pl> - 49.1.2-1
- Update to new upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 18 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.1.1-5
- Added win64 support
- Use mingw macros without leading underscore
- Use %%global instead of %%define

* Mon Feb 27 2012 Kalev Lember <kalevlember@gmail.com> - 4.8.1.1-4
- Added Erik van Pienbroek's patches to fix build with the mingw-w64 toolchain

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.1.1-3
- Rebuild against the mingw-w64 toolchain

* Tue Feb 07 2012 Forysiuk Paweł <tuxator@o2.pl> - 4.8.1.1-2
- Fix icu4c-4_6_1-crossbuild.patch to compile cleanly
- Minor packaging cleanup

* Tue Feb 07 2012 Forysiuk Paweł <tuxator@o2.pl> - 4.8.1.1-1
- Initial release based on openSUSE mingw32-icu package
