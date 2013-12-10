%global debug_package %{nil}

Name:           vmware-view-client
Version:        2.1.0
Release:        5%{?dist}
Summary:        VMware view client

License:        Proprietary
URL:            http://vmware.com/
Source0:        vmware-view-client_2.1.0.orig.tar.gz
Source1:        vmware-view-client.png
Source2:        vmware-view.desktop
Source3:        vmware-view-wrapper
Source4:        tmpfiles.conf
Source5:        vmware-view-usbd-wrapper
Source6:        vmware-view-usbd.service

Exclusivearch:  %{ix86}

Requires: zenity

BuildRequires: desktop-file-utils systemd

%description
VMware view client for fedora

%prep
%setup -q

# Fix view license
%if 0%{?fedora} <= 19
  sed -i -e 's!@DOCDIR@!%{_datadir}/doc/vmware-view-client-%{version}!g' %{SOURCE3}
%else
  sed -i -e 's!@DOCDIR@!%{_datadir}/doc/vmware-view-client!g' %{SOURCE3}
%endif

# Fix exec
sed -i -e 's!@LIBDIR@!%{_libdir}!g' %{SOURCE3} %{SOURCE5} %{SOURCE6}

%build

%install
for FILE in $(find -type f); do
  install -p -D ${FILE} %{buildroot}/${FILE}
done
rm -rf %{buildroot}%{_datadir}/doc
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
install -p -D -m0644 %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
install -p -m0755 %{SOURCE3} %{buildroot}%{_bindir}/

# set up vmware-view-usbd
chmod +s %{buildroot}%{_libdir}/vmware/vmware-{usbarbitrator,view-usbd}
install -p -D -m0755 %{SOURCE5} %{buildroot}%{_libdir}/vmware/
install -p -D -m0644 %{SOURCE6} %{buildroot}%{_unitdir}/vmware-view-usbd.service
ln -s %{_libdir}/libudev.so.1 %{buildroot}%{_libdir}/vmware/libudev.so.0

# this needs to be writeable for USB redirection
install -d -m0755 %{buildroot}%{_localstatedir}/run/vmware
install -p -D -m0644 %{SOURCE4} %{buildroot}%{_prefix}/lib/tmpfiles.d/vmware-view-client.conf

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install %{SOURCE2}

%find_lang vmware-view

rm -f %{buildroot}/find-requires

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/vmware-view.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
%systemd_post vmware-view-usbd.service

%preun
%systemd_preun vmware-view-usbd.service

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
%systemd_postun_with_restart vmware-view-usbd.service

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f vmware-view.lang
%doc usr/share/doc/vmware-view-client/*
%{_bindir}/vmware-*
%{_libdir}/vmware/
%{_libdir}/libpcoip*
%{_libdir}/pcoip/
%{_datadir}/applications/vmware-view.desktop
%{_datadir}/icons/hicolor/48x48/apps/vmware-view-client.png
%{_prefix}/lib/tmpfiles.d/vmware-view-client.conf
%{_localstatedir}/run/vmware
%{_unitdir}/vmware-view-usbd.service

%changelog
* Tue Dec 10 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.1.0-5
- use VMware instead of VmWare

* Tue Dec 10 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.1.0-4
- Fix doc, drop unneded req

* Tue Dec 10 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.1.0-3
- mega-update #2

* Mon Dec 09 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.1.0-2
- mega-update spec

* Mon Dec  2 2013 Vasiliy N. Glazov <vascom2@gmail.com> - 2.1.0
- Initial release
