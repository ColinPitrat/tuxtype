#
# spec file for package tuxtype 
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# norootforbuild

Name:           tuxtype
Summary:        Typing tutor for children
Url:            http://alioth.debian.org/projects/tux4kids/
%define         realname tuxtype_w_fonts
License:        GNU General Public License (GPL) v2, Open Font License v1.1, free (BSD-like) license
Group:          Amusements/Games/Action/Other
Version:        1.7.2
Release:        5.1
Vendor:         openSUSE-Education
Source:         %realname-%version.tar.bz2
Source1:        tuxtype.desktop
BuildRequires:  SDL-devel SDL_image-devel SDL_mixer-devel dialog gcc-c++ SDL_Pango-devel gtk-devel
BuildRequires:  SDL_ttf-devel
BuildRequires:  ImageMagick 
%if 0%{?suse_version}
BuildRequires:  update-desktop-files
BuildRequires:  fdupes
BuildRequires:  freefont
%endif
%if 0%{?fedora_version}
BuildRequires:  desktop-file-utils
BuildRequires:  freefont
%endif
%if 0%{?mandriva_version}
BuildRequires:  fonts-ttf-freefont
BuildRequires:  pulseaudio-esound-compat
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Tux Typing is an educational typing tutor game starring Tux, the Linux
penguin.

In "Fish Cascade" you control Tux as he searches for fish to eat. Fish fall
from the top of the screen. These fish have letters on them.  Unforunately
for Tux, eating a fish with a letter on it will cause his stomach to
become ill, so it is up to you to help Tux eat fish!  By typing the
letters, it will cause them to disappear so tux can chow down on the
fish.

In "Comet Zap" you control Tux as he defends the cities from comets.  To
protect a city from a comet, type the letter on the comet and it will
cause Tux to destroy it with a laser! (In case you wondered, Comet Zap
is an adaptation of the *great* math drill game, "Tux, of Math Command").

"Phrase Typing" offers practice typing phrases and sentences, with on-
screen display of accuracy and typing speed.

"Lessons" is an additional typing activity that we have not yet
completed. You will find other menu entries for planned features
that still need to be implemented.

Authors:
--------
    Current maintainer and programming lead:
    David Bruce <davidstuartbruce@gmail.com>

    Jesse Andrews <jdandr2@uky.edu>
    Calvin Arndt <calarndt@tux4kids.org>
    Sam Hart <hart@geekcomix.com>  --- Sam started it all with TuxType 1!!!
    Jacob Greig <bombastic@firstlinux.net>
    Sreyas Kurumanghat <k.sreyas@gmail.com>
    Sreerenj Balachandran <bsreerenj@gmail.com>
    Vimal Ravi <vimal_ravi@rediff.com>
    Prince K. Antony <prince.kantony@gmail.com>
    Mobin Mohan <mobinmohan@gmail.com>


%prep
%setup -q -n %realname-%version

%build
## autoreconf --force --install
%configure --docdir="%{_defaultdocdir}/%{name}" --disable-rpath
make %{?jobs:-j %jobs}

%install
%if 0%{?suse_version} < 1030
for i in $(find . -name Makefile ); do
    sed -i "s#MKDIR_P#mkdir_p#g" $i
done
%endif
make DESTDIR=%{buildroot} install
# remove unneeded data
rm -rf %buildroot/usr/doc/tuxtype
rm -rf %buildroot%_datadir/tuxtype/{autorun.inf,OFL.txt}
# install desktop file and icon
mkdir -p %buildroot%_datadir/pixmaps
convert -scale 48x48 %name.ico %buildroot%_datadir/pixmaps/%name.png
rm -rf %buildroot%_datadir/tuxtype/*.ico
%if 0%{?suse_version}
#install -Dm644 %{SOURCE1} %buildroot%_datadir/applications/%name.desktop
%suse_update_desktop_file -i %name Game KidsGame
# save some discspace using symlinks
%fdupes -s %buildroot
%endif
%if 0%{?fedora_version}
# install desktop file
desktop-file-install --vendor="%{vendor}" \
  --dir=%buildroot/%_datadir/applications \
  %{SOURCE1}
%endif
%if 0%{?mandriva_version}
#desktop-file-install --vendor="%{vendor}" \
#  --dir=%buildroot/%_datadir/applications \
install -Dm644  %{SOURCE1} %buildroot/%_datadir/applications/%name.desktop
%endif
# grmbl....
if [ ! -d %buildroot%{_datadir}/fonts/truetype ]; then
	mkdir -p %buildroot%{_datadir}/fonts/truetype
	ln -s %{_datadir}/tuxtype/fonts %buildroot%{_datadir}/fonts/truetype/ttf-sil-andika
fi
%find_lang %name

%if 0%{?mandriva_version}
%post
%{update_menus}

%postun
%{clean_menus}
%endif

%clean
rm -rf %buildroot

%files -f %name.lang
%defattr(-,root,root)
%doc README AUTHORS COPYING ChangeLog TODO 
# %doc tuxtype/docs/en/*.html
%doc data/sounds/README_SOUNDS.TXT
%doc data/images/README_IMAGES.TXT
%if 0%{?fedora_version}
%dir %_docdir/%{name}
%doc %_docdir/%{name}/*
%endif
%{_bindir}/tuxtype
%dir %_datadir/tuxtype
#%dir %_datadir/tuxtype/fonts
%dir %{_datadir}/fonts/truetype
%dir %{_datadir}/fonts/truetype/ttf-sil-andika
%_datadir/tuxtype/*
%_datadir/applications/*%name.desktop
%_datadir/pixmaps/%name.png

%changelog 
