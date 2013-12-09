%global debug_package %{nil}

Name:           vmware-view-client
Version:        2.1.0
Release:        2%{?dist}
Summary:        VmWare view client

License:        Proprietary
URL:            http://www2.fedoraforum.org/showthread.php?p=1664816
Source0:        vmware-view-client_2.1.0.orig.tar.gz
Source1:        vmware-view-client_2.1.0-0ubuntu0.13.10.debian.tar.gz
Source2:        vmware-view.desktop
Source3:        requires.sh

Exclusivearch:  %{ix86}

Requires: /bin/bash
Requires: /bin/sh
Requires: ld-linux.so.2
Requires: libX11.so.6
Requires: libXcursor.so.1
Requires: libXext.so.6
Requires: libXfixes.so.3
Requires: libXi.so.6
Requires: libXinerama.so.1
Requires: libXrender.so.1
Requires: libXtst.so.6
Requires: libatk-1.0.so.0
Requires: libc.so.6
Requires: libc.so.6(GLIBC_2.0)
Requires: libc.so.6(GLIBC_2.1)
Requires: libc.so.6(GLIBC_2.1.1)
Requires: libc.so.6(GLIBC_2.1.2)
Requires: libc.so.6(GLIBC_2.1.3)
Requires: libc.so.6(GLIBC_2.2)
Requires: libc.so.6(GLIBC_2.2.4)
Requires: libc.so.6(GLIBC_2.3)
Requires: libc.so.6(GLIBC_2.3.4)
Requires: libc.so.6(GLIBC_2.4)
Requires: libcairo.so.2
Requires: libcrypto.so.0.9.8
Requires: libdl.so.2
Requires: libdl.so.2(GLIBC_2.0)
Requires: libdl.so.2(GLIBC_2.1)
Requires: libgcc_s.so.1
Requires: libgcc_s.so.1(GCC_3.0)
Requires: libgcc_s.so.1(GCC_3.3)
Requires: libgcc_s.so.1(GLIBC_2.0)
Requires: libgdk-x11-2.0.so.0
Requires: libgdk_pixbuf-2.0.so.0
Requires: libgio-2.0.so.0
Requires: libglib-2.0.so.0
Requires: libgmodule-2.0.so.0
Requires: libgobject-2.0.so.0
Requires: libgthread-2.0.so.0
Requires: libgtk-x11-2.0.so.0
Requires: libm.so.6
Requires: libm.so.6(GLIBC_2.0)
Requires: libpango-1.0.so.0
Requires: libpangocairo-1.0.so.0
Requires: libpcsclite.so.1
Requires: libpixman-1.so.0
Requires: libpng12.so.0
Requires: libpthread.so.0
Requires: libpthread.so.0(GLIBC_2.0)
Requires: libpthread.so.0(GLIBC_2.1)
Requires: libpthread.so.0(GLIBC_2.2)
Requires: libpthread.so.0(GLIBC_2.3.2)
Requires: librt.so.1
Requires: librt.so.1(GLIBC_2.2)
Requires: libssl.so.0.9.8
Requires: libstdc++.so.6
Requires: libstdc++.so.6(CXXABI_1.3)
Requires: libstdc++.so.6(CXXABI_1.3.1)
Requires: libstdc++.so.6(GLIBCXX_3.4)
Requires: libudev.so.1
Requires: libuuid.so.1
Requires: libxml2.so.2
Requires: libz.so.1
Requires: rtld(GNU_HASH)
Requires: zenity
Autoreq: 0

BuildRequires: desktop-file-utils

%description
VmWare view client for fedora

%prep
%setup -q
tar --atime-preserve -xvzf %{SOURCE1}

%build

%install
mkdir -p %{buildroot}%{_prefix}/
cp -pR usr/* %{buildroot}%{_prefix}/
rm -rf %{buildroot}%{_prefix}/doc

mkdir -p %{buildroot}%{_datadir}/pixmaps/
install -p -m0644 debian/vmware-view-client-vmware.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

%if 0%{?fedora} <= 19
  sed -i -e '/--filename=/s!=.*$!=%{_datadir}/doc/vmware-view-client/VMware-Horizon-View-Client-EULA-en.txt!g' debian/vmware-view.wrapper
%else
  sed -i -e '/--filename=/s!=.*$!=%{_datadir}/doc/vmware-view-client-%{version}/VMware-Horizon-View-Client-EULA-en.txt!g' debian/vmware-view.wrapper
%endif
install -p -m0755 debian/vmware-view.wrapper %{buildroot}%{_bindir}/vmware-view-wrapper

mkdir -p %{buildroot}/%{_datadir}/applications/
desktop-file-install %{SOURCE2}

%find_lang vmware-view

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/vmware-view.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f vmware-view.lang
%doc usr/share/doc/*
%{_bindir}/vmware-*
%{_libdir}/*
%{_datadir}/applications/vmware-view.desktop
%{_datadir}/pixmaps/vmware-view-client.png

%changelog
* Mon Dec 09 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.1.0-2
- mega-update spec

* Mon Dec  2 2013 Vasiliy N. Glazov <vascom2@gmail.com> - 2.1.0
- Initial release
