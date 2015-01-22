#!/bin/bash

msgfmt='/usr/bin/msgfmt';

for dir in `ls -1`; do
    if [ -d $dir ]
	then
	    $msgfmt -o $dir/LC_MESSAGES/metamorphose.mo $dir/$dir.po;
	    rm -f $dir/*.mo;
    fi
done

