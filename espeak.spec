%define major	1
%define libname	%mklibname %{name} %major
%define devname	%mklibname -d %{name}
%define	debug_package	%nil

Summary:	Text to speech synthesis engine
Name:		espeak
Version:	1.47.07
Release:	7
License:	GPLv3+
Group:		Sound
Url:		http://espeak.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/%{name}/%{name}-%{version}/%{name}-%{version}-source.zip
Source1:	espeak.1
Source2:	http://espeak.sourceforge.net/data/ru_dict-46.zip
Source3:	zhy_dict-46.zip
Source4:	zh_dict-46.zip
Source5:	espeak.rpmlintrc
#gw from Fedora: make it work with pulseaudio enabled or disabled
Patch2:	espeak-1.46.02-runtime-detection.patch

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
%apply_patches
chmod 644 ReadMe *.txt
rm -f src/portaudio.h
rm -f espeak-data/ru_dict
rm -f espeak-data/zh_dict
rm -f espeak-data/zhy_dict
cd espeak-data
unzip %{SOURCE2}
unzip %{SOURCE3}
unzip %{SOURCE4}

%build
cd src
%make LDFLAGS="%{?ldflags}"

%install
%makeinstall_std -C src \
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

