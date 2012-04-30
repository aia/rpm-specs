%define beanstalkd_user      beanstalkd
%define beanstalkd_group     %{beanstalkd_user}
%define beanstalkd_home      %{_localstatedir}/lib/beanstalkd
%define beanstalkd_logdir    %{_localstatedir}/log/beanstalkd
%define beanstalkd_binlogdir %{beanstalkd_home}/binlog

Name:           beanstalkd
Version:        1.5.22
Release:        1%{?dist}
Summary:        A simple, fast work-queue service

Group:          System Environment/Daemons
License:        GPLv3+
URL:            http://xph.us/software/%{name}/
Source0:        http://xph.us/dist/%{name}/%{name}-%{version}.tar.gz
Source1:        %{name}.init
Source2:        %{name}.sysconfig

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:   libevent-devel

Requires(pre):      shadow-utils
Requires(pre):      %{_sbindir}/groupadd
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(preun):    initscripts
Requires(postun):   initscripts


%description
beanstalkd is a simple, fast work-queue service. Its interface is generic,
but was originally designed for reducing the latency of page views in
high-volume web applications by running most time-consuming tasks
asynchronously.


%prep
%setup -q
if [ ! -e configure ]; then
  echo "Configured"
  #sh autogen.sh
fi


%build
make %{?_smp_mflags}
%{__gzip} doc/%{name}.1


%install
rm -rf $RPM_BUILD_ROOT
#make install-man1 DESTDIR=$RPM_BUILD_ROOT
#make install-exec-am DESTDIR=$RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_mandir}/man1
%{__install} -p -D -m 0755 beanstalkd  %{buildroot}%{_bindir}/%{name}
%{__install} -p -D -m 0644 doc/%{name}.1.gz %{buildroot}%{_mandir}/man1/%{name}.1.gz
#%doc README README-DEVELOPERS README-TESTS COPYING doc/protocol.txt
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -d -m 0755 %{buildroot}%{beanstalkd_home}
%{__install} -d -m 0755 %{buildroot}%{beanstalkd_binlogdir}


%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group %{beanstalkd_group} >/dev/null || groupadd -r %{beanstalkd_group}
getent passwd %{beanstalkd_user} >/dev/null || \
    useradd -r -g %{beanstalkd_user} -d %{beanstalkd_home} -s /sbin/nologin \
    -c "beanstalkd user" %{beanstalkd_user}
exit 0


%post
/sbin/chkconfig --add %{name}

# make the binlog dir after installation, this is so SELinux does not complain
# about the init script creating the binlog directory
# Bug 558310
if [ -d %{beanstalkd_home} ]; then
    %{__install} -d %{beanstalkd_binlogdir} -m 0755 \
        -o %{beanstalkd_user} -g %{beanstalkd_group} \
        %{beanstalkd_binlogdir}
fi


%preun
if [ $1 = 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc README doc/protocol.txt
%{_initrddir}/%{name}
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0750,%{beanstalkd_user},%{beanstalkd_group}) %dir %{beanstalkd_home}
%ghost %attr(0750,%{beanstalkd_user},%{beanstalkd_group}) %dir %{beanstalkd_binlogdir}


%changelog
* Sun Feb 19 2012 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.6-2
- fix user creation bug #795159

* Sat Jun 05 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.6-1
- update to upstream 1.4.6
- fix binlogdir location initialization for bug #55831
- change default binlogdir in sysconfig file

* Sat Oct 17 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.2-1
- update to upstream 1.4.2

* Sun Oct 11 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4-0
- update to upstream 1.4

* Sat Apr 11 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3-1
- update to upstream 1.3

* Tue Feb 17 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.2-1
- update to upstream 1.2
- remove man page source as it was incorporated upstream

* Sat Nov 22 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.1-1
- initial spec creation
