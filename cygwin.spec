%{?cygwin_package_header}

%global snapshot_commit 3bd5b517f3fe46bdff8e70f1e6038bd0853ddc95
%global snapshot_shortcommit %(echo %{snapshot_commit} | cut -c1-8)
%global snapshot_date 20260523

Name:           cygwin
Version:        3.7.0
%if "%{?snapshot_commit}" != ""
Release:        0.%{snapshot_date}.%{snapshot_shortcommit}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        Cygwin cross-compiler runtime

License:        LGPLv3+ and GPLv3+
Group:          Development/Libraries
URL:            https://cygwin.com/
BuildArch:      noarch

# x86 is unsupported since 3.4.0
%undefine cygwin_build_32bit

# downloaded and extracted by .copr/Makefile
%if "%{?snapshot_commit}" != ""
%define git_ref %{snapshot_commit}
%else
%define git_ref cygwin-%{version}
%endif

Source0:        newlib-cygwin-%{git_ref}.tar.bz2

Patch0:         0001-cygwin-Only-compute-BFD_LIBS-if-building-dumper.patch
Patch2:         0003-Cygwin-Use-bool-return-type-for-comparison-operators.patch
Patch3:         0004-Cygwin-Fix-compilation-of-c8rtomb-with-gcc-16.patch
Patch4:         0001-Pass-include-directory-to-winres.patch

# patches with minimal stubs to build aarch64 for bootstrapping
# (don't expect the cygwin DLL this produces to work!)
Patch10:        0001-Workarounds-needed-to-make-Cygwin-build-for-AArch64-.patch
Patch11:        0002-Cygwin-Fix-typo-in-remainderl.S.patch
Patch12:        0003-Workaround-absence-of-AllocConsoleWithOptions-in-w32.patch

BuildRequires:  cygwin32-filesystem >= 7
BuildRequires:  cygwin32-binutils
BuildRequires:  cygwin32-gcc
BuildRequires:  cygwin32-gcc-c++
BuildRequires:  cygwin32-w32api-headers
BuildRequires:  cygwin32-w32api-runtime

BuildRequires:  cygwin64-filesystem >= 7
BuildRequires:  cygwin64-binutils
BuildRequires:  cygwin64-gcc
BuildRequires:  cygwin64-gcc-c++
BuildRequires:  cygwin64-w32api-headers
BuildRequires:  cygwin64-w32api-runtime

BuildRequires:  cygwin-aarch64-filesystem >= 151
BuildRequires:  cygwin-aarch64-binutils
BuildRequires:  cygwin-aarch64-gcc
BuildRequires:  cygwin-aarch64-gcc-c++
BuildRequires:  cygwin-aarch64-w32api-headers
BuildRequires:  cygwin-aarch64-w32api-runtime

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  texinfo

%description
Cygwin cross-compiler runtime, base libraries.

%package -n cygwin32
Summary:    Cygwin i686 cross-compiler runtime
Requires:   cygwin32-w32api-runtime

%description -n cygwin32
Cygwin 32-bit cross-compiler runtime, base libraries.

%package -n cygwin64
Summary:    Cygwin x86_64 cross-compiler runtime
Requires:   cygwin64-w32api-runtime

%description -n cygwin64
Cygwin 64-bit cross-compiler runtime, base libraries.

%package -n cygwin-aarch64
Summary:    Cygwin aarch64 cross-compiler runtime
Requires:   cygwin-aarch64-w32api-runtime

%description -n cygwin-aarch64
Cygwin 64-bit cross-compiler runtime, base libraries.



%prep
%autosetup -n newlib-cygwin -p1
touch winsup/cygwin/tlsoffsets*.h
touch winsup/cygwin/devices.cc
winsup/autogen.sh


%build
export CFLAGS_FOR_TARGET="-Wno-error"

%if 0%{?cygwin_build_32bit} == 1
mkdir -p build_32bit
pushd build_32bit
`pwd`/../configure \
  --prefix=%{cygwin32_prefix} \
  --build=%_build --host=%_host \
  --target=%{cygwin32_target} \
  --without-mingw-progs --disable-cygserver --disable-dumper --disable-utils \
  --disable-doc
popd
%endif

%if 0%{?cygwin_build_64bit} == 1
mkdir -p build_64bit
pushd build_64bit
`pwd`/../configure \
  --prefix=%{cygwin64_prefix} \
  --build=%_build --host=%_host \
  --target=%{cygwin64_target} \
  --without-mingw-progs --disable-cygserver --disable-dumper --disable-utils \
  --disable-doc
popd
%endif

%if 0%{?cygwin_build_aarch64} == 1
mkdir -p build_aarch64
pushd build_aarch64
`pwd`/../configure \
  --prefix=%{cygwin_aarch64_prefix} \
  --build=%_build --host=%_host \
  --target=%{cygwin_aarch64_target} \
  --without-mingw-progs --disable-cygserver --disable-dumper --disable-utils \
  --disable-doc
popd
%endif

%cygwin_make


%install
CYGWIN32_MAKE_ARGS="tooldir=%{cygwin32_prefix}" \
CYGWIN64_MAKE_ARGS="tooldir=%{cygwin64_prefix}" \
CYGWIN_AARCH64_MAKE_ARGS="tooldir=%{cygwin_aarch64_prefix}" \
%cygwin_make_install

# remove files not needed for cross-compiling
rm -fr $RPM_BUILD_ROOT%{cygwin32_prefix}/etc
rm -f  $RPM_BUILD_ROOT%{cygwin32_bindir}/*cygserver-config
rm -f  $RPM_BUILD_ROOT%{cygwin32_bindir}/*.exe
rm -fr $RPM_BUILD_ROOT%{cygwin32_sbindir}
rm -fr $RPM_BUILD_ROOT%{cygwin32_datadir}

rm -fr $RPM_BUILD_ROOT%{cygwin64_prefix}/etc
rm -f  $RPM_BUILD_ROOT%{cygwin64_bindir}/*cygserver-config
rm -f  $RPM_BUILD_ROOT%{cygwin64_bindir}/*.exe
rm -fr $RPM_BUILD_ROOT%{cygwin64_sbindir}
rm -fr $RPM_BUILD_ROOT%{cygwin64_datadir}

rm -fr $RPM_BUILD_ROOT%{cygwin_aarch64_prefix}/etc
rm -f  $RPM_BUILD_ROOT%{cygwin_aarch64_bindir}/*cygserver-config
rm -f  $RPM_BUILD_ROOT%{cygwin_aarch64_bindir}/*.exe
rm -fr $RPM_BUILD_ROOT%{cygwin_aarch64_sbindir}
rm -fr $RPM_BUILD_ROOT%{cygwin_aarch64_datadir}

# these are provided by other packages
rm -fr $RPM_BUILD_ROOT%{cygwin32_includedir}/iconv.h
rm -fr $RPM_BUILD_ROOT%{cygwin32_includedir}/unctrl.h
rm -fr $RPM_BUILD_ROOT%{cygwin32_includedir}/rpc/

rm -fr $RPM_BUILD_ROOT%{cygwin64_includedir}/iconv.h
rm -fr $RPM_BUILD_ROOT%{cygwin64_includedir}/unctrl.h
rm -fr $RPM_BUILD_ROOT%{cygwin64_includedir}/rpc/

rm -fr $RPM_BUILD_ROOT%{cygwin_aarch64_includedir}/iconv.h
rm -fr $RPM_BUILD_ROOT%{cygwin_aarch64_includedir}/unctrl.h
rm -fr $RPM_BUILD_ROOT%{cygwin_aarch64_includedir}/rpc/

%if 0%{?cygwin_build_32bit} == 1
%files -n cygwin32
%doc winsup/COPYING winsup/CYGWIN_LICENSE
%{cygwin32_bindir}/cygwin1.dll
%{cygwin32_includedir}/*
%{cygwin32_libdir}/*
%endif

%if 0%{?cygwin_build_64bit} == 1
%files -n cygwin64
%doc winsup/COPYING winsup/CYGWIN_LICENSE
%{cygwin64_bindir}/cygwin1.dll
%{cygwin64_includedir}/*
%{cygwin64_libdir}/*
%endif

%if 0%{?cygwin_build_aarch64} == 1
%files -n cygwin-aarch64
%doc winsup/COPYING winsup/CYGWIN_LICENSE
%{cygwin_aarch64_bindir}/cygwin1.dll
%{cygwin_aarch64_includedir}/*
%{cygwin_aarch64_libdir}/*
%endif


%changelog
* Mon Jan 10 2022 Yaakov Selkowitz <yselkowi@redhat.com> - 3.3.3-1
- new version

* Thu Aug 26 2021 Yaakov Selkowitz <yselkowi@redhat.com> - 3.2.0-1
- new version

* Wed Apr 01 2020 Yaakov Selkowitz <yselkowi@redhat.com> - 3.1.4-1
- new version

* Mon Mar 11 2019 Yaakov Selkowitz <yselkowi@redhat.com> - 3.0.3-1
- new version

* Thu Dec 20 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 2.11.2-1
- new version

* Fri Jan 26 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 2.10.0-1
- new version

* Tue Dec 05 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 2.9.0-2
- Fix build with GCC 6

* Sun Dec 03 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 2.9.0-1
- new version

* Fri Jun 24 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.5.2-1
- new version

* Wed Mar 30 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.1-2
- Fix build with GCC 5

* Sun Feb 21 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.1-1
- new version

* Mon Aug 10 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 2.2.0-1
- new version

* Fri Jun 19 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 2.0.4-1
- new version

* Tue Mar 3 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 1.7.34-1
- Version bump.

* Fri Nov 28 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1.7.33-1
- Version bump.

* Fri Aug 22 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1.7.32-2
- BR: mingw*-winpthreads-static to fix FTBFS on F21/EPEL7

* Fri Aug 15 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1.7.32-1
- Version bump.

* Fri Jul 25 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1.7.31-1
- Version bump.

* Thu May 22 2014 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.29-1
- Version bump.

* Thu Jan 16 2014 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.27-1
- Version bump.

* Mon Jul 15 2013 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.21-1
- Version bump.

* Fri Jun 28 2013 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.20-1
- Version bump.
- Updated for new Cygwin packaging scheme.

* Sun Oct 21 2012 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.17-1
- Version bump.
- New API: memrchr.

* Wed May 23 2012 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.15-1
- Version bump.

* Tue May 08 2012 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.14-1
- Version bump.

* Sun Feb 26 2012 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.11-1
- Version bump.
- New API: scandirat.

* Sun Feb 05 2012 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.10-1
- Version bump; removed all patches incorporated upstream.
- New headers: error.h, tgmath.h.
- 35 new APIs.

* Sun Aug 21 2011 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.9-3
- Remove <unctrl.h>, which is to be provided by cygwin-ncurses.
- Added _PATH_MAILDIR and _PATH_SHELLS to <paths.h>.
- Added strdupa and strndupa to <string.h>.
- Header fixes for <process.h> and <unistd.h>.

* Thu Apr 28 2011 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.9-2
- Header fixes for <fenv.h> and <sys/sysmacros.h>.

* Tue Mar 29 2011 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.9-1
- Version bump.
- New API: strchrnul.
- New header: <sys/xattr.h>

* Tue Mar 01 2011 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.8-1
- Version bump.
- New APIs: <fenv.h>, C99 complex math functions, POSIX-compliant strerror_r,
  madvise, pthread_yield, program_invocation_name, program_invocation_short_name.

* Wed Feb 16 2011 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.7.7-1
- Initial RPM release, largely based on earlier work from several sources.
