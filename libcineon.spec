#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

%define	subver	svn13
Summary:	Cineon Image Format reader/writer library
Summary(pl.UTF-8):	Biblioteka do odczytu/zapisu obrazów w formacie Cineon
Name:		libcineon
Version:	0.1
Release:	2
License:	BSD
Group:		Libraries
# svn checkout http://libcineon.googlecode.com/svn/trunk/ libcineon
Source0:	%{name}-%{subver}.tar.xz
# Source0-md5:	b2956588f890e86a89a8ce26facac956
Patch0:		%{name}-shared.patch
Patch1:		%{name}-missing.patch
URL:		https://github.com/inequation/libcineon
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cineon image format reader/writer library written in portable C++,
forked off of OpenDPX (<http://dpx.googlecode.com/>).

%description -l pl.UTF-8
Biblioteka do odczytu/zapisu obrazów w formacie Cineon. Jest napisana
w przenośnym C++, pierwotny kod wywodzi się z projektu OpenDPX
(<http://dpx.googlecode.com/>).

%package devel
Summary:	Header files for Cineon library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Cineon
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Cineon library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Cineon.

%package static
Summary:	Static Cineon library
Summary(pl.UTF-8):	Statyczna biblioteka Cineon
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Cineon library.

%description static -l pl.UTF-8
Statyczna biblioteka Cineon.

%package apidocs
Summary:	Cineon API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Cineon
Group:		Documentation
BuildArch:	noarch

%description apidocs
API and internal documentation for Cineon library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Cineon.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-shared
%{__make}

%if %{with apidocs}
cd doc
doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_bindir}/cineon2tiff
%attr(755,root,root) %{_bindir}/cineonheader
%attr(755,root,root) %{_libdir}/libcineon.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcineon.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcineon.so
%{_libdir}/libcineon.la
%{_includedir}/Cineon*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libcineon.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*.{css,html,js,png}
%endif
