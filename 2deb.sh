#!/bin/bash

# Clean up directory and make tarball for distribution.

VERSION=`cat version`;
VERSION="1-$VERSION";

cd ..;

rm -fr build_deb;
mkdir build_deb;

cp -R metamorphose1 build_deb/metamorphose${VERSION};

cd build_deb/metamorphose${VERSION};

find . -type f -regex ".*\\(\.pyc\|tmp\|~\|\.sh\|\.bat\)$" -delete;
find . -depth -name "*.svn" -exec rm -fr {} \;

rm -f metamorphose1.spec messages.pot py2exe_setup.py;
rm -fR nsis nbproject freeBSD;

# don't sign
dpkg-buildpackage -uc -us;
