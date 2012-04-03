%define debug_package %{nil}

Name:           logstash
Version:        1.1.0.1
Release:        7%{?dist}
Summary:        logstash is a tool for managing events and logs.

Group:          System Environment/Daemons
License:        Apache 2.0
URL:            http://logstash.net
Source0:        http://semicomplete.com/files/logstash/%{name}-%{version}-monolithic.jar
Source1:	logstash-wrapper.tar.gz
#Source1:        etc-rc.d-init.d-logstash
Source2:        etc-logstash-logstash.conf
Source3:        etc-logstash-log4j.properties
Source4:        usr-sbin-logstash

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      x86_64

Requires:       jdk
Requires:       grok
# Requires:       java

Requires:       chkconfig initscripts

# disable jar repackaging
%define __os_install_post %{nil}

%description
logstash is a tool for managing events and logs. You can use it to collect logs, parse them, and store them for later use (like, for searching).

%prep
cp -p %SOURCE0 %SOURCE1 %SOURCE2 %SOURCE3 %SOURCE4 .
find . -type f -print0 | xargs -0 --no-run-if-empty -- sed -i -e 's/@@@version@@@/%{version}/g'
%{__tar} xvfz %SOURCE1

%install
rm -rf "${RPM_BUILD_ROOT}"
mkdir -p "${RPM_BUILD_ROOT}/%{_datadir}/logstash/"
install -D -m 644 -t "${RPM_BUILD_ROOT}/%{_datadir}/logstash/" *.jar
#install -D -m 755 etc-rc.d-init.d-logstash          "${RPM_BUILD_ROOT}/etc/rc.d/init.d/logstash"
install -D -m 644 etc-logstash-logstash.conf        "${RPM_BUILD_ROOT}/%{_sysconfdir}/logstash/logstash.conf"
install -D -m 644 etc-logstash-log4j.properties     "${RPM_BUILD_ROOT}/%{_sysconfdir}/logstash/log4j.properties"
install -D -m 644 logstash-wrapper/logstash-wrapper.conf "${RPM_BUILD_ROOT}/%{_sysconfdir}/logstash/logstash-wrapper.conf"
install -D -m 755 usr-sbin-logstash                 "${RPM_BUILD_ROOT}/%{_sbindir}/logstash"
install -D -m 755 logstash-wrapper/logstash-wrapper "${RPM_BUILD_ROOT}/%{_sbindir}/logstash-wrapper"
install -D -m 644 logstash-wrapper/libwrapper.so    "${RPM_BUILD_ROOT}/%{_datadir}/logstash/libwrapper.so"
install -D -m 644 logstash-wrapper/wrapper.jar      "${RPM_BUILD_ROOT}/%{_datadir}/logstash/wrapper.jar"
install -D -m 755 logstash-wrapper/logstash-init    "${RPM_BUILD_ROOT}/%{_datadir}/logstash/logstash-init"
ln -sf %{name}-%{version}-monolithic.jar             ${RPM_BUILD_ROOT}/%{_datadir}/logstash/logstash.jar
mkdir -p "${RPM_BUILD_ROOT}/%{_var}/lib/logstash"
mkdir -p "${RPM_BUILD_ROOT}/%{_var}/log/logstash"
mkdir -p "${RPM_BUILD_ROOT}/%{_var}/run/logstash"

%pre
# create logstash group
if ! getent group logstash >/dev/null; then
  groupadd -r logstash
fi

# create logstash user
if ! getent passwd logstash >/dev/null; then
  #useradd -r -g logstash -d /usr/share/logstash -s /sbin/nologin -c "Logstash User" logstash
  useradd -r -M -g logstash -d /var/lib/logstash -c "Logstash User" logstash
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_sbindir}/logstash
%{_sbindir}/logstash-wrapper
%{_sysconfdir}/logstash
%{_datadir}/logstash
%attr(755, logstash, logstash) %{_var}/lib/logstash
%attr(755, logstash, logstash) %{_var}/log/logstash
%attr(755, logstash, logstash) %{_var}/run/logstash

%changelog

* Mon Apr 2 2012 Artem Veremey <artem@veremey.net> - 1.1.0.1-7
- Added Java Service Wrapper
- Converted references to macrosses 
- Added logstash user
- Cleaned up files

