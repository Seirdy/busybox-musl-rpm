Summary: Statically linked binary providing simplified versions of system commands
Name: busybox
Version: 0.51.062801
Release: 3
Copyright: GPL
Group: System Environment/Shells
Source: ftp://oss.lineo.com/busybox/busybox.tar.gz
Patch: busybox-static.patch
Patch1: busybox-anaconda.patch
URL: http://busybox.lineo.com/
BuildRoot: %{_tmppath}/%{name}-root

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
%setup -n busybox -q
%patch -b .static -p1

%build
make
cp busybox busybox-static
make clean

# revert the patch
find . -name "*.static" | while read n; do
    mv $n $(echo $n | sed 's/\.static$//')
done

patch --suffix .anaconda -p1 < $RPM_SOURCE_DIR/busybox-anaconda.patch
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
* Mon Jul  9 2001 Tim Powers <timp@redhat.com>
- don't obsolete sash
- fix URL and spelling in desc. to satisfy rpmlint

* Thu Jul 05 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add missing defattr for anaconda subpackage

* Thu Jun 28 2001 Erik Troan <ewt@redhat.com>
- initial build for Red Hat
