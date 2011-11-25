%define name espeak
%define version 1.46.01
%define release %mkrel 1

%define major 1
%define libname %mklibname %name %major
%define libnamedev %mklibname -d %name

#disable autorequires on portaudio since we build with portaudio0
#define _requires_exceptions devel(libportaudio

Summary: Text to speech synthesis engine
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/project/%{name}/%{name}-%{version}/%{name}-%{version}-source.zip
Source1: espeak.1
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
chmod 644 ReadMe *.txt
rm -f src/portaudio.h

%build
cd src
make CXXFLAGS="%{optflags}" LDFLAGS="%{?ldflags}" AUDIO=runtime

%install
rm -rf %{buildroot}
cd src
%makeinstall_std BINDIR=%_bindir INCDIR=%_includedir/%name LIBDIR=%_libdir DATADIR=%_datadir/%name-data LDFLAGS="%{?ldflags}"

install -m 644 -D %SOURCE1 %buildroot%_mandir/man1/%name.1
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ReadMe  *.txt docs
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


