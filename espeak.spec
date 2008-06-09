%define name espeak
%define version 1.37
%define release %mkrel 3

%define major 1
%define libname %mklibname %name %major
%define libnamedev %mklibname -d %name

#disable autorequires on portaudio since we build with portaudio0
%define _requires_exceptions devel(libportaudio

Summary: Text to speech synthesis engine
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/espeak/%{name}-%{version}-source.zip
License: GPL
Group: Sound
Url: http://espeak.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: portaudio0-devel
#BuildRequires: pulseaudio-devel
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
Requires: %name >= %version

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
Requires: %libname = %version
Provides: libespeak-devel = %version-%release
Obsoletes: %mklibname -d %name %major
Requires: portaudio0-devel


%description -n %libnamedev
eSpeak is a compact open source software speech synthesizer for
English and other languages.

eSpeak produces good quality English speech. It uses a different
synthesis method from other open source TTS engines, and sounds quite
different. It's perhaps not as natural or "smooth", but I find the
articulation clearer and easier to listen to for long periods.


%prep
%setup -q -n %name-%version-source
chmod 644 ReadMe ChangeLog *.txt
rm -f src/portaudio.h

%build
cd src
#gw use this to build with pulseaudio support ONLY
#make AUDIO=pulseaudio
make 


%install
rm -rf $RPM_BUILD_ROOT
cd src
mkdir -p %buildroot%_datadir/%name-data
%makeinstall BINDIR=%buildroot%_bindir INCDIR=%buildroot%_includedir/%name LIBDIR=%buildroot%_libdir DATADIR=%buildroot%_datadir/%name-data

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc ReadMe ChangeLog *.txt docs
%_bindir/%name
%_datadir/%name-data

%files -n %libname
%defattr(-,root,root)
%_libdir/libespeak.so.%{major}*

%files -n %libnamedev
%defattr(-,root,root)
%_includedir/%name
%_libdir/libespeak.so
%_libdir/libespeak.a


