#!/bin/bash
# -*- coding: utf-8 -*-
#
#  care_metrics.sh
#  
#  Copyright 2016 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

usage="$(basename "$0") [-h] [-y trajectory] [-r reference PDB] [-d]

Where:

    -h  show this help text
    -y  Trajectory file in PDB format
    -r  Reference PDB for the QCS program
    -d  Debugging mode. All the files will be kept. Default is false
    "
error="
    ERROR trying to parse parameters
    (╯°□°）╯︵ ┻━┻
    Did you made a mistake?
          ヽ(#ﾟДﾟ)ﾉ┌┛Σ(ノ´Д\`)ノ
    "
success="
    DONE!!!
    ( •_•)
    ( •_•)>⌐■-■
    (⌐■_■) Yeeeeeaaaahhhh!!!
    "

flag1=false
flag2=false
debug=false
while getopts ':hy:r:d' option; do
    case "$option" in
	h)  echo "$usage"
	    exit
	    ;;
	y)  traj=$OPTARG
	    if [ -f $traj ]; then
		echo "Trajectory file selected --> "$traj
		flag1=true
	    else
		echo "Trajectory file -->"$traj"<-- is incorrect or does not exist!!!"
		echo "$error"
		echo "$usage"
		exit 1
	    fi
	    ;;
	r)  ref=$OPTARG
	    if [ -f $ref ]; then
		echo "Reference file selected --> "$ref
		flag2=true
	    else
		echo "Reference file -->"$ref"<-- is incorrect or does not exist!!!"
		echo "$error"
		echo "$usage"
		exit 1
	    fi
	    ;;
	d)  debug=true
	    echo "Debugging mode activated ƪ(‾_‾)ʃ"
	    ;;
	:)  printf "Missing argument for -%s\n" "$OPTARG" >&2
            echo "$error"
	    echo "$usage" >&2
	    exit 1
	    ;;
	\?) printf "Illegal option: -%s\n" "$OPTARG" >&2
            echo "$error"
	    echo "$usage" >&2
	    exit 1
	    ;;
    esac
done
shift $((OPTIND - 1))

# Make sure that all the files exist!!!
if [[ $flag1 == false || $flag2 == false ]]; then
    echo "$error"
    exit 1
fi

# Create directories for all the analysis
mkdir dope gfactor probscore dfire-ddfire rwplus opus_psp-goap qcs gdt tmscore abs rel

# Name of the reference pdb
ref_pdb=`basename $ref`

# Generate the pdb's
care_generate_pdbs.py -y $traj &
# In this part the problem with the sleep time depends if you already have the index file or not,
# i'm going to use a until (a negative while loop) loop to ask whenever the index file is been created or not
until [ -f ${traj%.pdb}'_index.txt' ]; do
    sleep 1
done

indx_name=`basename $traj`
indx_name=`echo ${traj%.pdb}`
num_pdbs=`wc $indx_name"_index.txt" | awk '{print $1}'`

# Run clusco in background for the gdt score
clusco_cpu -t $traj -s gdt -e $ref -o gdt/gdt_${traj%.pdb}.txt &

# Run the metrics
out_name=${traj%.pdb}
for i in `seq 1 $num_pdbs`
do
    pdb_name=${traj%.pdb}_M$i.pdb
    ################################################################################################
    #                                 CALCULATING DOPE SCORE                                       #
    ################################################################################################
    cd dope
    care_get_dope.py ../$pdb_name | grep 'DOPE score' | awk -F ' ' '{print $4}' >> dope_$out_name.txt
    ################################################################################################
    #                                CALCULATING GFACTOR SCORE                                     #
    ################################################################################################
    cd ../gfactor
    procheck ../$pdb_name 1.5
    grep "Means" ${traj%.pdb}_M$i.sdh | awk -F ' ' '{print $7}' >> gfactor_$out_name.txt
    rm *.ps *.lan *.nb *.new *.out *.pln *.rin *.sco *.sdh *.sum *.log
    ################################################################################################
    #                                  CALCULATING PROBSCORE                                       #
    ################################################################################################
    cd ../probscore
    clash=`phenix.clashscore ../$pdb_name | grep 'clashscore'  | awk -F ' ' '{print $3}'`
    rotal=`phenix.rotalyze   ../$pdb_name | grep "outliers (G" | cut -d " " -f 2 | cut -d % -f 1`
    ramal=`phenix.ramalyze   ../$pdb_name | grep "favored (G"  | cut -d " " -f 2 | cut -d % -f 1`
    care_probityScore.py $clash $rotal $ramal >> probscore_$out_name.txt
    ################################################################################################
    #                            CALCULATING DFIRE AND DDFIRE SCORES                               #
    ################################################################################################
    cd ../dfire-ddfire
    fire=`dDFIRE ../$pdb_name | awk -F ' ' '{print $2" "$3}'`
    echo $fire | awk '{print $1}' >> dfire_$out_name.txt
    echo $fire | awk '{print $2}' >> ddfire_$out_name.txt
    ################################################################################################
    #                                CALCULATING RWPLUS SCORE                                      #
    ################################################################################################
    cd ../rwplus
    if [ $i = 1 ]; then
        ln -s $RWPLUS_DIR/rw.dat rw.dat
        ln -s $RWPLUS_DIR/scb.dat scb.dat
    fi
    calRWplus ../$pdb_name | awk '{print $4}' >> rwplus_$out_name.txt
    ################################################################################################
    #                           PREPARING OPUS_PSP AND GOAP INPUT FILES                            #
    ################################################################################################
    cd ../opus_psp-goap
    if [ $i = 1 ]; then
        ln -s $OPUS_DIR/config.psp config.psp
        ln -s $OPUS_DIR/energy_dir energy_dir
        echo $GOAP_DIR >> goap_input_$out_name.in
    fi
    ln -s ../$pdb_name $pdb_name
    echo $pdb_name >> goap_input_$out_name.in
    echo ../${pdb_name%.pdb}_no_h.pdb >> opus_input_$out_name.in
    ################################################################################################
    #                                CALCULATING QCS SCORE                                         #
    ################################################################################################
    cd ../qcs
    if [ $i = 1 ]; then
        ln -s ../$ref $ref_pdb
        getQCS.py -r $ref_pdb -m ../$pdb_name -new
    else
        getQCS.py -r $ref_pdb -m ../$pdb_name
    fi
    grep "scores_for_model" $ref_pdb'_vs_'$pdb_name.final | awk '{print $9}' >> qcs_$out_name.txt
    rm $ref_pdb'_vs_'$pdb_name $ref_pdb'_vs_'$pdb_name.final
    ################################################################################################
    #                                CALCULATING TM SCORE                                          #
    ################################################################################################
    cd ../tmscore
    if [ $i = 1 ]; then
        ln -s ../$ref $ref_pdb
    fi
    TMscore ../$pdb_name $ref_pdb | grep 'TM-score    =' | awk '{print $3}' >> tmscore_$out_name.txt
    ################################################################################################
    cd ..
    phenix.trim_pdb ${traj%.pdb}_M$i.pdb
done

####################################################################################################
#                                 FORMATTING THE GDT OUPUT FILE                                    #
####################################################################################################
GDTtemp=`cat gdt/gdt_${traj%.pdb}.txt | awk '{print $3}'`
echo "$GDTtemp" > gdt/gdt_${traj%.pdb}.txt
####################################################################################################
#                              CALCULATING OPUS_PSP AND GOAP SCORES                                #
####################################################################################################
cd opus_psp-goap
#opus_psp < opus_input_${traj%.pdb}.in >> opus_psp_$out_name.txt
opus_psp < opus_input_${traj%.pdb}.in | grep "${traj%.pdb}" | awk '{print $2}' > opus_psp_$out_name.txt
#goap < goap_input_${traj%.pdb}.in >> goap_$out_name.txt
goap < goap_input_${traj%.pdb}.in | awk '{print $3}' > goap_$out_name.txt
#rm config.psp energy_dir *.pdb
cd ..

####################################################################################################
#                                     MOVING RESULT FILES                                          #
####################################################################################################
mv dope/*.txt          abs/
mv gfactor/*.txt       abs/
mv probscore/*.txt     abs/
mv dfire-ddfire/*.txt  abs/
mv rwplus/*.txt        abs/
mv opus_psp-goap/*.txt abs/
mv qcs/*.txt           rel/
mv gdt/*.txt           rel/
mv tmscore/*.txt       rel/

####################################################################################################
#                                 CLEANING UP TEMPORARY FILES                                      #
####################################################################################################
if [ $debug == false ]; then
    rm -R dope gfactor probscore dfire-ddfire rwplus opus_psp-goap qcs gdt tmscore *_M*.pdb*
fi

echo "$success"
