#!/bin/bash

#usage: rmsd.sh prote.prmtop reference.inpcrd #mdfile
#          0        1              2             3

model1="parm "
model2="K/"$1"\nreference "$2"\ntrajin "
model3="K/trajec/md-"$3".nc\nrms rmsd-"
model4=" @CA,C,O,N reference out "
model5="K.txt\nrun"

temps=(300 350 400 450)

for i in ${temps[*]};
do
	echo -e $model1$i$model2$i$model3$i$model4$i$model5 > cpp-$i.in
	cpptraj -i cpp-$i.in
done

paste 300K.txt 350K.txt 400K.txt 450K.txt | awk -F " " '{print $1","$2","$4","$6","$8}' > rmsd.txt

