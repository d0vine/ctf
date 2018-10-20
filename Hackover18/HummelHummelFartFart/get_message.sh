#!/bin/bash
IMGS=`ls -art frames/*.jpg`

for IMG in ${IMGS[@]}; do
    OUT=`python get_symbo.py $IMG 2>/dev/null`
    echo $OUT
done
