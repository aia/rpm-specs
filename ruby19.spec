%define rubyver		1.9.3
%define rubyminorver	p125

Name:		ruby19
Version:	%{rubyver}%{rubyminorver}
Release:	5%{?dist}
License:	Ruby License/GPL - see COPYING
URL:		http://www.ruby-lang.org/
Provides:       ruby(abi) = 1.9
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	autoconf automake readline readline-devel ncurses ncurses-devel gdbm gdbm-devel glibc-devel tcl-devel gcc unzip openssl-devel db4-devel byacc make libyaml-devel libffi-devel
Source0:	ftp://ftp.ruby-lang.org/pub/ruby/ruby-%{rubyver}-%{rubyminorver}.tar.gz
Patch0: ruby-1.9.3-p125-gc.patch
Patch1: ruby-1.9.3-p125-debug.patch
Summary:	An interpreter of object-oriented scripting language
Group:		Development/Languages
Provides: ruby(abi) = 1.9
Provides: ruby
Provides: ruby-irb
Provides: ruby-libs
Provides: ruby-rdoc
Provides: ruby-devel
Obsoletes: ruby
Obsoletes: ruby-libs
Obsoletes: ruby-irb
Obsoletes: ruby-rdoc
Obsoletes: ruby-devel

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%package devel
Summary:	A Ruby development environment
Group:		Development/Languages
Provides: ruby-devel
Obsoletes: ruby-devel


%description devel
Header files and libraries for building a extension library for the
Ruby or an application embedded Ruby.

%package doc
Summary:        Ruby documentation
Group:          Development/Languages
Provides: ruby-doc
Obsoletes: ruby-doc

%description doc
Ruby documentation

%prep
%setup -n ruby-%{rubyver}-%{rubyminorver}
%patch0 -p1
%build
export CFLAGS="$RPM_OPT_FLAGS -Wall -fno-strict-aliasing"

%configure \
  --enable-shared \
  --disable-rpath \
  --includedir=%{_includedir}/ruby \
  --libdir=%{_libdir}

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

# installing binaries ...
make install DESTDIR=$RPM_BUILD_ROOT

# we don't want to keep the src directory
rm -rf $RPM_BUILD_ROOT/usr/src

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root)
%{_bindir}
%{_includedir}
%{_libdir}

%files devel
%defattr(-, root, root)
%{_includedir}

%files doc
%defattr(-, root, root)
%{_datadir}

%changelog
* Sat Mar 3 2012 Artem Veremey <artem@veremey.net> - 1.9.3-p125-5
- Update ruby to version 1.9.3-p125
- Include a patche to support profiling
- Move documentation to a separate rpm
- Added libffi-devel autoconf automake deps

* Tue Nov 1 2011 Josh Toft <jtoft@zinio.com> - 1.9.3-p0-1
- Update ruby version to 1.9.3-p0

* Wed Aug 17 2011 Josh Toft <jtoft@zinio.com> - 1.9.2-p290-1
- Update ruby version to 1.9.2-p290

* Sat Jun 25 2011 Ian Meyer <ianmmeyer@gmail.com> - 1.9.2-p180-2
- Remove non-existant --sitearchdir and --vedorarchdir from %configure
- Replace --sitedir --vendordir with simpler --libdir
- Change %{_prefix}/share to %{_datadir}

* Tue Mar 7 2011 Robert Duncan <robert@robduncan.co.uk> - 1.9.2-p180-1
- Update prerequisites to include make
- Update ruby version to 1.9.2-p180
- Install /usr/share documentation
- (Hopefully!?) platform agnostic

* Sun Jan 2 2011 Ian Meyer <ianmmeyer@gmail.com> - 1.9.2-p136-1
- Initial spec to replace system ruby with 1.9.2-p136

