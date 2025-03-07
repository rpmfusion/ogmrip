Name:           ogmrip
Version:        1.0.1
Release:        21%{?dist}
Summary:        DVD ripping and encoding graphical user interface

License:        GPLv2+
URL:            http://ogmrip.sourceforge.net/
Source0:        http://downloads.sourceforge.net/ogmrip/ogmrip-%{version}.tar.gz

BuildRequires:  gtk2-devel, libglade2-devel, GConf2-devel, libxml2-devel
BuildRequires:  dbus-glib-devel, enchant-devel, enca-devel
BuildRequires:  libdvdread-devel, libtheora-devel, libvorbis-devel
BuildRequires:  libtiff-devel
BuildRequires:  tesseract-devel
BuildRequires:  libnotify-devel
BuildRequires:  gettext-devel, intltool, gcc
BuildRequires:  desktop-file-utils

# Not technically build required, but configure checks for it...
Buildrequires:  mplayer, mencoder, vorbis-tools, theora-tools
BuildRequires:  mkvtoolnix, lame

# Now, all the same as runtime requirements
Requires: mplayer, mencoder, vorbis-tools, theora-tools
Requires: mkvtoolnix, lame
Requires: gpac
Requires: tesseract

Requires(post): GConf2
Requires(postun): GConf2


%description
OGMRip is an application and a set of libraries for ripping and encoding DVDs
into AVI, OGM MP4 or Matroska files using a wide variety of codecs. It relies
on mplayer, mencoder, mkvtoolnix, oggenc, lame and faac to perform
its tasks.


%package devel
Summary: Development files for ogmrip
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires:  gtk2-devel, libglade2-devel, GConf2-devel, libxml2-devel
Requires:  dbus-glib-devel, enchant-devel, enca-devel
Requires:  libdvdread-devel, libtheora-devel, libvorbis-devel
Requires:  libtiff-devel
Requires:  tesseract-devel
Requires:  libnotify-devel
Requires:  pkgconfig

%description devel
Development headers and libraries for ogmrip.


%prep
%autosetup

%build
%configure \
    --disable-static \
    --disable-schemas-install \
    --with-ocr=tesseract
# Disable RPATH
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install
%find_lang %{name}

# Remove useless files
find %{buildroot} -name '*.la' -delete

desktop-file-install \
    --delete-original \
    --dir=%{buildroot}%{_datadir}/applications \
    %{buildroot}/%{_datadir}/applications/ogmrip.desktop


%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
    %{_sysconfdir}/gconf/schemas/ogmrip.schemas &>/dev/null || :

%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
        %{_sysconfdir}/gconf/schemas/ogmrip.schemas &>/dev/null || :
fi


%files -f %{name}.lang
%doc AUTHORS ChangeLog README TODO
%license COPYING
%{_sysconfdir}/gconf/schemas/ogmrip.schemas
%{_bindir}/dvdcpy
%{_bindir}/avibox
%{_bindir}/ogmrip
%{_bindir}/subp2pgm
%{_bindir}/subp2png
%{_bindir}/subp2tiff
%{_bindir}/subptools
%{_bindir}/theoraenc
%{_libdir}/*.so.*
%{_libdir}/ogmrip/
%{_datadir}/applications/ogmrip.desktop
%doc %{_datadir}/gtk-doc/html/ogm*
%{_datadir}/ogmrip/
%{_datadir}/pixmaps/ogmrip.png
%{_mandir}/man1/*.1*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Feb 02 2023 Leigh Scott <leigh123linux@gmail.com> - 1.0.1-17
- Drop ogmtools requirement due to fedora retirement

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 21 2020 Leigh Scott <leigh123linux@gmail.com> - 1.0.1-12
- Rebuild for new libdvdread

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 15 2019 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 1.0.1-9
- rebuild for libdvdread ABI bump

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.1-6
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 15 2015 Thomas Björklund <tb@ludd.ltu.se> - 1.0.1-1
- new upstream release
- drop upstreamed patches

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Feb  3 2014 Gianluca Sforna <giallu@gmail.com> - 1.0.0-3
- add upstream patch for startup hang (#3124)

* Mon May 27 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.0-2
- Rebuilt for x264/FFmpeg

* Thu Mar 14 2013 Gianluca Sforna <giallu@gmail.com> - 1.0.0-1
- new upstream release

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.13.8-3
- Mass rebuilt for Fedora 19 Features

* Wed Jun 13 2012 Gianluca Sforna <giallu@gmail.com> - 0.13.8-2
- remove hal-devel dep from -devel package

* Sat May 19 2012 Gianluca Sforna <giallu@gmail.com> - 0.13.8-1
- new upstream release

* Tue May 15 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.13.7-3
- Orphan subtitleripper

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.13.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Gianluca Sforna <giallu@gmail.com> - 0.13.7-1
- new upstream release
- drop upstreamed patches

* Tue Jul 26 2011 Gianluca Sforna <giallu@gmail.com> - 0.13.6-2
- Fix build with newer GLib
- Fix preferences bug with upstream patch

* Sun Nov 21 2010 Gianluca Sforna <giallu@gmail.com> - 0.13.6-1
- new upstream release
- Fix build with GTK3 and libnotify 0.7

* Fri May 21 2010 Gianluca Sforna <giallu gmail com> - 0.13.5-1
- new upstream release
- drop upstreamed patch

* Mon Mar 22 2010 Gianluca Sforna <giallu gmail com> - 0.13.4-1
- New upstream release
- Add patch to compile against GTK 2.19

* Thu Dec 24 2009 Gianluca Sforna <giallu gmail com> - 0.13.3-1
- New upstream release

* Thu Oct  8 2009 Gianluca Sforna <giallu gmail com> - 0.13.2-1
- New upstream release
- drop dependencies on hal-devel and eject

* Mon Sep 21 2009 Gianluca Sforna <giallu gmail com> - 0.13.1-1
- New upstream release
- drop upstreamed patches

* Fri Aug 14 2009 Gianluca Sforna <giallu gmail com> - 0.13.0-4
- Require tesseract for subtitle extraction

* Sun Jul 19 2009 Gianluca Sforna <giallu gmail com> - 0.13.0-3
- add patch to compile against gtk2-2.17.4

* Fri Jul 17 2009 Gianluca Sforna <giallu gmail com> - 0.13.0-1
- New upstream release
- drop upstreamed patches

* Mon Apr 20 2009 Gianluca Sforna <giallu gmail com> - 0.12.3-3
- Add Requires on -devel
- Find and remove .la files
- Properly install .desktop file

* Mon Feb 16 2009 Gianluca Sforna <giallu gmail com> - 0.12.3-2
- Rebase Patch0

* Mon Feb  9 2009 Gianluca Sforna <giallu gmail com> - 0.12.3-1
- Upstream release 0.12.3

* Sat Dec 13 2008 Gianluca Sforna <giallu gmail com> - 0.12.2-1
- New spec based off freshrpms for Fedora submission
