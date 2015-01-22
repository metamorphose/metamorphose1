#!/bin/bash

# Clean up directory and publish to Ubuntu ppa.
#
#

VERSION=`cat src/version`;
FULL_VERSION="1_${VERSION}";
SERIES='hardy jaunty karmic lucid';
REVISION=1;

function create_and_upload {
    cd ..;

    rm -fr build_deb;
    mkdir build_deb;

    cp -R metamorphose1 build_deb/metamorphose${FULL_VERSION};

    cd build_deb/metamorphose${FULL_VERSION};

    sed -i "s/${VERSION}-${REVISION}/${VERSION}-${REVISION}~${1}/" debian/changelog
    sed -i "s/unstable;/${1};/" debian/changelog

    find . -type f -regex ".*\\(\.pyc\|tmp\|~\|\.sh\|\.bat\)$" -delete;
    find . -depth -name "*.svn" -exec rm -fr {} \;

    rm -f metamorphose1.spec messages.pot py2exe_setup.py;
    rm -fR nsis nbproject freeBSD;

    # sign
    dpkg-buildpackage -S; #-us -uc;

    cd ..;

    echo;
    CHANGES=metamorphose${FULL_VERSION}-"$REVISION"~"$1"_source.changes;
    cat $CHANGES | grep urgency;
    
    #dput ppa:ianare/ppa $CHANGES;
}

for series in $SERIES;
do
    create_and_upload ${series};
done;
