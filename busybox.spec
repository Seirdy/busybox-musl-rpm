%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%define WITH_SELINUX 1
%endif
Summary: Statically linked binary providing simplified versions of system commands
Name: busybox
Version: 1.00.rc1
Release: 2
License: GPL
Group: System Environment/Shells
Source: http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
Patch: busybox-static.patch
Patch1: busybox-anaconda.patch
Patch2: busybox-selinux.patch
URL: http://www.busybox.net
BuildRoot: %{_tmppath}/%{name}-root
%if %{WITH_SELINUX}
BuildRequires: libselinux-devel
%endif

%package anaconda
Group: System Environment/Shells
Summary: Version of busybox configured for use with anaconda

%description 
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries.

%description anaconda
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  The version contained in this
package is designed for use with the Red Hat installation program,
anaconda. The busybox package provides a binary better suited to
normal use.

%prep
%setup -q
cp sysdeps/linux/defconfig .config
#SELINUX Patch
%if %{WITH_SELINUX}
%patch2 -b .selinux -p1
%endif
%patch -b .static -p1
#%patch1 -b .anaconda -p1

%build
make defconfig
make
cp busybox busybox-static
make clean

# revert the patch
find . -name "*.static" | while read n; do
    mv $n $(echo $n | sed 's/\.static$//')
done

patch -b --suffix .anaconda -p1 < %{PATCH1}
make DOLFS=y defconfig
make 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -s -m 755 busybox-static $RPM_BUILD_ROOT/sbin/busybox
install -s -m 755 busybox $RPM_BUILD_ROOT/sbin/busybox.anaconda
install -m 644 docs/BusyBox.1 $RPM_BUILD_ROOT/%{_mandir}/man1/busybox.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/sbin/busybox
%{_mandir}/man1/busybox*

%files anaconda
%defattr(-,root,root)
/sbin/busybox.anaconda

%changelog
* Wed Aug 25 2004 Jeremy Katz <katzj@redhat.com> - 1.00.rc1-2
- rebuild

* Fri Jun 25 2004 Dan Walsh <dwalsh@redhat.com> 1.00-pre10.1
- Add BuildRequires libselinux-devel
- Update to latest from upstream

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 11 2004 Karsten Hopp <karsten@redhat.de> 1.00.pre8-4 
- add mknod to busybox-anaconda

* Wed Apr 21 2004 Karsten Hopp <karsten@redhat.de> 1.00.pre8-3 
- fix LS_COLOR in anaconda patch

* Tue Mar 23 2004 Jeremy Katz <katzj@redhat.com> 1.00.pre8-2
- add awk to busybox-anaconda

* Sat Mar 20 2004 Dan Walsh <dwalsh@redhat.com> 1.00-pre8.1
- Update with latest patch. 
- Turn off LS_COLOR in static patch

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Dan Walsh <dwalsh@redhat.com> 1.00-pre5.2
- Fix is_selinux_enabled calls

* Mon Dec 29 2003 Dan Walsh <dwalsh@redhat.com> 1.00-pre5.1
-Latest update

* Wed Nov 26 2003 Dan Walsh <dwalsh@redhat.com> 1.00-pre3.2
- Add insmod

* Mon Sep 15 2003 Dan Walsh <dwalsh@redhat.com> 1.00-pre3.1
- Upgrade to pre3

* Thu Sep 11 2003 Dan Walsh <dwalsh@redhat.com> 1.00.2
- Upgrade selinux support

* Wed Jul 23 2003 Dan Walsh <dwalsh@redhat.com> 1.00.1
- Upgrade to 1.00 package

* Wed Jul 16 2003 Elliot Lee <sopwith@redhat.com> 0.60.5-10
- Rebuild

* Mon Jul 14 2003 Jeremy Katz <katzj@redhat.com> 0.60.5-9
- rebuild

* Mon Jul 14 2003 Jeremy Katz <katzj@redhat.com> 0.60.5-8
- add dmesg to busybox-anaconda

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Jeremy Katz <katzj@redhat.com> 0.60.5-5
- lost nolock for anaconda mount when rediffing, it returns (#81764)

* Mon Jan 6 2003 Dan Walsh <dwalsh@redhat.com> 0.60.5-4
- Upstream developers wanted to eliminate the use of floats

* Thu Jan 3 2003 Dan Walsh <dwalsh@redhat.com> 0.60.5-3
- Fix free to work on large memory machines.

* Sat Dec 28 2002 Jeremy Katz <katzj@redhat.com> 0.60.5-2
- update Config.h for anaconda build to include more useful utils

* Thu Dec 19 2002 Dan Walsh <dwalsh@redhat.com> 0.60.5-1
- update latest release

* Thu Dec 19 2002 Dan Walsh <dwalsh@redhat.com> 0.60.2-8
- incorporate hammer changes

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 06 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix compilation on mainframe

* Tue Apr  2 2002 Jeremy Katz <katzj@redhat.com>
- fix static busybox (#60701)

* Thu Feb 28 2002 Jeremy Katz <katzj@redhat.com>
- don't include mknod in busybox.anaconda so we get collage mknod

* Fri Feb 22 2002 Jeremy Katz <katzj@redhat.com>
- rebuild in new environment

* Wed Jan 30 2002 Jeremy Katz <katzj@redhat.com>
- update to 0.60.2
- include more pieces for the anaconda version so that collage can go away
- make the mount in busybox.anaconda default to -onolock

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
`- automated rebuild

* Mon Jul  9 2001 Tim Powers <timp@redhat.com>
- don't obsolete sash
- fix URL and spelling in desc. to satisfy rpmlint

* Thu Jul 05 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add missing defattr for anaconda subpackage

* Thu Jun 28 2001 Erik Troan <ewt@redhat.com>
- initial build for Red Hat
