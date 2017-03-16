#!/bin/bash
# -*- coding: utf-8 -*-
#
#  care_get_mopac_results.sh
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

usage="$(basename "$0") [-h] [-y trajectory] [-d]

Where:

    -h  show this help text
    -y  Trajectory file in PDB format
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
if [ $flag1 == false ]; then
    echo "$error"
    exit 1
fi

# Generate the pdb's
care_generate_pdbs.py -y $traj &
# In this part the problem with the sleep time depends if you already have the index file or not,
# i'm going to use a until (a negative while loop) loop to ask whenever the index file is been created or not
until [ -f ${traj%.pdb}'_index.txt' ]; do
    sleep 1
done

models=`wc ${traj%.pdb}'_index.txt' | awk '{print $1}'`

for i in `seq 1 $models`;
do
    care_pdb_to_mopac.py -i ${traj%.pdb}'_M'$i'.pdb'
    /opt/mopac/MOPAC2016.exe ${traj%.pdb}'_M'$i'.mop'
    rm ${traj%.pdb}'_M'$i'.pdb' ${traj%.pdb}'_M'$i'.aux' ${traj%.pdb}'_M'$i'.mop' ${traj%.pdb}'_M'$i'.out'
done

care_edit_mopac_results.py -y $traj -m $models

if [ $debug == false ]; then
    rm *.arc
fi

echo "$success"
