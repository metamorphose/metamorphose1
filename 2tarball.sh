#!/bin/bash

# Clean up directory and make tarball for distribution.

VERSION=`cat version`;

cd ..;

rm -f metamorphose1_${VERSION}.tar.gz;

cp -R metamorphose1 metamorphose-${VERSION};

cd metamorphose-${VERSION};

find . -type f -regex ".*\\(pyc\|tmp\|~\)$" -delete;
find . -depth -name "*.svn" -exec rm -fr {} \;

rm -f metamorphose1.spec messages.pot py2exe_setup.py 2*;
rm -fR nsis nbproject freeBSD debian;

cd ..;

tar -pczf metamorphose-${VERSION}.tar.gz metamorphose-${VERSION}
rm -fR metamorphose-${VERSION}
