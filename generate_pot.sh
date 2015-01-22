#!/bin/bash

# grabs all translatable strings in python files

FILES=''

for file in `find . -name "*.py"`; do
    FILES="$FILES ${file:2}";
done

pygettext -a $FILES
