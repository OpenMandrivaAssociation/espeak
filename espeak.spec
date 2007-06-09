%define name espeak
%define version 1.26
%define release %mkrel 1

%define major 1
%define libname %mklibname %name %major

Summary: Text to speech synthesis engine
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/espeak/%{name}-%{version}-source.tar.bz2
Patch:espeak-1.21-mkstemp.patch
License: GPL
Group: Sound
Url: http://espeak.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libportaudio-devel
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

%package -n %libname-devel
Group: Development/C++
Summary: Text to speech library
Requires: %libname = %version
Provides: libespeak-devel = %version-%release

%description -n %libname-devel
eSpeak is a compact open source software speech synthesizer for
English and other languages.

eSpeak produces good quality English speech. It uses a different
synthesis method from other open source TTS engines, and sounds quite
different. It's perhaps not as natural or "smooth", but I find the
articulation clearer and easier to listen to for long periods.


%prep
%setup -q -n %name-%version-source
%patch -p1 -b .mkstemp
chmod 644 ReadMe ChangeLog *.txt
rm -f src/portaudio.h

%build
cd src
make

%install
rm -rf $RPM_BUILD_ROOT
cd src
mkdir -p %buildroot%_datadir/%name-data
%makeinstall BINDIR=%buildroot%_bindir INCDIR=%buildroot%_includedir/%name LIBDIR=%buildroot%_libdir DATADIR=%buildroot%_datadir/%name-data

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc ReadMe ChangeLog *.txt docs
%_bindir/%name
%_datadir/%name-data

%files -n %libname
%defattr(-,root,root)
%_libdir/libespeak.so.%{major}*

%files -n %libname-devel
%defattr(-,root,root)
%_includedir/%name
%_libdir/libespeak.so
%_libdir/libespeak.a


