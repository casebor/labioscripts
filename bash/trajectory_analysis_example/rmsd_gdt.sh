#!/bin/bash

treatment=(10ps 20ps 40ps 60ps 80ps 100ps 200ps 300ps 400ps trad_new)
temps=(290.00 316.99 345.76 376.44 409.14 444.04)

for trat in ${treatment[*]}
do
    for temp in ${temps[*]}
    do
	care_gdt_ranges.py -i $trat/gdt_$trat-$temp.txt -o gdt_ranges_$trat-$temp.txt -c 3
    done
done

for temp in ${temps[*]}
do
    cat gdt_ranges_10ps-$temp.txt > gdt_ranges-$temp.txt
done

for trat in ${treatment[*]}
do
    for temp in ${temps[*]}
    do
	tail -n 1 gdt_ranges_$trat-$temp.txt >> gdt_ranges-$temp.txt
    done
done

for temp in ${temps[*]}
do
    care_graph_gdt_ranges.py -i gdt_ranges-$temp.txt -o GDT-$temp.png
done

for trat in ${treatment[*]}
do
    for temp in ${temps[*]}
    do
	care_rmsd_ranges.py -i $trat/rmsd-$trat-$temp.txt -c 2 -o rmsd_ranges_$trat-$temp.txt
    done
done

for temp in ${temps[*]}
do
    cat rmsd_ranges_10ps-$temp.txt > rmsd_ranges-$temp.txt
done

for trat in ${treatment[*]}
do
    for temp in ${temps[*]}
    do
	tail -n 1 rmsd_ranges_$trat-$temp.txt >> rmsd_ranges-$temp.txt
    done
done

for temp in ${temps[*]}
do
    care_graph_gdt_ranges.py -i rmsd_ranges-$temp.txt -o RMSD-$temp.png -r
done

for trat in ${treatment[*]}
do
    for temp in ${temps[*]}
    do
    	care_get_structures_list_gdt_ranges.py -i $trat/rmsd-$trat-$temp.txt -o $trat-structures-$temp.txt -c 2 -r
    done
    printf "#Temp\t290.00\t#Temp\t316.99\t#Temp\t345.76\t#Temp\t376.44\t#Temp\t409.14\t#Temp\t444.04\n" > $trat-rmsd-structures.txt
    paste $trat-structures-290.00.txt $trat-structures-316.99.txt $trat-structures-345.76.txt $trat-structures-376.44.txt $trat-structures-409.14.txt $trat-structures-444.04.txt >> $trat-rmsd-structures.txt
    
    for temp in ${temps[*]}
    do
    	care_get_structures_list_gdt_ranges.py -i $trat/gdt_$trat-$temp.txt -o $trat-structures-$temp.txt -c 3
    done
    printf "#Temp\t290.00\t#Temp\t316.99\t#Temp\t345.76\t#Temp\t376.44\t#Temp\t409.14\t#Temp\t444.04\n" > $trat-gdt-structures.txt
    paste $trat-structures-290.00.txt $trat-structures-316.99.txt $trat-structures-345.76.txt $trat-structures-376.44.txt $trat-structures-409.14.txt $trat-structures-444.04.txt >> $trat-gdt-structures.txt
    
    rm $trat-structures-290.00.txt $trat-structures-316.99.txt $trat-structures-345.76.txt $trat-structures-376.44.txt $trat-structures-409.14.txt $trat-structures-444.04.txt
	
done
