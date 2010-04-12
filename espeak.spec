%define name espeak
%define version 1.43
%define release %mkrel 3

%define major 1
%define libname %mklibname %name %major
%define libnamedev %mklibname -d %name

#disable autorequires on portaudio since we build with portaudio0
#define _requires_exceptions devel(libportaudio

Summary: Text to speech synthesis engine
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/project/espeak/%{name}/%{name}-%{version}/%{name}-%{version}-source.zip
Source1: espeak.1
Patch0: espeak-1.39-ldflags.patch
#gw from Fedora: make it work with pulseaudio enabled or disabled
Patch2: espeak-1.42.04-runtime-detection.patch
License: GPLv3+
Group: Sound
Url: http://espeak.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
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

%description -n %libnamedev
eSpeak is a compact open source software speech synthesizer for
English and other languages.

eSpeak produces good quality English speech. It uses a different
synthesis method from other open source TTS engines, and sounds quite
different. It's perhaps not as natural or "smooth", but I find the
articulation clearer and easier to listen to for long periods.


%prep
%setup -q -n %name-%version-source
%patch0 -p0
%patch2 -p1
chmod 644 ReadMe ChangeLog *.txt
rm -f src/portaudio.h

%build
cd src
make CXXFLAGS="%{optflags}" LDFLAGS="%{?ldflags}"

%install
rm -rf %{buildroot}
cd src
%makeinstall_std BINDIR=%_bindir INCDIR=%_includedir/%name LIBDIR=%_libdir DATADIR=%_datadir/%name-data LDFLAGS="%{?ldflags}"

install -m 644 -D %SOURCE1 %buildroot%_mandir/man1/%name.1
%clean
rm -rf %{buildroot}

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
%_mandir/man1/%name.1*

%files -n %libname
%defattr(-,root,root)
%_libdir/libespeak.so.%{major}*

%files -n %libnamedev
%defattr(-,root,root)
%_includedir/%name
%_libdir/libespeak.so
%_libdir/libespeak.a


