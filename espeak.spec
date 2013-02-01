%define name espeak
%define version 1.46.02
%define release 3

%define major 1
%define libname %mklibname %{name} %major
%define libnamedev %mklibname -d %{name}

#disable autorequires on portaudio since we build with portaudio0
#define _requires_exceptions devel(libportaudio

Summary: Text to speech synthesis engine
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/project/%{name}/%{name}-%{version}/%{name}-%{version}-source.zip
Source1: espeak.1
Source2: http://espeak.sourceforge.net/data/ru_dict-46.zip
Source3: zhy_dict-46.zip
Source4: zh_dict-46.zip
#Patch0: espeak-1.39-ldflags.patch
#gw from Fedora: make it work with pulseaudio enabled or disabled
Patch2: espeak-1.46.02-runtime-detection.patch
License: GPLv3+
Group: Sound
Url: http://espeak.sourceforge.net/
BuildRequires: portaudio-devel
BuildRequires: pulseaudio-devel
Requires: sox

%description
eSpeak is a compact open source software speech synthesizer for
English and other languages.

eSpeak produces good quality English speech. It uses a different
synthesis method from other open source TTS engines, and sounds quite
different. It's perhaps not as natural or "smooth", but I find the
articulation clearer and easier to listen to for long periods.

%package -n %libname
Group: System/Libraries
Summary: Text to speech library
Requires: %{name} >= %{version}

%description -n %libname
eSpeak is a compact open source software speech synthesizer for
English and other languages.

eSpeak produces good quality English speech. It uses a different
synthesis method from other open source TTS engines, and sounds quite
different. It's perhaps not as natural or "smooth", but I find the
articulation clearer and easier to listen to for long periods.

%package -n %libnamedev
Group: Development/C++
Summary: Text to speech library
Requires: %libname = %{version}
Provides: libespeak-devel = %{version}-%{release}
Obsoletes: %mklibname -d %{name} %major

%description -n %libnamedev
eSpeak is a compact open source software speech synthesizer for
English and other languages.

eSpeak produces good quality English speech. It uses a different
synthesis method from other open source TTS engines, and sounds quite
different. It's perhaps not as natural or "smooth", but I find the
articulation clearer and easier to listen to for long periods.


%prep
%setup -q -n %{name}-%{version}-source
#%patch0 -p0
%patch2 -p1
chmod 644 ReadMe *.txt
rm -f src/portaudio.h
rm -f espeak-data/ru_dict
rm -f espeak-data/zh_dict
rm -f espeak-data/zhy_dict
cd espeak-data
unzip %SOURCE2
unzip %SOURCE3
unzip %SOURCE4

%build
cd src
make CXXFLAGS="%{optflags}" LDFLAGS="%{?ldflags}"

%install
cd src
%makeinstall_std BINDIR=%{_bindir} INCDIR=%{_includedir}/%{name} LIBDIR=%{_libdir} DATADIR=%{_datadir}/%{name}-data LDFLAGS="%{?ldflags}"

install -m 644 -D %SOURCE1 %{buildroot}%{_mandir}/man1/%{name}.1

%files
%defattr(-,root,root)
%doc ReadMe *.txt docs
%{_bindir}/%{name}
%{_datadir}/%{name}-data
%{_mandir}/man1/%{name}.1*

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libespeak.so.%{major}*

%files -n %libnamedev
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/libespeak.so
%{_libdir}/libespeak.a




%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.43.03-2mdv2011.0
+ Revision: 664150
- mass rebuild

* Mon Aug 02 2010 Götz Waschk <waschk@mandriva.org> 1.43.03-1mdv2011.0
+ Revision: 565014
- new version

* Mon Apr 12 2010 Götz Waschk <waschk@mandriva.org> 1.43-3mdv2010.1
+ Revision: 533668
- remove wrong dep on portaudio0-devel

* Wed Mar 31 2010 Götz Waschk <waschk@mandriva.org> 1.43-2mdv2010.1
+ Revision: 530175
- add patch for runtime pulseaudio detection (bug #58490)

* Fri Feb 19 2010 Frederik Himpe <fhimpe@mandriva.org> 1.43-1mdv2010.1
+ Revision: 508515
- Update to new version 1.43
- Fix download URL

* Thu Dec 24 2009 Götz Waschk <waschk@mandriva.org> 1.42.04-1mdv2010.1
+ Revision: 482018
- new version
- drop patch 1

* Fri Dec 04 2009 Götz Waschk <waschk@mandriva.org> 1.41.01-3mdv2010.1
+ Revision: 473437
- patch to really use pulseaudio
- add man page from Fedora

* Tue Dec 01 2009 Götz Waschk <waschk@mandriva.org> 1.41.01-2mdv2010.1
+ Revision: 472201
- build with pulseaudio output

* Tue Aug 25 2009 Frederik Himpe <fhimpe@mandriva.org> 1.41.01-1mdv2010.0
+ Revision: 421233
- Update to new version 1.41.01
- Fix BuildRequires

* Fri Feb 27 2009 Emmanuel Andry <eandry@mandriva.org> 1.40.02-3mdv2009.1
+ Revision: 345810
- switch back to portaudio0-devel (my tests with portaudio2 were not long enough)

* Fri Feb 27 2009 Emmanuel Andry <eandry@mandriva.org> 1.40.02-2mdv2009.1
+ Revision: 345679
- use default portaudio

* Mon Jan 12 2009 Götz Waschk <waschk@mandriva.org> 1.40.02-1mdv2009.1
+ Revision: 328489
- update to new version 1.40.02

* Wed Dec 24 2008 Funda Wang <fwang@mandriva.org> 1.40.01-1mdv2009.1
+ Revision: 318235
- new verison 1.40.01

* Tue Dec 23 2008 Götz Waschk <waschk@mandriva.org> 1.40-1mdv2009.1
+ Revision: 317823
- new version
- fix build

* Mon Oct 27 2008 Funda Wang <fwang@mandriva.org> 1.39-3mdv2009.1
+ Revision: 297624
- revert to portaudio18

* Mon Oct 27 2008 Funda Wang <fwang@mandriva.org> 1.39-2mdv2009.1
+ Revision: 297532
- BR portaudio19
- use ldflags when building

* Tue Sep 09 2008 Götz Waschk <waschk@mandriva.org> 1.39-1mdv2009.0
+ Revision: 282909
- new version

* Sat Aug 23 2008 Götz Waschk <waschk@mandriva.org> 1.38-1mdv2009.0
+ Revision: 275296
- new version
- update license

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.37-4mdv2009.0
+ Revision: 264462
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Apr 18 2008 Götz Waschk <waschk@mandriva.org> 1.37-3mdv2009.0
+ Revision: 195538
- new version

* Thu Mar 13 2008 Frederic Crozat <fcrozat@mandriva.com> 1.36.02-3mdv2008.1
+ Revision: 187508
- Exclude requires, not provides

* Thu Mar 13 2008 Frederic Crozat <fcrozat@mandriva.com> 1.36.02-2mdv2008.1
+ Revision: 187471
- Disable autorequires on devel portaudio package since we build with portaudio18

* Thu Mar 13 2008 Frederic Crozat <fcrozat@mandriva.com> 1.36.02-1mdv2008.1
+ Revision: 187448
- Fix buildrequires for x86-64
- Release 1.36.02
- Build with portaudio18, since portaudio19 alsa support doesn't work with Pulseaudio :(

* Fri Jan 25 2008 Colin Guthrie <cguthrie@mandriva.org> 1.31-2mdv2008.1
+ Revision: 157871
- Rebuild to fix extension

* Sun Jan 20 2008 Götz Waschk <waschk@mandriva.org> 1.31-1mdv2008.1
+ Revision: 155301
- new version
- *** empty log message ***

* Mon Dec 31 2007 Götz Waschk <waschk@mandriva.org> 1.30-1mdv2008.1
+ Revision: 139858
- new version

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of buildroot on Pixel's request

* Mon Aug 27 2007 Götz Waschk <waschk@mandriva.org> 1.29-1mdv2008.0
+ Revision: 71890
- new devel name
- new version
- drop patch

* Mon Aug 20 2007 Oden Eriksson <oeriksson@mandriva.com> 1.28-2mdv2008.0
+ Revision: 67911
- rebuilt against new portaudio libs

* Mon Jul 16 2007 Götz Waschk <waschk@mandriva.org> 1.28-1mdv2008.0
+ Revision: 52755
- new version

* Sat Jun 30 2007 Götz Waschk <waschk@mandriva.org> 1.27-1mdv2008.0
+ Revision: 46122
- new version

* Sat Jun 09 2007 Götz Waschk <waschk@mandriva.org> 1.26-1mdv2008.0
+ Revision: 37668
- new version

* Sat May 19 2007 Götz Waschk <waschk@mandriva.org> 1.25-1mdv2008.0
+ Revision: 28440
- new version

* Thu May 03 2007 Götz Waschk <waschk@mandriva.org> 1.24-1mdv2008.0
+ Revision: 21896
- new version

* Sun Apr 22 2007 Götz Waschk <waschk@mandriva.org> 1.23-1mdv2008.0
+ Revision: 16897
- new version
- update file list


* Fri Apr 06 2007 Götz Waschk <waschk@mandriva.org> 1.22-1mdv2007.1
+ Revision: 150798
- new version
- fix installation

* Wed Feb 28 2007 Götz Waschk <waschk@mandriva.org> 1.21-1mdv2007.1
+ Revision: 127156
- new version
- rediff the patch

* Wed Feb 07 2007 Götz Waschk <waschk@mandriva.org> 1.20-1mdv2007.1
+ Revision: 116969
- new version
- rediff the patch

* Tue Jan 30 2007 Götz Waschk <waschk@mandriva.org> 1.19-3mdv2007.1
+ Revision: 115424
- replace tmpnam by mkstemp

* Tue Jan 30 2007 Götz Waschk <waschk@mandriva.org> 1.19-2mdv2007.1
+ Revision: 115413
- fix doc permissions
- depend on sox

* Sat Jan 27 2007 Götz Waschk <waschk@mandriva.org> 1.19-1mdv2007.1
+ Revision: 114403
- Import espeak

* Sat Jan 27 2007 G�tz Waschk <waschk@mandriva.org> 1.19-1mdv2007.1
- initial package

