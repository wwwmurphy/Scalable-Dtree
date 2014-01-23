#!/bin/bash

if (( "$#" < 2 )); then
    echo -n `basename $0`
    echo " input-filename output-filename"
    exit
fi

awk ' BEGIN { FS=","; OFS=","; getline; print $0 } { $NF=""; print $0 } ' < $1 > $2

