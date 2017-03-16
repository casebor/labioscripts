#!/bin/bash

treatment=(10ps 20ps 40ps 60ps 80ps 100ps 200ps 300ps 400ps trad_new)
temps=(290.00 316.99 345.76 376.44 409.14 444.04)

for trat in ${treatment[*]}
do
    for temp in ${temps[*]}
    do
	care_cluster_distribution.py -i $trat/$trat-$temp.info -c $trat/$trat-$temp-clusters.clu -o $trat/$trat-$temp.txt
    done
done

for trat in ${treatment[*]}
do
    for temp in ${temps[*]}
    do
	cpptraj -p 1E0Q.prmtop -c 1E0Q.pdb << EOF
trajin $trat/$trat-$temp-centroids.pdb
drmsd :2-16@CA ref 1E0Q.pdb out $trat/rmsd-centroids-$trat-$temp.txt
go
EOF
    done
done

for trat in ${treatment[*]}
do
    for temp in ${temps[*]}
    do
	care_rmsd_ranges.py -i $trat/rmsd-centroids-$trat-$temp.txt -c 2 -o rmsd_ranges_centroids_$trat-$temp.txt
    done
done

for temp in ${temps[*]}
do
    cat rmsd_ranges_centroids_10ps-$temp.txt > rmsd_ranges-$temp.txt
done

for trat in ${treatment[*]}
do
    for temp in ${temps[*]}
    do
	tail -n 1 rmsd_ranges_centroids_$trat-$temp.txt >> rmsd_ranges-$temp.txt
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
	cpptraj -p 1E0Q.prmtop -y $trat/$trat-$temp-centroids.pdb -x $trat-$temp-centroids.pdb
	mv $trat-$temp-centroids.pdb $trat/
    done
done

for trat in ${treatment[*]}
do
    for temp in ${temps[*]}
    do
	clusco_cpu -t $trat/$trat-$temp-centroids.pdb -s gdt -e 1E0Q.pdb -o $trat/gdt-centroids-$trat-$temp.txt
    done
done

for trat in ${treatment[*]}
do
    for temp in ${temps[*]}
    do
	care_gdt_ranges.py -i $trat/gdt-centroids-$trat-$temp.txt -c 3 -o gdt_ranges_centroids_$trat-$temp.txt
    done
done

for temp in ${temps[*]}
do
    cat gdt_ranges_centroids_10ps-$temp.txt > gdt_ranges-$temp.txt
done

for trat in ${treatment[*]}
do
    for temp in ${temps[*]}
    do
	tail -n 1 gdt_ranges_centroids_$trat-$temp.txt >> gdt_ranges-$temp.txt
    done
done

for temp in ${temps[*]}
do
    care_graph_gdt_ranges.py -i gdt_ranges-$temp.txt -o GDT-$temp.png
done

for temp in ${temps[*]}
do
    echo -e "#Treatment\tClusters" > clusters-$temp.txt
done

for trat in ${treatment[*]}
do
    for temp in ${temps[*]}
    do
	clust=`grep "#Clustering:" $trat/$trat-$temp.info | awk '{print $2}'`
	echo -e "$trat\t$clust" >> clusters-$temp.txt
    done
done

echo -e "Treatment\t290.00\t316.99\t345.76\t376.44\t409.14\t444.04" > clusters-total.txt
paste clusters-290.00.txt clusters-316.99.txt clusters-345.76.txt clusters-376.44.txt clusters-409.14.txt clusters-444.04.txt | tail -n 10 | awk '{print $1"\t"$2"\t"$4"\t"$6"\t"$8"\t"$10"\t"$12}' >> clusters-total.txt
transpose=`awk 'BEGIN { FS=OFS="\t" }
{for (rowNr=1;rowNr<=NF;rowNr++){
    cell[rowNr,NR]=$rowNr}
maxRows=(NF>maxRows?NF:maxRows)
maxCols=NR}
END {for (rowNr=1;rowNr<=maxRows;rowNr++){
    for (colNr=1;colNr<=maxCols;colNr++){
	printf "%s%s", cell[rowNr,colNr], (colNr<maxCols?OFS:ORS)}}}' clusters-total.txt`
echo -e "$transpose" > clusters-total.txt

gnuplot <<EOF
set terminal pngcairo size 2048,1080 enhanced font 'Verdana,15'
set output 'clusters-total.png'
set key inside right top vertical Right noreverse noenhanced autotitle nobox
set style data linespoints
set xtics border in scale 1,0.5 nomirror rotate by -45  autojustify
set xtics norangelimit
set xtics ()
set title "Clusters per Treatment"
plot 'clusters-total.txt' using 2:xtic(1) title columnheader(2), for [i=3:12] '' using i title columnheader(i)
EOF
