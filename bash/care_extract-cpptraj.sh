#!/bin/bash
# -*- coding: utf-8 -*-
#
#  care_extract-cpptraj.sh
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


usage="$(basename "$0") [-h] [-p topology] [-y trajectory] [-o output] [-e element]
	   Use this script to take the CL funnel out of the trajectory

Where:

    -h  show this help text
    -p  Amber topology file of the trajectory
    -y  Trajectory file in NETcdf format
    -e  Element of the funnel
    -o  Output file name with extension
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

while getopts ':hp:y:o:e:' option; do
    case "$option" in
	h)  echo "$usage"
	    exit
	    ;;
	p)  parm=$OPTARG
	    if [ -f $parm ]; then
		echo "Topology parameter file  --> "$parm
		flag1=true
	    else
		echo "Topology file -->"$parm"<-- is incorrect or does not exist!!!"
		echo "$usage"
		exit 1
	    fi
	    ;;
	y)  traj=$OPTARG
	    if [ -f $traj ]; then
		echo "Trajectory file selected --> "$traj
		flag2=true
	    else
		echo "Trajectory file -->"$traj"<-- is incorrect or does not exist!!!"
		echo "$usage"
		exit 1
	    fi
	    ;;
	e)  element=$OPTARG
	    echo "The element of the funnel --> "$element
	    ;;
	o)  out=$OPTARG
	    echo "The output name of the file will be --> "$out
	    flag3=true
	    ;;
	:)  printf "Missing argument for -%s\n" "$OPTARG" >&2
	    echo "$usage" >&2
	    exit 1
	    ;;
	\?) printf "Illegal option: -%s\n" "$OPTARG" >&2
	    echo "$usage" >&2
	    exit 1
	    ;;
    esac
done
shift $((OPTIND - 1))

#if [[ $flag1 == true && $flag2 == true ]]; then
if [[ $flag1 == true && $flag2 == true && $flag3 == true ]]; then
    echo "strip :$element
    go" > .temp.in
    #cpptraj -p $parm -y $traj -x ${traj:0:-3}.pdb -i .temp.in
    cpptraj -p $parm -y $traj -x $out -i .temp.in
    rm .temp.in
else
    echo "$error"
    echo "$usage"
    exit 1
fi

echo "$success"
