%define major	1
%define libname	%mklibname %{name} %major
%define devname	%mklibname -d %{name}

Summary:	Text to speech synthesis engine
Name:		espeak
Version:	1.48.04
Release:	3
License:	GPLv3+
Group:		Sound
Url:		http://espeak.sourceforge.net/
Source0:	http://sourceforge.net/projects/espeak/files/espeak/espeak-%(echo %{version}|cut -d. -f1-2)/espeak-%{version}-source.zip
Source1:	espeak.1
Source2:	http://espeak.sourceforge.net/data/ru_dict-48.zip
Source3:	http://espeak.sourceforge.net/data/ru_listx.zip
Source4:	http://espeak.sourceforge.net/data/zhy_list.zip
Source5:	http://espeak.sourceforge.net/data/zh_listx.zip
Source50:	espeak.rpmlintrc
Patch1:		espeak-1.48.04-compile.patch
#gw from Fedora: make it work with pulseaudio enabled or disabled
Patch2:		espeak-1.46.02-runtime-detection.patch

BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(portaudio-2.0)
Requires:	sox

%description
eSpeak is a compact open source software speech synthesizer for
English and other languages.

eSpeak produces good quality English speech. It uses a different
synthesis method from other open source TTS engines, and sounds quite
different. It's perhaps not as natural or "smooth", but I find the
articulation clearer and easier to listen to for long periods.

%package -n %{libname}
Summary:	Text to speech library
Group:		System/Libraries
Suggests:	%{name} >= %{version}

%description -n %{libname}
This package contains the shared library for %{name}.

%package -n %{devname}
Summary:	Text to speech library
Group:		Development/C++
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the development files for %{name}.

%prep
%setup -qn %{name}-%{version}-source
%autopatch -p1
chmod 644 ReadMe *.txt
rm -f src/portaudio.h
rm -f espeak-data/ru_dict
rm -f espeak-data/zh_dict
rm -f espeak-data/zhy_dict
cd espeak-data
unzip %{SOURCE2}
cd ..
cd dictsource
unzip %{S:3}
unzip %{S:4}
unzip %{S:5}

%build
TOPDIR="$(pwd)"
cd src
%make_build LDFLAGS="%{build_ldflags}" CXXFLAGS="%{optflags}" CC=%{__cc} CXX=%{__cxx}
cd ../dictsource
export LD_LIBRARY_PATH="$TOPDIR/src"
export ESPEAK_DATA_PATH="$TOPDIR"
../src/espeak --compile=ru
../src/espeak --compile=zh
../src/espeak --compile=zh-yue

%install
%make_install -C src \
	BINDIR=%{_bindir} \
	INCDIR=%{_includedir}/%{name}src \
	LIBDIR=%{_libdir} \
	DATADIR=%{_datadir}/%{name}-data \
	LDFLAGS="%{?ldflags}"

install -m 644 -D %{SOURCE1} %{buildroot}%{_mandir}/man1/%{name}.1
rm -f %{buildroot}/%{_libdir}/libespeak.a
mv %{buildroot}/%{_includedir}/espeaksrc/ %{buildroot}/%{_includedir}/espeak/

%pre
# some dirs for languages changed to files, so remove old dirs and files
[ $1 -gt 1 -a -d /usr/share/espeak-data/voices ] && \
rm -rf /usr/share/espeak-data/voices || :

%files
%doc ReadMe *.txt docs
%{_bindir}/%{name}
%{_datadir}/%{name}-data
%{_mandir}/man1/%{name}.1*

%files -n %{libname}
%{_libdir}/libespeak.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/libespeak.so
