#!/bin/sh

URL="http://vlsicad.eecs.umich.edu/BK/GSRCbench"
K="HARD SOFT"
N="n10 n30 n50 n100 n200 n300"
F="blocks nets pl"
DATA="./gsrc"

[ -d $DATA ] || mkdir -p $DATA

for k in $K; do
    [ -d "$DATA/$k" ] || mkdir -p "$DATA/$k"
    for n in $N; do
        for f in $F; do
            curl --silent -X GET "$URL/$k/$n.$f" > "$DATA/$k/$n.$f"
        done
    done
done
