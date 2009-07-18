Name:           ogmrip
Version:        0.13.0
Release:        2%{?dist}
Summary:        DVD ripping and encoding graphical user interface

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://ogmrip.sourceforge.net/
Source0:        http://downloads.sourceforge.net/ogmrip/ogmrip-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel, libglade2-devel, GConf2-devel, libxml2-devel
BuildRequires:  hal-devel, dbus-glib-devel, enchant-devel, enca-devel
BuildRequires:  libdvdread-devel, libtheora-devel, libvorbis-devel
BuildRequires:  libtiff-devel
BuildRequires:  tesseract-devel
BuildRequires:  libnotify-devel
BuildRequires:  gettext-devel, intltool
BuildRequires:  desktop-file-utils

# We patch configure.in
BuildRequires:  autoconf

# Not technically build required, but configure checks for it...
Buildrequires:  eject, mplayer, mencoder, ogmtools, vorbis-tools, theora-tools
BuildRequires:  mkvtoolnix, lame

# Now, all the same as runtime requirements
Requires: eject, mplayer, mencoder, ogmtools, vorbis-tools, theora-tools
Requires: mkvtoolnix, lame
Requires: gpac
Requires: subtitleripper

Requires(post): GConf2
Requires(postun): GConf2

Patch0: http://ogmrip.sourceforge.net/patches/ogmrip-0.13.0-configure.patch
Patch1: ogmrip-0.13.0-gtk-include.patch


%description
OGMRip is an application and a set of libraries for ripping and encoding DVDs
into AVI, OGM MP4 or Matroska files using a wide variety of codecs. It relies
on mplayer, mencoder, ogmtools, mkvtoolnix, oggenc, lame and faac to perform
its tasks.


%package devel
Summary: Development files for ogmrip
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires:  gtk2-devel, libglade2-devel, GConf2-devel, libxml2-devel
Requires:  hal-devel, dbus-glib-devel, enchant-devel, enca-devel
Requires:  libdvdread-devel, libtheora-devel, libvorbis-devel
Requires:  libtiff-devel
Requires:  tesseract-devel
Requires:  libnotify-devel
Requires:  pkgconfig

%description devel
Development headers and libraries for ogmrip.


%prep
%setup -q
%patch0 -p0 -b .configure
%patch1 -p1 -b .configure


%build
autoconf
%configure \
    --disable-static \
    --disable-schemas-install \
    --with-ocr=tesseract
# Disable RPATH
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%find_lang %{name}

# Remove useless files
find %{buildroot} -name '*.la' -delete

desktop-file-install \
    --delete-original \
    --dir=%{buildroot}%{_datadir}/applications \
    %{buildroot}/%{_datadir}/applications/ogmrip.desktop


%clean
rm -rf %{buildroot}


%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
    %{_sysconfdir}/gconf/schemas/ogmrip.schemas &>/dev/null || :

%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
        %{_sysconfdir}/gconf/schemas/ogmrip.schemas &>/dev/null || :
fi

%postun -p /sbin/ldconfig



%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO
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
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
* Sun Jul 19 2009 Gianluca Sforna <giallu gmail com> - 0.13.0-2
* add patch to compile against gtk2-2.17.4

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
