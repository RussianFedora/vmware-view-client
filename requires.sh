#!/bin/sh
rpmbuilddir=~/rpmbuild
spec=${rpmbuilddir}/SPECS/vmware-view-client.spec
sed -i -e '/^Requires:/d' -e '/Autoreq/d' ${spec}
rpmbuild -bs ${spec}
rm -rf ${rpmbuilddir}/build/ /tmp/requires
if [ -z ${1} ]; then
  mock -r fedora-devel-i386 --rebuild ${rpmbuilddir}/SRPMS/vmware-view-client*.src.rpm --resultdir ${rpmbuilddir}/build/
else
  mock -r fedora-${1}-i386 --rebuild ${rpmbuilddir}/SRPMS/vmware-view-client*.src.rpm --resultdir ${rpmbuilddir}/build/
fi
grep "Requires:" ${rpmbuilddir}/build/build.log | sed -e 's/Requires: //g' -e 's/ /\n/g' | tee /tmp/requires
sed -i -e 's/^/Requires: /g' -e 's/libudev.so.0/libudev.so.1/g' /tmp/requires
echo -e "Requires: zenity\nAutoreq: 0" >> /tmp/requires
line=`grep -n "Exclusivearch:" ${spec} | awk -F: '{print($1)}'`
let line+=1
sed -i -e "${line}r /tmp/requires" ${spec}
