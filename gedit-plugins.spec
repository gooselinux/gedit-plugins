Name:           gedit-plugins
Version:        2.28.0
Release:        2%{?dist}
Summary:        Plugins for gedit

Group:          Applications/Editors
License:        GPLv2+
URL:            http://live.gnome.org/GeditPlugins
Source0:        ftp://ftp.gnome.org/pub/gnome/sources/gedit-plugins/2.28/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gedit-devel
BuildRequires:  gucharmap-devel
BuildRequires:  gnome-doc-utils
BuildRequires:  perl(XML::Parser)
BuildRequires:  gettext
BuildRequires:  vte-devel
BuildRequires:  cairo-devel
BuildRequires:  atk-devel
BuildRequires:  pygtk2-devel
BuildRequires:  pygtksourceview-devel
BuildRequires:  pygobject2-devel
BuildRequires:  intltool
Requires:       gedit
Requires:       pygtk2
Requires:       pygtksourceview
Requires:       pygobject2
Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2


%description
A collection of plugins for gedit.


%prep
%setup -q
grep '"import vte' configure && sed \
    -i "s!import vte!import imp; imp.find_module('vte')!" configure

%build
%configure --disable-schemas-install --enable-python
#--with-plugins=bracketcompletion,charmap,codecomment,colorpicker,drawspaces,joinlines,showtabbar,smartspaces,terminal,bookmarks
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}
find $RPM_BUILD_ROOT/%{_libdir}/gedit-2/plugins -name "*.la" -exec rm {} \;


%clean
rm -rf $RPM_BUILD_ROOT


%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gedit-show-tabbar-plugin.schemas >/dev/null || :
fi


%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
  %{_sysconfdir}/gconf/schemas/gedit-show-tabbar-plugin.schemas > /dev/null || :



%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gedit-show-tabbar-plugin.schemas > /dev/null || :
fi

%check
[ -f ${RPM_BUILD_ROOT}%{_libdir}/gedit-2/plugins/terminal.py ]


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README NEWS AUTHORS COPYING
%config(noreplace) %{_sysconfdir}/gconf/schemas/*.schemas
%{_libdir}/gedit-2/plugins/*
%{_datadir}/gedit-2/plugins/*


%changelog
* Fri Jan 29 2010 Ray Strode <rstrode@redhat.com> 2.28.0-2
Resolves: #559982
- Fix up spec file Source URL

* Mon Nov 09 2009 Rakesh Pandit <rakesh@fedoraproject.org> 2.28.0-1
- Updated to 2.28.0

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.26.1-3
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 11 2009 Dodji Seketeli <dodji@redhat.org> - 2.26.1-1
- Update to upstream release 2..26.1
- Fixes GNOME bugzilla bug #576766 - Crash when Configuring "Draw Spaces"
- Make sure to remove all *.la files
- Remove BuildRequire libgnomeui-devel as needless now

* Fri Apr 10 2009 Dodji Seketeli <dodji@redhat.org> - 2.26.0-1
- Update to upstream release (2.26.1)
- Add plugin files from %%{_datadir}
- Don't check for vte anymore, the package checks it pkg-config
- Add 'bookmarks' to the plugin set

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.22.3-3
- Rebuild for Python 2.6

* Mon Sep 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 2.22.3-2
- Fixed buildrequires

* Mon Sep 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 2.22.3-1
- Updated to 2.22.3

* Mon Sep 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 2.22.0-2
- rebuild to pick latest gucharmap

* Tue Mar 18 2008 Trond Danielsen <trond.danielsen@gmail.com> - 2.22.0-1
- Updated.

* Mon Apr 30 2007 Trond Danielsen <trond.danielsen@gmail.com> - 2.18.0-2
- Disable buggy session saver plugin.
- Removed static libraries.

* Sun Apr 01 2007 Trond Danielsen <trond.danielsen@gmail.com> - 2.18.0-1
- Initial version.
