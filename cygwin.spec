%{?cygwin_package_header}

Name:           cygwin
Version:        2.11.2
Release:        1%{?dist}
Summary:        Cygwin cross-compiler runtime

License:        LGPLv3+ and GPLv3+
Group:          Development/Libraries
URL:            http://www.cygwin.com/
BuildArch:      noarch

# downloaded and extracted by get-sources.sh
Source0:        newlib-cygwin-%{version}.tar.bz2

BuildRequires:  cygwin32-filesystem >= 7
BuildRequires:  cygwin32-binutils
BuildRequires:  cygwin32-gcc
BuildRequires:  cygwin32-gcc-c++
BuildRequires:  cygwin32-w32api-headers
BuildRequires:  cygwin32-w32api-runtime
BuildRequires:  mingw32-crt
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-headers
BuildRequires:  mingw32-winpthreads-static
BuildRequires:  mingw32-zlib-static

BuildRequires:  cygwin64-filesystem >= 7
BuildRequires:  cygwin64-binutils
BuildRequires:  cygwin64-gcc
BuildRequires:  cygwin64-gcc-c++
BuildRequires:  cygwin64-w32api-headers
BuildRequires:  cygwin64-w32api-runtime
BuildRequires:  mingw64-crt
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-headers
BuildRequires:  mingw64-winpthreads-static
BuildRequires:  mingw64-zlib-static

BuildRequires:  texinfo
BuildRequires:  xmlto-tex
BuildRequires:  dblatex
BuildRequires:  docbook2X

%description
Cygwin cross-compiler runtime, base libraries.

%package -n cygwin32
Summary:    Cygwin32 cross-compiler runtime
Requires:   cygwin32-w32api-runtime

%description -n cygwin32
Cygwin 32-bit cross-compiler runtime, base libraries.

%package -n cygwin64
Summary:    Cygwin64 cross-compiler runtime
Requires:   cygwin64-w32api-runtime

%description -n cygwin64
Cygwin 64-bit cross-compiler runtime, base libraries.


%prep
%setup -q -n newlib-cygwin
touch winsup/cygwin/tlsoffsets*.h
touch winsup/cygwin/devices.cc


%build
mkdir -p build_32bit
pushd build_32bit
`pwd`/../configure \
  --prefix=%{cygwin32_prefix} \
  --build=%_build --host=%_host \
  --target=%{cygwin32_target}
popd

mkdir -p build_64bit
pushd build_64bit
`pwd`/../configure \
  --prefix=%{cygwin64_prefix} \
  --build=%_build --host=%_host \
  --target=%{cygwin64_target}
popd

%cygwin_make %{?_smp_mflags}


%install
CYGWIN32_MAKE_ARGS="tooldir=%{cygwin32_prefix}" \
CYGWIN64_MAKE_ARGS="tooldir=%{cygwin64_prefix}" \
%cygwin_make install DESTDIR=$RPM_BUILD_ROOT

# remove files not needed for cross-compiling
rm -fr $RPM_BUILD_ROOT%{cygwin32_prefix}/etc
rm -f  $RPM_BUILD_ROOT%{cygwin32_bindir}/cyglsa*
rm -f  $RPM_BUILD_ROOT%{cygwin32_bindir}/cygserver-config
rm -f  $RPM_BUILD_ROOT%{cygwin32_bindir}/*.exe
rm -fr $RPM_BUILD_ROOT%{cygwin32_sbindir}
rm -fr $RPM_BUILD_ROOT%{cygwin32_datadir}

rm -fr $RPM_BUILD_ROOT%{cygwin64_prefix}/etc
rm -f  $RPM_BUILD_ROOT%{cygwin64_bindir}/cyglsa*
rm -f  $RPM_BUILD_ROOT%{cygwin64_bindir}/cygserver-config
rm -f  $RPM_BUILD_ROOT%{cygwin64_bindir}/*.exe
rm -fr $RPM_BUILD_ROOT%{cygwin64_sbindir}
rm -fr $RPM_BUILD_ROOT%{cygwin64_datadir}

# these are provided by other packages
rm -fr $RPM_BUILD_ROOT%{cygwin32_includedir}/iconv.h
rm -fr $RPM_BUILD_ROOT%{cygwin32_includedir}/unctrl.h
rm -fr $RPM_BUILD_ROOT%{cygwin32_includedir}/rpc/

rm -fr $RPM_BUILD_ROOT%{cygwin64_includedir}/iconv.h
rm -fr $RPM_BUILD_ROOT%{cygwin64_includedir}/unctrl.h
rm -fr $RPM_BUILD_ROOT%{cygwin64_includedir}/rpc/


%files -n cygwin32
%doc winsup/COPYING winsup/CYGWIN_LICENSE
%{cygwin32_bindir}/cygwin1.dll
%{cygwin32_includedir}/*
%{cygwin32_libdir}/*

%files -n cygwin64
%doc winsup/COPYING winsup/CYGWIN_LICENSE
%{cygwin64_bindir}/cygwin1.dll
%{cygwin64_includedir}/*
%{cygwin64_libdir}/*


%changelog
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
