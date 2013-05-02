# Copyright (c) 2000-2009, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section         non-free

%define origin          sun
%define priority        1500
%define javaver         1.7.0
%define cvsver          7
%define buildver        21

# TODO: Think about using conditionals for version variants.
%define cvsversion	%{cvsver}u%{buildver}

%define javaws_ver      %{javaver}
%define javaws_version  %{cvsversion}

%define toplevel_dir    jdk%{javaver}_%{buildver}

%define sdklnk          java-%{javaver}-%{origin}
%define jrelnk          jre-%{javaver}-%{origin}
%define sdkdir          %{name}-%{version}
%define jredir          %{sdkdir}/jre
%define sdkbindir       %{_jvmdir}/%{sdklnk}/bin
%define sdklibdir       %{_jvmdir}/%{sdklnk}/lib
%define jrebindir       %{_jvmdir}/%{jrelnk}/bin
%define jvmjardir       %{_jvmjardir}/%{name}-%{version}

%define x11bindir       %{_prefix}/X11R6/bin
%define x11encdir       %{_prefix}/X11R6/lib/X11/fonts/encodings
%define fontconfigdir   %{_sysconfdir}/fonts
%define fontdir         %{_datadir}/fonts/java
%define xsldir          %{_datadir}/xml/%{name}-%{version}

%ifarch %ix86
%define target_cpu      i586
%define pluginname      %{_jvmdir}/%{jredir}/plugin/i386/ns7/libjavaplugin_oji.so
%endif

%ifarch x86_64
%define target_cpu      x64
%define pluginname      %{_jvmdir}/%{jredir}/lib/amd64/libnpjp2.so
%endif

%define cgibindir       %{_var}/www/cgi-bin

# Avoid RPM 4.2+'s internal dep generator, it may produce bogus
# Provides/Requires here.
%define _use_internal_dependency_generator 0

# This prevents aggressive stripping.
%define debug_package %{nil}


Name:           java-%{javaver}-%{origin}
Version:        %{javaver}.%{buildver}
Release:        1.2jpp.im
Epoch:          0
Summary:        Java Runtime Environment for %{name}
License:        Sun Binary Code License
Group:          Development/Interpreters
URL:            http://java.sun.com/j2se/%{javaver}
Source0:        jdk-%{cvsversion}-linux-%{target_cpu}.tar.gz
Source1:        %{name}-register-java-fonts.xsl
Source2:        %{name}-unregister-java-fonts.xsl
NoSource:       0
Provides:       jre-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides:       jre-%{origin} = %{epoch}:%{version}-%{release}
Provides:       jre-%{javaver}, java-%{javaver}, jre = %{epoch}:%{javaver}
Provides:       java-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java = %{epoch}:%{javaver}
Requires:       /usr/sbin/update-alternatives
Requires:       jpackage-utils >= 0:1.5.38
Conflicts:      kaffe
BuildArch:      i586 x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  jpackage-utils >= 0:1.5.38, sed, %{_bindir}/perl
Provides:       javaws = %{epoch}:%{javaws_ver}
Provides:       jndi = %{epoch}:%{version}, jndi-ldap = %{epoch}:%{version}
Provides:       jndi-cos = %{epoch}:%{version}, jndi-rmi = %{epoch}:%{version}
Provides:       jndi-dns = %{epoch}:%{version}
Provides:       jaas = %{epoch}:%{version}
Provides:       jsse = %{epoch}:%{version}
Provides:       jce = %{epoch}:%{version}
Provides:       jdbc-stdext = %{epoch}:3.0, jdbc-stdext = %{epoch}:%{version}
Provides:       java-sasl = %{epoch}:%{version}
Obsoletes:      javaws-menu

%description
This package contains the Java Runtime Environment for %{name}

%package        devel
Summary:        Java Development Kit for %{name}
Group:          Development/Compilers
Requires:       /usr/sbin/update-alternatives
Provides:       java-sdk-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-sdk-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-sdk-%{javaver}, java-sdk = %{epoch}:%{javaver}
Provides:       java-devel-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-%{javaver}-devel, java-devel = %{epoch}:%{javaver}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    devel
The Java(tm) Development Kit (JDK(tm)) contains the software and tools that
developers need to compile, debug, and run applets and applications
written using the Java programming language.

%package        src
Summary:        Source files for %{name}
Group:          Development/Interpreters
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    src
This package contains source files for %{name}.

%package        demo
Summary:        Demonstration files for %{name}
Group:          Development/Interpreters
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    demo
This package contains demonstration files for %{name}.

%package        plugin
Summary:        Browser plugin files for %{name}
Group:          Internet/WWW/Browsers
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       %{_bindir}/find, sed
Provides:       java-plugin = %{epoch}:%{javaver}, java-%{javaver}-plugin = %{epoch}:%{version}
Conflicts:      java-%{javaver}-ibm-plugin, java-%{javaver}-blackdown-plugin
Conflicts:      java-%{javaver}-bea-plugin
Obsoletes:      java-1.3.1-plugin, java-1.4.0-plugin, java-1.4.1-plugin, java-1.4.2-plugin

%description    plugin
This package contains browser plugin files for %{name}.
Note!  This package supports browsers built with GCC 3.2 and later.

%package        fonts
Summary:        TrueType fonts for %{origin} JVMs
Group:          Text Processing/Fonts
Requires:       %{name} = %{epoch}:%{version}-%{release}, %{_bindir}/ttmkfdir
Requires:       xorg-x11-font-utils, mktemp
Requires:       %{_bindir}/xsltproc, %{_bindir}/perl
Provides:       java-fonts = %{epoch}:%{javaver}, java-%{javaver}-fonts
Conflicts:      java-%{javaver}-ibm-fonts, java-%{javaver}-blackdown-fonts
Conflicts:      java-%{javaver}-bea-fonts
Obsoletes:      java-1.3.1-fonts, java-1.4.0-fonts, java-1.4.1-fonts, java-1.4.2-fonts

%description    fonts
This package contains the TrueType fonts for %{origin} JVMs.

%package        alsa
Summary:        ALSA support for %{name}
Group:          Development/Libraries/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    alsa
This package contains Advanced Linux Sound Architecture (ALSA) support
libraries for %{name}.

%package        jdbc
Summary:        JDBC/ODBC bridge driver for %{name}
Group:          Development/Libraries/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       unixODBC

%description    jdbc
This package contains the JDBC/ODBC bridge driver for %{name}.


%prep
%setup -q -n %{toplevel_dir}

%build
# Nope.


%install
rm -rf $RPM_BUILD_ROOT

# fix up ControlPanel APPHOME and bin locations
perl -p -i -e 's|APPHOME=.*|APPHOME=%{_jvmdir}/%{jredir}|' jre/bin/ControlPanel
perl -p -i -e 's|/usr/bin/||g' jre/bin/ControlPanel

# fix up (create new) HtmlConverter
cat > bin/HtmlConverter << EOF
%{jrebindir}/java -jar %{sdklibdir}/htmlconverter.jar $*
EOF

# fix up java-rmi.cgi PATH
perl -p -i -e 's|PATH=.*|PATH=%{jrebindir}|' bin/java-rmi.cgi

%ifnarch x86_64
# install java-rmi-cgi
install -D -m 755 bin/java-rmi.cgi $RPM_BUILD_ROOT%{cgibindir}/java-rmi-%{version}.cgi
%endif

# main files
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
cp -a bin include lib src.zip $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}

# extensions handling
install -d -m 755 $RPM_BUILD_ROOT%{jvmjardir}
pushd $RPM_BUILD_ROOT%{jvmjardir}
   ln -s %{_jvmdir}/%{jredir}/lib/jsse.jar jsse-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/jce.jar jce-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar jndi-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar jndi-ldap-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar jndi-cos-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar jndi-rmi-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar jaas-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar jdbc-stdext-%{version}.jar
   ln -s jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar sasl-%{version}.jar
   for jar in *-%{version}.jar ; do
      if [ x%{version} != x%{javaver} ]; then
         ln -fs ${jar} $(echo $jar | sed "s|-%{version}.jar|-%{javaver}.jar|g")
      fi
      ln -fs ${jar} $(echo $jar | sed "s|-%{version}.jar|.jar|g")
   done
popd

# rest of the jre
cp -a jre/bin jre/lib $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
cp -a jre/plugin $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/endorsed

# jce policy file handling
install -d -m 755 $RPM_BUILD_ROOT%{_jvmprivdir}/%{name}/jce/vanilla
for file in local_policy.jar US_export_policy.jar; do
  mv $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/$file \
    $RPM_BUILD_ROOT%{_jvmprivdir}/%{name}/jce/vanilla
  # for ghosts
  touch $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/$file
done

# versionless symlinks
pushd $RPM_BUILD_ROOT%{_jvmdir}
ln -s %{jredir} %{jrelnk}
ln -s %{sdkdir} %{sdklnk}
popd

pushd $RPM_BUILD_ROOT%{_jvmjardir}
ln -s %{sdkdir} %{jrelnk}
ln -s %{sdkdir} %{sdklnk}
popd

# ControlPanel freedesktop.org menu entry
perl -p -i -e 's|INSTALL_DIR/JRE_NAME_VERSION|%{_jvmdir}/%{jredir}|g' jre/plugin/desktop/sun_java.desktop
perl -p -i -e 's|Name=.*|Name=Java Plugin Control Panel \(%{name}\)|' jre/plugin/desktop/sun_java.desktop
perl -p -i -e 's|Icon=.*|Icon=%{name}.png|' jre/plugin/desktop/sun_java.desktop

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
install -m 644 jre/plugin/desktop/sun_java.desktop  $RPM_BUILD_ROOT%{_datadir}/applications/jpackage-%{name}-control-panel.desktop
install -m 644 jre/plugin/desktop/sun_java.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.png

# javaws freedesktop.org menu entry
cat >> $RPM_BUILD_ROOT%{_datadir}/applications/jpackage-%{name}-javaws.desktop << EOF
[Desktop Entry]
Name=Java Web Start (%{name})
Comment=Java Application Launcher
Exec=%{_jvmdir}/%{jredir}/bin/javaws
Icon=%{name}.png
Terminal=0
Type=Application
Categories=Application;Settings;X-Sun-Supported;X-Red-Hat-Base;
EOF

# man pages
install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
for manpage in man/man1/*; do
  install -m 644 -p $manpage $RPM_BUILD_ROOT%{_mandir}/man1/`basename $manpage .1`-%{name}.1
done

# ghost plugin installation lists
for i in mozilla firefox ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
  touch $RPM_BUILD_ROOT%{_datadir}/%{name}/$i-plugin-dirs
done

### font handling

pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib

   # Remove font.properties and use the system-wide one -- NiM
   rm -f font.properties
   ln -fs %{_sysconfdir}/java/font.properties .

   # remove supplied fonts.dir in preference of the one to be dynamically generated -- Rex
   rm fonts/fonts.dir

   # These %ghost'd files are created properly in %post  -- Rex
   touch fonts/{fonts.{alias,dir,scale,cache-1},XftCache,encodings.dir}

   if [ "%{fontdir}" != "%{jredir}/lib/fonts" ] ; then
      install -d -m 755 $RPM_BUILD_ROOT%{fontdir}
      mv fonts/* $RPM_BUILD_ROOT%{fontdir}
      rmdir fonts
      ln -fs %{fontdir} fonts
   fi

popd

# font registration/unregistration
install -d -m 755 $RPM_BUILD_ROOT%{xsldir}
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{xsldir}/register-java-fonts.xsl
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{xsldir}/unregister-java-fonts.xsl

# Most of this shamelessly stolen from redhat's kdebase-2.2.2 specfile

find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type d \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' >  %{name}-%{version}-all.files
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type f -o -type l \
  | sed 's|'$RPM_BUILD_ROOT'||'      >> %{name}-%{version}-all.files

grep plugin  %{name}-%{version}-all.files | sort \
  > %{name}-%{version}-plugin.files
grep npjp  %{name}-%{version}-all.files | sort \
  >> %{name}-%{version}-plugin.files
grep Jdbc    %{name}-%{version}-all.files | sort \
  > %{name}-%{version}-jdbc.files
grep -F alsa.so %{name}-%{version}-all.files | sort \
  > %{name}-%{version}-alsa.files
cat %{name}-%{version}-all.files \
  | grep -v plugin \
  | grep -v npjp \
  | grep -v Jdbc \
  | grep -v lib/fonts \
  | grep -vF alsa.so \
  | grep -v jre/lib/security \
  > %{name}-%{version}.files


%clean
rm -rf $RPM_BUILD_ROOT


%preun fonts
[ $1 -eq 0 ] || exit 0

 # Unregister self in fontconfig aliases
if [ -w %{fontconfigdir}/fonts.conf ] ; then
   TMPFILE=$(/bin/mktemp -q /tmp/fonts.conf.XXXXXX) && \
   %{_bindir}/xsltproc --novalid %{xsldir}/unregister-java-fonts.xsl \
        %{fontconfigdir}/fonts.conf > $TMPFILE && \
   /bin/cat $TMPFILE > %{fontconfigdir}/fonts.conf && /bin/rm $TMPFILE
fi


%post
ext=
[ -f %{_mandir}/man1/java-%{name}.1.bz2 ] && ext=".bz2"
[ -f %{_mandir}/man1/java-%{name}.1.gz ] && ext=".gz"

update-alternatives --install %{_bindir}/java java %{jrebindir}/java %{priority} \
--slave %{_bindir}/ControlPanel            ControlPanel                %{jrebindir}/ControlPanel \
--slave %{_jvmdir}/jre                     jre                         %{_jvmdir}/%{jrelnk} \
--slave %{_jvmjardir}/jre                  jre_exports                 %{_jvmjardir}/%{jrelnk} \
--slave %{_bindir}/keytool                 keytool                     %{jrebindir}/keytool \
--slave %{_bindir}/orbd                    orbd                        %{jrebindir}/orbd \
--slave %{_bindir}/policytool              policytool                  %{jrebindir}/policytool \
--slave %{_bindir}/rmid                    rmid                        %{jrebindir}/rmid \
--slave %{_bindir}/rmiregistry             rmiregistry                 %{jrebindir}/rmiregistry \
--slave %{_bindir}/servertool              servertool                  %{jrebindir}/servertool \
--slave %{_bindir}/tnameserv               tnameserv                   %{jrebindir}/tnameserv \
--slave %{_bindir}/javaws                  javaws                      %{jrebindir}/javaws \
--slave %{_mandir}/man1/java.1$ext         java.1$ext                  %{_mandir}/man1/java-%{name}.1$ext \
--slave %{_mandir}/man1/keytool.1$ext      keytool.1$ext               %{_mandir}/man1/keytool-%{name}.1$ext \
--slave %{_mandir}/man1/orbd.1$ext         orbd.1$ext                  %{_mandir}/man1/orbd-%{name}.1$ext \
--slave %{_mandir}/man1/policytool.1$ext   policytool.1$ext            %{_mandir}/man1/policytool-%{name}.1$ext \
--slave %{_mandir}/man1/rmid.1$ext         rmid.1$ext                  %{_mandir}/man1/rmid-%{name}.1$ext \
--slave %{_mandir}/man1/rmiregistry.1$ext  rmiregistry.1$ext           %{_mandir}/man1/rmiregistry-%{name}.1$ext \
--slave %{_mandir}/man1/servertool.1$ext   servertool.1$ext            %{_mandir}/man1/servertool-%{name}.1$ext \
--slave %{_mandir}/man1/tnameserv.1$ext    tnameserv.1$ext             %{_mandir}/man1/tnameserv-%{name}.1$ext \
--slave %{_mandir}/man1/javaws.1$ext       javaws.1$ext                %{_mandir}/man1/javaws-%{name}.1$ext \
--slave %{_mandir}/man1/kinit.1$ext        kinit.1$ext                 %{_mandir}/man1/kinit-%{name}.1$ext \
--slave %{_mandir}/man1/klist.1$ext        klist.1$ext                 %{_mandir}/man1/klist-%{name}.1$ext \
--slave %{_mandir}/man1/ktab.1$ext         ktab.1$ext                  %{_mandir}/man1/ktab-%{name}.1$ext

update-alternatives --install %{_jvmdir}/jre-%{origin} jre_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
--slave %{_jvmjardir}/jre-%{origin}        jre_%{origin}_exports     %{_jvmjardir}/%{jrelnk}

update-alternatives --install %{_jvmdir}/jre-%{javaver} jre_%{javaver} %{_jvmdir}/%{jrelnk} %{priority} \
--slave %{_jvmjardir}/jre-%{javaver}       jre_%{javaver}_exports      %{_jvmjardir}/%{jrelnk}

if [ -d %{_jvmdir}/%{jrelnk}/lib/security ]; then
  # Need to remove the old jars in order to support upgrading, ugly :(
  # update-alternatives fails silently if the link targets exist as files.
  rm -f %{_jvmdir}/%{jrelnk}/lib/security/{local,US_export}_policy.jar
fi
update-alternatives \
  --install \
    %{_jvmdir}/%{jrelnk}/lib/security/local_policy.jar \
    jce_%{javaver}_%{origin}_local_policy \
    %{_jvmprivdir}/%{name}/jce/vanilla/local_policy.jar \
    %{priority} \
  --slave \
    %{_jvmdir}/%{jrelnk}/lib/security/US_export_policy.jar \
    jce_%{javaver}_%{origin}_us_export_policy \
    %{_jvmprivdir}/%{name}/jce/vanilla/US_export_policy.jar

if [ -f %{_sysconfdir}/mime.types ]; then
   perl -p -i -e 's|application/x-java-jnlp-file.*||g' %{_sysconfdir}/mailcap.bak 2>/dev/null
   echo "type=application/x-java-jnlp-file; description=\"Java Web Start\"; exts=\"jnlp\"" >> %{_sysconfdir}/mailcap 2>/dev/null

   perl -p -i -e 's|application/x-java-jnlp-file.*||g' %{_sysconfdir}/mime.types 2>/dev/null
   echo "application/x-java-jnlp-file      jnlp" >> %{_sysconfdir}/mime.types 2>/dev/null
fi


%post devel
ext=
[ -f %{_mandir}/man1/javac-%{name}.1.bz2 ] && ext=".bz2"
[ -f %{_mandir}/man1/javac-%{name}.1.gz ] && ext=".gz"

update-alternatives --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} \
--slave %{_jvmdir}/java                     java_sdk                    %{_jvmdir}/%{sdklnk} \
--slave %{_jvmjardir}/java                  java_sdk_exports            %{_jvmjardir}/%{sdklnk} \
--slave %{_bindir}/appletviewer             appletviewer                %{sdkbindir}/appletviewer \
--slave %{_bindir}/extcheck                 extcheck                    %{sdkbindir}/extcheck \
--slave %{_bindir}/idlj                     idlj                        %{sdkbindir}/idlj \
--slave %{_bindir}/jar                      jar                         %{sdkbindir}/jar \
--slave %{_bindir}/jarsigner                jarsigner                   %{sdkbindir}/jarsigner \
--slave %{_bindir}/javadoc                  javadoc                     %{sdkbindir}/javadoc \
--slave %{_bindir}/javah                    javah                       %{sdkbindir}/javah \
--slave %{_bindir}/javap                    javap                       %{sdkbindir}/javap \
--slave %{_bindir}/jdb                      jdb                         %{sdkbindir}/jdb \
--slave %{_bindir}/jvisualvm                jvisualvm                   %{sdkbindir}/jvisualvm \
--slave %{_bindir}/native2ascii             native2ascii                %{sdkbindir}/native2ascii \
--slave %{_bindir}/rmic                     rmic                        %{sdkbindir}/rmic \
--slave %{_bindir}/serialver                serialver                   %{sdkbindir}/serialver \
--slave %{_bindir}/jconsole                 jconsole                    %{sdkbindir}/jconsole \
--slave %{_bindir}/pack200                  pack200                     %{sdkbindir}/pack200 \
--slave %{_bindir}/unpack200                unpack200                   %{sdkbindir}/unpack200 \
--slave %{_bindir}/HtmlConverter            HtmlConverter               %{sdkbindir}/HtmlConverter \
--slave %{_bindir}/apt                      apt                         %{sdkbindir}/apt \
--slave %{_bindir}/jinfo                    jinfo                       %{sdkbindir}/jinfo \
--slave %{_bindir}/jmap                     jmap                        %{sdkbindir}/jmap \
--slave %{_bindir}/jps                      jps                         %{sdkbindir}/jps \
--slave %{_bindir}/jsadebugd                jsadebugd                   %{sdkbindir}/jsadebugd \
--slave %{_bindir}/jstack                   jstack                      %{sdkbindir}/jstack \
--slave %{_bindir}/jstat                    jstat                       %{sdkbindir}/jstat \
--slave %{_bindir}/jstatd                   jstatd                      %{sdkbindir}/jstatd \
--slave %{_mandir}/man1/appletviewer.1$ext  appletviewer.1$ext          %{_mandir}/man1/appletviewer-%{name}.1$ext \
--slave %{_mandir}/man1/extcheck.1$ext      extcheck.1$ext              %{_mandir}/man1/extcheck-%{name}.1$ext \
--slave %{_mandir}/man1/idlj.1$ext          idlj.1$ext                  %{_mandir}/man1/idlj-%{name}.1$ext \
--slave %{_mandir}/man1/jar.1$ext           jar.1$ext                   %{_mandir}/man1/jar-%{name}.1$ext \
--slave %{_mandir}/man1/jarsigner.1$ext     jarsigner.1$ext             %{_mandir}/man1/jarsigner-%{name}.1$ext \
--slave %{_mandir}/man1/javac.1$ext         javac.1$ext                 %{_mandir}/man1/javac-%{name}.1$ext \
--slave %{_mandir}/man1/javadoc.1$ext       javadoc.1$ext               %{_mandir}/man1/javadoc-%{name}.1$ext \
--slave %{_mandir}/man1/javah.1$ext         javah.1$ext                 %{_mandir}/man1/javah-%{name}.1$ext \
--slave %{_mandir}/man1/javap.1$ext         javap.1$ext                 %{_mandir}/man1/javap-%{name}.1$ext \
--slave %{_mandir}/man1/jdb.1$ext           jdb.1$ext                   %{_mandir}/man1/jdb-%{name}.1$ext \
--slave %{_mandir}/man1/native2ascii.1$ext  native2ascii.1$ext          %{_mandir}/man1/native2ascii-%{name}.1$ext \
--slave %{_mandir}/man1/rmic.1$ext          rmic.1$ext                  %{_mandir}/man1/rmic-%{name}.1$ext \
--slave %{_mandir}/man1/serialver.1$ext     serialver.1$ext             %{_mandir}/man1/serialver-%{name}.1$ext \
--slave %{_mandir}/man1/jconsole.1$ext      jconsole.1$ext              %{_mandir}/man1/jconsole-%{name}.1$ext \
--slave %{_mandir}/man1/pack200.1$ext       pack200.1$ext               %{_mandir}/man1/pack200-%{name}.1$ext \
--slave %{_mandir}/man1/unpack200.1$ext     unpack200.1$ext             %{_mandir}/man1/unpack200-%{name}.1$ext \
--slave %{_mandir}/man1/apt.1$ext           apt.1$ext                   %{_mandir}/man1/apt-%{name}.1$ext \
--slave %{_mandir}/man1/jinfo.1$ext         jinfo.1$ext                 %{_mandir}/man1/jinfo-%{name}.1$ext \
--slave %{_mandir}/man1/jmap.1$ext          jmap.1$ext                  %{_mandir}/man1/jmap-%{name}.1$ext \
--slave %{_mandir}/man1/jps.1$ext           jps.1$ext                   %{_mandir}/man1/jps-%{name}.1$ext \
--slave %{_mandir}/man1/jsadebugd.1$ext     jsadebugd.1$ext             %{_mandir}/man1/jsadebugd-%{name}.1$ext \
--slave %{_mandir}/man1/jstack.1$ext        jstack.1$ext                %{_mandir}/man1/jstack-%{name}.1$ext \
--slave %{_mandir}/man1/jstat.1$ext         jstat.1$ext                 %{_mandir}/man1/jstat-%{name}.1$ext \
--slave %{_mandir}/man1/jstatd.1$ext        jstatd.1$ext                %{_mandir}/man1/jstatd-%{name}.1$ext \
--slave %{_mandir}/man1/jvisualvm.1$ext     jvisualvm.1$ext             %{_mandir}/man1/jvisualvm-%{name}.1$ext

update-alternatives --install %{_jvmdir}/java-%{origin} java_sdk_%{origin} %{_jvmdir}/%{sdklnk} %{priority} \
--slave %{_jvmjardir}/java-%{origin}        java_sdk_%{origin}_exports     %{_jvmjardir}/%{sdklnk}

update-alternatives --install %{_jvmdir}/java-%{javaver} java_sdk_%{javaver} %{_jvmdir}/%{sdklnk} %{priority} \
--slave %{_jvmjardir}/java-%{javaver}       java_sdk_%{javaver}_exports      %{_jvmjardir}/%{sdklnk}


# We do not care if all/any of this actually succeeds
# Therefore errors are caught but messages are allowed
%post fonts
{
    # Legacy font handling
    export PATH=${PATH}:%{_bindir}:%{_sbindir}

    if [ -d "%{x11bindir}" ]; then
      export PATH=${PATH}:%{x11bindir}
    fi

    if [ -d "/usr/share/X11/fonts/encodings" ]; then
      ENCODINGDIR=/usr/share/X11/fonts/encodings
    else
      ENCODINGDIR=%{x11encdir}
    fi

    ttmkfdir -d %{fontdir} -o %{fontdir}/fonts.scale

    # Mandrake workaround
    perl -pi -e 's@0-c-0@0-p-0@g' %{fontdir}/fonts.scale

    mkfontdir -e ${ENCODINGDIR} -e ${ENCODINGDIR}/large %{fontdir}

    if [ ! -z "$(which chkfontpath 2> /dev/null)" ]; then
      chkfontpath -q -a %{fontdir}
    fi

    if [ -d /etc/X11/fontpath.d ]; then
      ln -sf %{fontdir} /etc/X11/fontpath.d/%{name}-fonts
    fi

    # The following commands will be executed on upgrade by their respective
    # packages

    # Late legacy font handling
    if [ -x %{_bindir}/redhat-update-gnome-font-install ] ; then
        %{_bindir}/redhat-update-gnome-font-install
    fi

    if [ -x %{_bindir}/redhat-update-gnome-font-install2 ] ; then
        %{_bindir}/redhat-update-gnome-font-install2
    fi

    # Modern font handling
    if [ -x %{_bindir}/fc-cache ] ; then
        %{_bindir}/fc-cache -f %{_datadir}/fonts
    fi
} || :


%triggerin plugin -- mozilla, %{_bindir}/mozilla, firefox, %{_bindir}/firefox
{
  for bin in mozilla firefox ; do
    if [ -e %{_bindir}/$bin ] ; then
      _MOZILLA_PLUGIN_DIR=$(sed -n -e 's|"||g' \
        -e 's|^MOZ_DIST_BIN=\(.*\)$|\1|p' %{_bindir}/$bin)/plugins
      if [ -d "$_MOZILLA_PLUGIN_DIR" -o -h "$_MOZILLA_PLUGIN_DIR" ] ; then
        realdir=$(readlink "$_MOZILLA_PLUGIN_DIR" 2>/dev/null)
        [ -n "$realdir" ] && _MOZILLA_PLUGIN_DIR="$realdir"
%ifnarch x86_64
        ln -sf %{pluginname} "$_MOZILLA_PLUGIN_DIR/libjavaplugin_oji.so"
%else
        ln -sf %{pluginname} "/usr/lib64/mozilla/plugins/libnpjp2.so"
%endif

        echo "$_MOZILLA_PLUGIN_DIR" >> \
          %{_datadir}/%{name}/$bin-plugin-dirs
      fi
    fi
  done
} >/dev/null || :

%triggerin fonts -- fontconfig, %{fontconfigdir}/fonts.conf

TMPFILE=$(/bin/mktemp -q /tmp/fonts.conf.XXXXXX) && \
%{_bindir}/xsltproc --novalid %{xsldir}/register-java-fonts.xsl \
   %{fontconfigdir}/fonts.conf > $TMPFILE && \
/bin/cat $TMPFILE > %{fontconfigdir}/fonts.conf && /bin/rm $TMPFILE


%triggerun plugin -- mozilla, %{_bindir}/mozilla
{
  list=%{_datadir}/%{name}/mozilla-plugin-dirs
  [ $2 -eq 0 -a -e $list ] || exit 0
  while read d ; do
    [ -e "$d" ] || continue
    # Remove if the dir is only in this list, and it's our link.
    [ $(grep -l "^$d$" %{_datadir}/%{name}/*-plugin-dirs) = $list ] && \
      ( cd $d ; rm -f $(find . -lname %{pluginname}) )
  done < $list
  rm -f $list
} >/dev/null || :


%triggerun plugin -- firefox, %{_bindir}/firefox
{
  list=%{_datadir}/%{name}/firefox-plugin-dirs
  [ $2 -eq 0 -a -e $list ] || exit 0
  while read d ; do
    [ -e "$d" ] || continue
    # Remove if the dir is only in this list, and it's our link.
    [ $(grep -l "^$d$" %{_datadir}/%{name}/*-plugin-dirs) = $list ] && \
      ( cd $d ; rm -f $(find . -lname %{pluginname}) )
  done < $list
  rm -f $list
} >/dev/null || :


%preun plugin
{
  [ $1 -eq 0 ] || exit 0
  for list in %{_datadir}/%{name}/*-plugin-dirs ; do
    if [ -e "$list" ] ; then
      while read d ; do
        ( cd $d ; rm -f $(find . -lname %{pluginname}) )
      done < "$list"
      rm -f "$list"
    fi
  done
} >/dev/null || :

%postun
if [ $1 -eq 0 ]; then
  update-alternatives --remove java %{jrebindir}/java
  update-alternatives --remove \
    jce_%{javaver}_%{origin}_local_policy \
    %{_jvmprivdir}/%{name}/jce/vanilla/local_policy.jar
  update-alternatives --remove jre_%{origin}  %{_jvmdir}/%{jrelnk}
  update-alternatives --remove jre_%{javaver} %{_jvmdir}/%{jrelnk}
fi


%postun devel
if [ $1 -eq 0 ]; then
  update-alternatives --remove javac %{sdkbindir}/javac
  update-alternatives --remove java_sdk_%{origin}  %{_jvmdir}/%{sdklnk}
  update-alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdklnk}
fi


# We do not care if all/any of this actually succeeds
# Therefore errors are catched but messages allowed
%postun fonts
{
   # Rehash the font dir to keep only stuff manually installed
   [ $1 -eq 0 ] || exit 0

    export PATH=${PATH}:%{_bindir}:%{_sbindir}

    if [ -d "%{x11bindir}" ]; then
      export PATH=${PATH}:%{x11bindir}
    fi

    if [ -d "/usr/share/X11/fonts/encodings" ]; then
      ENCODINGDIR=/usr/share/X11/fonts/encodings
    else
      ENCODINGDIR=%{x11encdir}
    fi

   if [ -d %{fontdir} ] && [ $(%{_bindir}/find %{fontdir} \
        -follow -type f -iname "*.ttf" -printf "\b\b\b\btrue") ] ; then

        ttmkfdir -d %{fontdir} -o %{fontdir}/fonts.scale
        mkfontdir -e ${ENCODINGDIR} -e ${ENCODINGDIR}/large %{fontdir}

   else
        if [ ! -z "$(which chkfontpath 2> /dev/null)" ]; then
          chkfontpath -q -r %{fontdir}
        fi

        if [ -d /etc/X11/fontpath.d ]; then
          rm -f /etc/X11/fontpath.d/%{name}-fonts
        fi
   fi

   if [ -x %{_bindir}/redhat-update-gnome-font-install ] ; then
        %{_bindir}/redhat-update-gnome-font-install
   fi

   if [ -x %{_bindir}/redhat-update-gnome-font-install2 ] ; then
        %{_bindir}/redhat-update-gnome-font-install2
   fi

   if [ -x %{_bindir}/fc-cache ] ; then
        %{_bindir}/fc-cache -f %{_datadir}/fonts
   fi

} || :


%files -f %{name}-%{version}.files
%defattr(-,root,root,-)
%doc jre/COPYRIGHT jre/THIRDPARTYLICENSEREADME.txt jre/README
%doc jre/Welcome.html
%dir %{_jvmdir}/%{sdkdir}
%{jvmjardir}
%{_jvmdir}/%{jredir}/lib/fonts
%dir %{_jvmdir}/%{jredir}/lib/security
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/cacerts
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/javaws.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/blacklist
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/trusted.libraries
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/javafx.policy
%ghost %{_jvmdir}/%{jredir}/lib/security/local_policy.jar
%ghost %{_jvmdir}/%{jredir}/lib/security/US_export_policy.jar
%{_jvmdir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk}
%{_jvmprivdir}/*
%{_mandir}/man1/java-%{name}.1*
%{_mandir}/man1/keytool-%{name}.1*
%{_mandir}/man1/orbd-%{name}.1*
%{_mandir}/man1/policytool-%{name}.1*
%{_mandir}/man1/rmid-%{name}.1*
%{_mandir}/man1/rmiregistry-%{name}.1*
%{_mandir}/man1/servertool-%{name}.1*
%{_mandir}/man1/tnameserv-%{name}.1*
%{_mandir}/man1/javaws-%{name}.1*
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png

%files devel
%defattr(-,root,root,-)
%doc COPYRIGHT THIRDPARTYLICENSEREADME.txt README.html
%dir %{_jvmdir}/%{sdkdir}/bin
%dir %{_jvmdir}/%{sdkdir}/include
%dir %{_jvmdir}/%{sdkdir}/lib
%{_jvmdir}/%{sdkdir}/bin/*
%{_jvmdir}/%{sdkdir}/include/*
%{_jvmdir}/%{sdkdir}/lib/*
%{_jvmdir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk}
%{_mandir}/man1/appletviewer-%{name}.1*
%{_mandir}/man1/extcheck-%{name}.1*
%{_mandir}/man1/idlj-%{name}.1*
%{_mandir}/man1/jar-%{name}.1*
%{_mandir}/man1/jarsigner-%{name}.1*
%{_mandir}/man1/javac-%{name}.1*
%{_mandir}/man1/javadoc-%{name}.1*
%{_mandir}/man1/javah-%{name}.1*
%{_mandir}/man1/javap-%{name}.1*
%{_mandir}/man1/jdb-%{name}.1*
%{_mandir}/man1/jvisualvm-%{name}.1*
%{_mandir}/man1/native2ascii-%{name}.1*
%{_mandir}/man1/rmic-%{name}.1*
%{_mandir}/man1/serialver-%{name}.1*
%{_mandir}/man1/jconsole-%{name}.1*
%{_mandir}/man1/pack200-%{name}.1*
%{_mandir}/man1/unpack200-%{name}.1*
%{_mandir}/man1/apt-%{name}.1*
%{_mandir}/man1/jinfo-%{name}.1*
%{_mandir}/man1/jmap-%{name}.1*
%{_mandir}/man1/jps-%{name}.1*
%{_mandir}/man1/jsadebugd-%{name}.1*
%{_mandir}/man1/jstack-%{name}.1*
%{_mandir}/man1/jstat-%{name}.1*
%{_mandir}/man1/jstatd-%{name}.1*
%{_mandir}/man1/jhat-%{name}.1*
%{_mandir}/man1/jrunscript-%{name}.1*
%{_mandir}/man1/schemagen-%{name}.1*
%{_mandir}/man1/wsgen-%{name}.1*
%{_mandir}/man1/wsimport-%{name}.1*
%{_mandir}/man1/xjc-%{name}.1*
%{_mandir}/man1/jcmd-%{name}.1*
%{_mandir}/man1/javafxpackager-%{name}.1*

%ifnarch x86_64
%{cgibindir}/java-rmi-%{version}.cgi
%endif

%files src
%defattr(-,root,root,-)
%{_jvmdir}/%{sdkdir}/src.zip

%files alsa -f %{name}-%{version}-alsa.files
%defattr(-,root,root,-)

%files jdbc -f %{name}-%{version}-jdbc.files
%defattr(-,root,root,-)

%files plugin -f %{name}-%{version}-plugin.files
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
%ghost %{_datadir}/%{name}/*-plugin-dirs

%files fonts
%defattr(0644,root,root,0755)
%dir %{fontdir}
%dir %{xsldir}
%{fontdir}/*.ttf
%{xsldir}/*.xsl
%config(noreplace) %{fontdir}/fonts.alias
%ghost %{fontdir}/fonts.dir
%ghost %{fontdir}/fonts.scale
%ghost %{fontdir}/fonts.cache-1
%ghost %{fontdir}/XftCache
%ghost %{fontdir}/encodings.dir

%changelog
* Wed Mar 1 2013 Josh Toft <josh@likeness.com> - 0:1.7.0.21-1.2jpp.im
- Bumped to 1.7.0_21

* Wed Jun 13 2012 Henning P. Schmiedehausen <henning@likeness.com> - 0:1.7.0.5-1.1jpp.im
- Bumped to 1.7.0_05

* Wed Feb 22 2012 Henning P. Schmiedehausen <henning@likeness.com> - 0:1.7.0.3-1.1jpp.im
- Bumped to 1.7.0_03

* Thu Nov  3 2011 Henning P. Schmiedehausen <henning@likeness.com> - 0:1.6.0.29-1.1jpp.im
- bump to 1.6.0_29

* Thu Feb 17 2011 Henning P. Schmiedehausen <henning@schmiedehausen.org> - 0:1.6.0.24-1.1jpp.im
- bump to 1.6.0_24

* Mon Jan 31 2011 Henning P. Schmiedehausen <henning@schmiedehausen.org> - 0:1.6.0.23-1.1jpp.im
- bump to 1.6.0_23

* Sat Nov 20 2010 Henning P. Schmiedehausen <henning@schmiedehausen.org> - 0:1.6.0.22-1.1jpp.im
- bump to 1.6.0_22

* Fri Apr 16 2010 Henning P. Schmiedehausen <henning@schmiedehausen.org> - 0:1.6.0.20-1.1jpp.im
- bump to 1.6.0_20

* Tue Apr 13 2010 Henning P. Schmiedehausen <henning@schmiedehausen.org> - 0:1.6.0.19-1.1jpp.im
- bump to 1.6.0_19

* Fri Nov 27 2009 Henning P. Schmiedehausen <henning@schmiedehausen.org> - 0:1.6.0.17-1.1jpp.im
- bump to 1.6.0_17

* Thu Feb 12 2009 Henning P. Schmiedehausen <henning@schmiedehausen.org> - 0:1.6.0.12-1.1jpp.im
- bump to 1.6.0_12, enable browser plugin for x64

* Mon Nov 24 2008 Henning P. Schmiedehausen <henning@schmiedehausen.org> - 0:1.6.0.10-1.1jpp.im
- bump to 1.6.0_10

* Fri Aug 29 2008 Henning P. Schmiedehausen <henning@schmiedehausen.org> - 0:1.6.0.7-1.1jpp.im
- bump to 1.6.0_07

* Tue Apr 29 2008 Henning P. Schmiedehausen <hps@intermeta.de> - 0:1.6.0.6-1.1jpp.im
- 1.6.0_06

* Wed Feb  6 2008 Henning P. Schmiedehausen <hps@intermeta.de> - 0:1.6.0.4-1.1jpp.im
- 1.6.0_04

* Thu Oct 18 2007 Henning P. Schmiedehausen <hps@intermeta.de> - 0:1.6.0.3-1.1jpp.im
- bump to 1.6.0.3

* Sun Oct 07 2007 Jason Corley <jason.corley@gmail.com> 0:1.6.0.3-1jpp
- 1.6.0.3

* Sun Sep  9 2007 Henning P. Schmiedehausen <hps@intermeta.de> - 0:1.6.0.2-2jpp
- Fix font scripts and dependencies to deal with newer, modular X11 builds (e.g. Fedora 7)
- Fix ODBC dependency for JDBC-ODBC bridge

* Wed Jul 04 2007 Jason Corley <jason.corley@gmail.com> 0:1.6.0.2-1jpp
- 1.6.0.2

* Sat Jun 23 2007 Jason Corley <jason.corley@gmail.com> 0:1.6.0.1-1jpp
- 1.6.0.1 (contributed by Lyle Dietz)
- remove redundant defines for name, version, and release
- remove vendor and distribution (should be defined in ~/.rpmmacros)
- add JPackage license

* Thu Dec 21 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.10-2jpp
- respin, no changes

* Wed Dec 20 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.10-1jpp
- Upgrade to 1.5.0_10

* Mon Oct  2 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.09-1jpp
- Upgrade to 1.5.0_09... stupid Sun :-P (submitted by Henning Schmiedehausen)

* Fri Sep 29 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.08-1jpp
- Upgrade to 1.5.0_08

* Fri Jun 8 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.07-1jpp
- Upgrade to 1.5.0_07

* Fri Feb 3 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.06-1jpp
- Upgrade to 1.5.0_06

* Wed Sep 28 2005 Jason Corley <jason.corley@gmail.com> 0:1.5.0.05-1jpp
- Upgrade to 1.5.0_05

* Mon Jun 27 2005 Jason Corley <jason.corley@gmail.com> 0:1.5.0.04-1jpp
- Upgrade to 1.5.0_04

* Wed May 04 2005 David Walluck <david@jpackage.org> 0:1.5.0.03-1jpp
- 1.5.0_03

* Wed Mar 16 2005 Jason Corley <jason.corley@gmail.com> 0:1.5.0.02-1jpp
- Upgrade to 1.5.0_02

* Tue Feb 08 2005 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.5.0.01-3jpp
- Support for x86_64 (amd64); no javaws, no plugins

* Wed Jan 19 2005 David Walluck <david@jpackage.org> 0:1.5.0.01-1jpp
- 1.5.0_01

* Thu Jan 06 2005 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0.01-0.cte.1
- Updated to Upstream 1.5.0_01.
- Added long cvsversion definition.
- Rearranged defintiions that are sensitive to buildver.

* Sat Nov 13 2004 Ville Skyttä <scop at jpackage.org> - 0:1.5.0-3jpp
- Provide java-sasl.
- Fix build failure when no previous java-1.5.0 package is installed
  (%%{jvmjardir}/*.jar are dangling symlinks at build time).
- Minor spec cleanups and consistency tweaks.

* Sun Oct 17 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-2jpp.cte.1
- Switched off rpm internal dependency generator. This fixes the bogus
  devel package provides noted in 1.5.0-0.beta2.4jpp.
- Changed auto requires/provides for all packages to be the same as
  java-1.4.2-sun (all on except jdbc due to libodbc name variability).
- AutoReq off for demo package as it still looks for libjava_crw_demo_g.so.

* Mon Oct  4 2004 Ville Skyttä <scop at jpackage.org> - 0:1.5.0-2jpp
- Update to 1.5.0, thanks to Carwyn Edwards.
- Fix alternative priority (1500 -> 1503, where "3" is Sun).

* Fri Oct 1 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-0.cte.1
- Added missing Obsoletes for java-1.4.2-plugin.
- Modified release version to use fedora.us style 0. so jpp packages
  will override mine.

* Thu Sep 30 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-1jpp
- Updated to 1.5.0 final.

* Thu Sep 02 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-0.rc.1jpp
- Updated to J2SE 1.5.0 rc.
- Added alternatives slaves for new tools (and their man pages):
  apt, jinfo, jmap, jps, jsadebugd, jstack, jstat and jstatd.

* Mon Aug 02 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-0.beta2.4jpp
- Switch off AutoReq for demo package (breaks on: libjava_crw_demo.so).
- Switch off AutoReqProv for devel package (Provides: lib.so!?).

* Thu Jul 29 2004 Carwyn Edwards <carwyn@carwyn.com> 0:1.5.0-0.beta2.3jpp
- Corrected Requires and BuildRequires for jpackage-utils (1.5.38).

* Sun Jul 25 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-0.beta2.2jpp
- Use %%{_datadir}/xml for XSL's per FHS.
- Change plugin handling to be the same as 1.4.2.05-3jpp(sun)
  (adds firefox support).
- Remove dependency on %%{_bindir}/mozilla.
- Change manpage extension management to be the same as 1.4.2.05-3jpp(sun)
  (also supports uncompressed man pages).
- Rollback javaws alternative location to _datadir location so that concurrent
  jdk installation works again.
- Fixed freedesktop.org menu entry - Exec line was incorrect.
- Corrected the way the jconsole, pack200 and unpack200 man pages were added
  (use macros, added slave links).
- Actaully add jconsole, pack200, unpack200 and their alternatives links.

* Fri Jul 23 2004 Carwyn Edwards <carwyn@carwyn.com> 0:1.5.0-0.beta2.1jpp
- Updated to J2SE 1.5.0 Beta 2.
- Upstream filenames have changed, string replacement: "j2sdk" -> "jdk".
- Remove attempt to copy jre/.systemPrefs (it isn't there any more).
- Added man pages for jconsole, pack200 and unpack200

* Wed Feb 25 2004 David Walluck <david@anti-microsoft.org> 0:1.5.0-0.beta1.3jpp
- remove some unused code from the spec file

* Fri Feb 20 2004 David Walluck <david@anti-microsoft.org> 0:1.5.0-0.beta1.2jpp
- find man extension based on distribution
- ensure correct plugin installation
- Obsoletes: java-1.4.2-fonts
- install java-rmi.cgi
- move ControlPanel back to main so that we can use update-alternatives
- fix ControlPanel, HtmlConverter, and java-rmi.cgi bash scripts
- use included .desktop file for ControlPanel and modify included .desktop file for javaws

* Mon Feb 09 2004 David Walluck <david@anti-microsoft.org> 0:1.5.0-0.beta1.1jpp
- J2SE 1.5.0 Beta 1
- change javaws alternative to point to %%{_bindir}/javaws and only edit
  %%{_sysconfdir}/mime.types if it exists
- add javaws menu into main package (still looking for icon)
- fix installing extensions when %%{version} = %%{javaver}
- add epochs to all requires and provides
- really turn off automatic dependency generation
