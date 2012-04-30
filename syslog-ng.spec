%global evtlog_ver 0.2.12

%global _sbindir /sbin
%global _libdir /%{_lib}
%global _default_patch_fuzz	-1

Name: syslog-ng
Version: 3.2.5
Release: 4%{?dist}
Summary: Next-generation syslog server

Group: System Environment/Daemons
License: GPLv2+
Url: http://www.balabit.com/network-security/syslog-ng
Source0: http://www.balabit.com/downloads/files?path=/syslog-ng/sources/%{version}/source/%{name}_%{version}.tar.gz
Source1: syslog-ng.conf
Source2: syslog-ng.init.d
Source3: syslog-ng.sysconfig
Source4: syslog-ng.logrotate

Patch0: syslog-ng-3.2.4-disable-ssl-tests.patch
Patch1: syslog-ng-3.2.5-tests-functional-control.py.patch
Patch2: syslog-ng-3.2.5-tests-functional-sql-test.patch
Patch3: syslog-ng-include-glob.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: pkgconfig
BuildRequires: libtool
BuildRequires: eventlog-devel >= %{evtlog_ver}
BuildRequires: glib2-devel >= 2.10.1
BuildRequires: libdbi-devel
BuildRequires: libnet-devel >= 1.1.4-3
#BuildRequires: openssl-devel
BuildRequires: pcre-devel >= 6.1
BuildRequires: tcp_wrappers-devel

# For the test suite
BuildRequires: python
# For the SQL tests
BuildRequires: libdbi-dbd-sqlite

Requires: logrotate
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service

Provides: syslog
# merge separate syslog-vim package into one
Provides: syslog-ng-vim = %{version}-%{release}
Obsoletes: syslog-ng-vim < 2.0.8-1


%description
syslog-ng, as the name shows, is a syslogd replacement, but with new
functionality for the new generation. The original syslogd allows
messages only to be sorted based on priority/facility pairs; syslog-ng
adds the possibility to filter based on message contents using regular
expressions. The new configuration scheme is intuitive and powerful.
Forwarding logs over TCP and remembering all forwarding hops makes it
ideal for firewalled environments.


%package libdbi
Summary: libdbi support for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description libdbi
This module supports a large number of database systems via libdbi.


%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# fix perl path
%{__sed} -i 's|^#!/usr/local/bin/perl|#!%{__perl}|' contrib/relogger.pl

# fix executable perms on contrib files
%{__chmod} -c a-x contrib/syslog2ng

# fix authors file
/usr/bin/iconv -f iso8859-1 -t utf-8 AUTHORS > AUTHORS.conv && \
    %{__mv} -f AUTHORS.conv AUTHORS


%build
%configure \
    --prefix=/ \
    --libdir=/%{_lib} \
    --includedir=%{_includedir} \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --localstatedir=%{_sharedstatedir}/%{name} \
    --datadir=%{_datadir}/%{name} \
    --with-module-dir=/%{_lib}/%{name} \
    --enable-ipv6 \
    --enable-tcp-wrapper \
    --enable-pcre \
    --enable-spoof-source \
    --enable-sql \
    --disable-ssl \
    --enable-shared \
    --disable-static \
    --enable-dynamic-linking

# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{_smp_mflags}


%install
%{__rm} -rf %{buildroot}
make DESTDIR=%{buildroot} install

#%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
%{__install} -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/syslog-ng.conf

%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/init.d
%{__install} -p -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/init.d/%{name}

%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/syslog-ng

# create the local state dir
%{__install} -d -m 755 %{buildroot}/%{_sharedstatedir}/%{name}

# install the main library header files
%{__install} -d -m 755 %{buildroot}%{_includedir}/%{name}
%{__install} -p -m 644 config.h %{buildroot}%{_includedir}/%{name}
%{__install} -p -m 644 lib/*.h %{buildroot}%{_includedir}/%{name}

# install vim files
%{__install} -d -m 755 %{buildroot}%{_datadir}/%{name}
%{__install} -p -m 644 contrib/syslog-ng.vim %{buildroot}%{_datadir}/%{name}
for vimver in 70 71 72 73 ; do
    %{__install} -d -m 755 %{buildroot}%{_datadir}/vim/vim$vimver/syntax
    cd %{buildroot}%{_datadir}/vim/vim$vimver/syntax
    ln -s ../../../%{name}/syslog-ng.vim .
    cd -
done

find %{buildroot} -name "*.la" -exec rm -f {} \;


%check
LD_LIBRARY_PATH=%{buildroot}/%{_lib}:%{buildroot}/%{_lib}/%{name} make check


%clean
rm -rf %{buildroot}


%post
/sbin/ldconfig
/sbin/chkconfig --add %{name}


%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi


%postun
/sbin/ldconfig
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /sbin/service %{name} condrestart >/dev/null 2>&1
fi


%triggerin -- vim-common
VIMVERNEW=`rpm -q --qf='%%{epoch}:%%{version}\n' vim-common | sort | tail -n 1 | sed -e 's/[0-9]*://' | sed -e 's/\.[0-9]*$//' | sed -e 's/\.//'`
[ -d %{_datadir}/vim/vim${VIMVERNEW}/syntax ] && \
    cd %{_datadir}/vim/vim${VIMVERNEW}/syntax && \
    ln -sf ../../../%{name}/syslog-ng.vim . || :

%triggerun -- vim-common
VIMVEROLD=`rpm -q --qf='%%{epoch}:%%{version}\n' vim-common | sort | head -n 1 | sed -e 's/[0-9]*://' | sed -e 's/\.[0-9]*$//' | sed -e 's/\.//'`
[ $2 = 0 ] && rm -f %{_datadir}/vim/vim${VIMVEROLD}/syntax/syslog-ng.vim || :

%triggerpostun -- vim-common
VIMVEROLD=`rpm -q --qf='%%{epoch}:%%{version}\n' vim-common | sort | head -n 1 | sed -e 's/[0-9]*://' | sed -e 's/\.[0-9]*$//' | sed -e 's/\.//'`
VIMVERNEW=`rpm -q --qf='%%{epoch}:%%{version}\n' vim-common | sort | tail -n 1 | sed -e 's/[0-9]*://' | sed -e 's/\.[0-9]*$//' | sed -e 's/\.//'`
if [ $1 = 1 ]; then
    rm -f %{_datadir}/vim/vim${VIMVEROLD}/syntax/syslog-ng.vim || :
    [ -d %{_datadir}/vim/vim${VIMVERNEW}/syntax ] && \
        cd %{_datadir}/vim/vim${VIMVERNEW}/syntax && \
        ln -sf ../../../%{name}/syslog-ng.vim . || :
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog NEWS
%doc doc/security/*.txt
%doc contrib/{relogger.pl,syslog2ng,syslog-ng.conf.doc}

%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/patterndb.d
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/modules.conf
%config(noreplace) %{_sysconfdir}/%{name}/scl.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/syslog-ng
%{_sysconfdir}/init.d/%{name}
%dir %{_sharedstatedir}/%{name}
%{_sbindir}/%{name}
%{_sbindir}/syslog-ng-ctl
%{_bindir}/loggen
%{_bindir}/pdbtool
%{_bindir}/update-patterndb
%{_libdir}/lib%{name}.so.*
%{_libdir}/%{name}/*.so
%exclude %{_libdir}/%{name}/libafsql.so

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/syslog-ng.vim
%ghost %{_datadir}/vim/

# scl files
%{_datadir}/%{name}/include/

# uhm, some better places for those?
%{_datadir}/%{name}/xsd/

%{_mandir}/man1/loggen.1*
%{_mandir}/man1/pdbtool.1*
%{_mandir}/man1/syslog-ng-ctl.1*
%{_mandir}/man5/syslog-ng.conf.5*
%{_mandir}/man8/syslog-ng.8*


%files libdbi
%defattr(-,root,root,-)
%{_libdir}/%{name}/libafsql.so


%files devel
%defattr(-,root,root,-)
%{_libdir}/libsyslog-ng.so
%{_includedir}/%{name}/


%changelog
* Sun Jan 15 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.2.5-3
- Enabled SQL support (subpackage syslog-ng-libdbi) and the SQL test.

* Wed Dec 14 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.2.5-2
- Ship the same logrotate file as the one shipped in RHEL 6.2 rsyslog package
  (see #767761 and #683537)
- Move the SCL files to the main RPM (#742624 comments >= 28)

* Tue Nov  1 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.2.5-1
- Update to 3.2.5

* Mon Jun 27 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.2.4-2
- Patch syslog-ng-3.2.4-chain-hostnames-processing.patch (#713965)

* Tue May 17 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.2.4-1
- Updated the homepage URL
- Syslog-ng data directory in %%{_datadir}/%%{name}
- Include the main library header files in the devel subpackage

* Fri May 13 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.2.4-0
- Update to 3.2.4
- No need to create the directory /etc/syslog-ng in the install section
- Enable the test suite (but excluding the SQL and SSL tests)

* Mon May  9 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.1.4-3
- Bumped the eventlog version to match the latest upstream version (0.2.12)
- Overrided the default _localstatedir value (configure --localstatedir)
  (value hardcoded in update-patterndb)
- Manually created the patterndb.d configuration directory (update-patterndb)
  (see also https://bugzilla.balabit.com/show_bug.cgi?id=119 comments >= 4)
- Minor modifications of the %%post, %%preun and %%postun scripts
- Corrected a couple of macro references in changelog entries (rpmlint)
- Expanded tabs to spaces (also added a vim modeline)

* Mon Apr 25 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.1.4-2
- cleans the sysconfig and logrotate file mess (#651823 comments 17, 20 and 21)
- add support for vim versions 72 and 73; drop support for 6x
- clean the spoofsource conditional logical: libnet resides in /lib{,64} since
  since 2009

* Wed Apr 13 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.1.4-1
- update for syslog-ng 3.1.4
- updated the source URL
- versioned some of the build requirements
- dropped the libnet patch (syslog-ng-2.1.4-libnet.patch)
- dropped support for EPEL-4 and EPEL-5 (syslog-ng 4.x requires pcre >= 7.3)
- new file: update-patterndb

* Sat Jul 24 2010 Doug Warner <silfreed@fedoraproject.org> - 3.1.1-1
- update for syslog-ng 3.1.1
- supports the new syslog protocol standards
- log statements can be embedded into each other
- the encoding of source files can be set for proper character conversion
- can read, process, and rewrite structured messages (e.g., Apache webserver
  logs) using templates and regular expressions
- support for patterndb v2 and v3 format, along with a bunch of new
  parsers: ANYSTRING, IPv6, IPvANY and FLOAT.
- added a new "pdbtool" utility to manage patterndb files: convert them
  from v1 or v2 format, merge mulitple patterndb files into one and look
  up matching patterns given a specific message.
- support for message tags: tags can be assigned to log messages as they
  enter syslog-ng: either by the source driver or via patterndb.
  Later it these tags can be used for efficient filtering.
- added support for rewriting structured data
- added pcre support in the binary packages of syslog-ng

* Tue Sep 15 2009 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.4-8
- Adjust eventlog build requirement

* Tue Sep 15 2009 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.4-7
- Branch sync

* Tue Sep 15 2009 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.4-6
- Branch sync

* Tue Sep 15 2009 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.4-5
- Rebuilding for tag issue

* Thu Aug 20 2009 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.4-4
- libnet linking (bug#518150)

* Tue Aug 18 2009 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.4-3
- Init script fix (bug#517339)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 24 2009 Douglas E. Warner <silfreed@silfreed.net> - 2.1.4-1
- update to 2.1.4
- enabling mixed linking to compile only non-system libs statically
- lots of packaging updates to be able to build on RHEL4,5, Fedora9+ and be
  parallel-installable with rsyslog and/or sysklogd on those platforms
- removing BR for flex & byacc to try to prevent files from being regenerated
- fixing build error with cfg-lex.l and flex 2.5.4
- Fixed a possible DoS condition triggered by a destination port unreachable
  ICMP packet received from a UDP destination.  syslog-ng started eating all
  available memory and CPU until it crashed if this happened.
- Fixed the rate at which files regular were read using the file() source.
- Report connection breaks as a write error instead of reporting POLLERR as
  the write error path reports more sensible information in the logs.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 02 2008 Douglas E. Warner <silfreed@silfreed.net> 2.0.10-1
- update to 2.0.10
- fix for CVE-2008-5110

* Mon Sep 15 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.8-3
- do not conflicts with rsyslog, both rsyslog and syslog-ng use
  same pidfile and logrotate file (#441664)

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-2
- fix license tag

* Thu Jan 31 2008 Douglas E. Warner <silfreed@silfreed.net> 2.0.8-1
- updated to 2.0.8
- removed logrotate patch

* Tue Jan 29 2008 Douglas E. Warner <silfreed@silfreed.net> 2.0.7-2
- added patch from git commit a8b9878ab38b10d24df7b773c8c580d341b22383
  to fix log rotation (bug#430057)

* Tue Jan 08 2008 Douglas E. Warner <silfreed@silfreed.net> 2.0.7-1
- updated to 2.0.7
- force regeneration to avoid broken paths from upstream (#265221)
- adding loggen binary

* Mon Dec 17 2007 Douglas E. Warner <silfreed@silfreed.net> 2.0.6-1
- updated to 2.0.6
- fixes DoS in ZSA-2007-029

* Thu Nov 29 2007 Peter Vrabec <pvrabec@redhat.com> 2.0.5-3
- add conflicts (#400661)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.0.5-2
- Rebuild for selinux ppc32 issue.

* Thu Jul 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.0.5-1
- Update to 2.0.5

* Thu Jun  7 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.0.4-4
- Add support for vim 7.1.

* Thu May 31 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.0.4-3
- Increase the number of unix-stream max-connections (10 -> 32).

* Sat May 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.0.4-2
- New upstream download location
  (https://lists.balabit.hu/pipermail/syslog-ng/2007-May/010258.html)

* Tue May 22 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.0.4-1
- Update to 2.0.4.

* Mon Mar 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.0.3-1
- Update to 2.0.3.

* Fri Mar 23 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.0.3-0.20070323
- Update to latest snapshot (2007-03-23).

* Fri Mar  9 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.0.3-0.20070309
- Enable support for TCP wrappers (--enable-tcp-wrapper).
- Optional support for spoofed source addresses (--enable-spoof-source)
  (disabled by default; build requires libnet).

* Sun Feb 25 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.0.2-2
- Dynamic link glib2 and eventlog (--enable-dynamic-linking).
  For Fedora Core 6 (and above) both packages install their dynamic
  libraries in /lib.

* Mon Jan 29 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.0.2-1
- Update to 2.0.2.

* Thu Jan  4 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.0.1-1
- Update to 2.0.1.

* Fri Dec 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.0.0-1
- Updated the init script patch: LSB Description and Short-Description.

* Fri Nov  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.0.0-0
- Update to 2.0.0.

* Sun Sep 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.6.11-3
- Rebuild for FC6.

* Sun Jun  4 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.6.11-2
- Install the vim syntax file.

* Fri May  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.6.11-1
- Update to 1.6.11.

* Sun Apr  2 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.6.10-2
- Build option to support the syslog-ng spoof-source feature
  (the feature spoof-source is disabled by default).

* Thu Mar 30 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.6.10-1
- Update to 1.6.10.
- The postscript documentation has been dropped (upstream).

* Wed Feb 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.6.9-3
- Rebuild.

* Mon Dec 19 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.6.9-2
- Provides syslog instead of sysklogd (#172885).

* Wed Nov 30 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.6.9-1
- Build conflict statement
  (see: https://lists.balabit.hu/pipermail/syslog-ng/2005-June/007630.html)

* Wed Nov 23 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.6.9-0
- Update to 1.6.9.
- The libol support library is now included in the syslog-ng tarball.

* Wed Jun 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.6.8-2
- BuildRequire which, since it's not part of the default buildgroup
  (Konstantin Ryabitsev).

* Fri May 27 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.6.8-1
- Update to 1.6.8.

* Thu May 26 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.6.7-3
- Shipping the sysklogd logrotate file and using the same pidfile
  as suggested by Jeremy Katz.
- Patching the init script: no default runlevels.
- Removed the triggers to handle the logrotate file (no longer needed).
- The SELinux use_syslogng boolean has been dropped (rules enabled).

* Sat May 07 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.6.7-2.fc4
- Increased libol required version to 0.3.16
  (https://lists.balabit.hu/pipermail/syslog-ng/2005-May/007385.html).

* Sat Apr 09 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.6.7-0.fdr.1
- Update to 1.6.7.
- The Red Hat/Fedora Core configuration files are now included in the
  syslog-ng tarball (directory: contrib/fedora-packaging).

* Fri Mar 25 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.6.6-0.fdr.4
- Logrotate file conflict: just comment/uncomment contents of the syslog
  logrotate file using triggers.

* Tue Feb 15 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.6.6-0.fdr.3
- Require logrotate.
- Documentation updates (upstream).

* Sat Feb 05 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.6.6-0.fdr.2
- Added contrib/relogger.pl (missing in syslog-ng-1.6.6).
- Requires libol 0.3.15.
- Added %%trigger scripts to handle the logrotate file.

* Fri Feb 04 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.6.6-0.fdr.1
- Update to 1.6.6.
- Patches no longer needed.

* Fri Feb 04 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.6.5-0.fdr.7
- Took ownership of the configuration directory (/etc/syslog-ng/).
- Updated the syslog-ng(8) manpage (upstream patch).
- Updated the configuration file: /proc/kmsg is a file not a pipe.
- Patched two contrib files: syslog2ng and syslog-ng.conf.RedHat.
- Logrotate file inline replacement: perl --> sed (bug 1332 comment 23).

* Tue Jan 25 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.6.5-0.fdr.6
- Logrotate problem: only one logrotate file for syslog and syslog-ng.
- Configuration file: don't sync d_mail destination (/var/log/maillog).

* Mon Jan 24 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.6.5-0.fdr.5
- SIGHUP handling upstream patch (syslog-ng-1.6.5+20050121.tar.gz).
- Static linking /usr libraries (patch already upstream).

* Thu Sep 30 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.6.5-0.fdr.4
- make: do not strip the binaries during installation (install vs install-strip)
  (bug 1332 comment 18).
- install: preserve timestamps (option -p) (bug 1332 comment 18).

* Wed Sep  1 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> 0:1.6.5-0.fdr.3
- use the tcp_wrappers static library instead (bug 1332 comment 15).

* Wed Sep  1 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> 0:1.6.5-0.fdr.2
- added missing build requirement: flex (bug 1332 comment 13).

* Wed Aug 25 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> 0:1.6.5-0.fdr.1
- update to 1.65.
- removed the syslog-ng.doc.patch patch (already upstream).
- removed the syslog-ng.conf.solaris documentation file.

* Wed Apr 21 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> 0:1.6.2-0.fdr.3
- removed Conflits:
- changed the %%post and %%preun scripts
- splitted Requires( ... , ... ) into Requires( ... )

* Fri Mar  5 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> 0:1.6.2-0.fdr.2
- corrected the source URL

* Sat Feb 28 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> 0:1.6.2-0.fdr.1
- changed packaged name to be compliant with fedora.us naming conventions

* Fri Feb 27 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> 0:1.6.2-0.fdr.0.2
- updated to version 1.6.2
- undo "Requires: tcp_wrappers" - tcp_wrappers is a static lib

* Sat Feb  7 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> 0:1.6.1-0.fdr.2
- make %{?_smp_mflags}
- Requires: tcp_wrappers

* Sat Jan 10 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> 0:1.6.1-0.fdr.1
- first release for fedora.us

* Fri Jan  9 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> 1.6.1-1.1tux
- updated to version 1.6.1

* Tue Oct  7 2003 Jose Pedro Oliveira <jpo at di.uminho.pt> 1.6.0rc4-1.1tux
- updated to version 1.6.0rc4

* Tue Aug 26 2003 Jose Pedro Oliveira <jpo at di.uminho.pt> 1.6.0rc3-1.4tux
- installation scripts improved
- conflits line

* Sat Aug 16 2003 Jose Pedro Oliveira <jpo at di.uminho.pt> 1.6.0rc3-1.3tux
- install-strip

* Tue Jul 22 2003 Jose Pedro Oliveira <jpo at di.uminho.pt> 1.6.0rc3-1.2tux
- missing document: contrib/syslog-ng.conf.doc

* Thu Jun 12 2003 Jose Pedro Oliveira <jpo at di.uminho.pt> 1.6.0rc3-1.1tux
- Version 1.6.0rc3

* Sat Apr 12 2003 Jose Pedro Oliveira <jpo at di.uminho.pt> 1.6.0rc2 snapshot
- Reorganized specfile
- Corrected the scripts (%%post, %%postun, and %%preun)
- Commented the mysql related lines; create an option for future inclusion

* Thu Feb 27 2003 Richard E. Perlotto II <richard@perlotto.com> 1.6.0rc1-1
- Updated for new version

* Mon Feb 17 2003 Richard E. Perlotto II <richard@perlotto.com> 1.5.26-1
- Updated for new version

* Sun Dec 20 2002 Richard E. Perlotto II <richard@perlotto.com> 1.5.24-1
- Updated for new version

* Sun Dec 13 2002 Richard E. Perlotto II <richard@perlotto.com> 1.5.23-2
- Corrected the mass of errors that occured with rpmlint
- Continue to clean up for the helpful hints on how to write to a database

* Sun Dec 08 2002 Richard E. Perlotto II <richard@perlotto.com> 1.5.23-1
- Updated file with notes and PGP signatures

# vim:set ai ts=4 sw=4 sts=4 et:
