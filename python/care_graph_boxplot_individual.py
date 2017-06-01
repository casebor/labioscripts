#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_graph_boxplot_individual.py
#  
#  Copyright 2017 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
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

import argparse, sys, math
import numpy as np
from os import system

def get_min():
    """ Function doc
    """
    min = sys.float_info.max
    for file in args.files:
        tempdata = np.loadtxt(file, usecols=(args.column-1,))
        mintemp = np.amin(tempdata)
        if mintemp < min:
            min = mintemp
    temp = int(min)
    cont = 0
    while (temp-10) > 0:
        cont += 10
        temp = temp - 10
    if int(min) == cont:
        min = cont - 10
    else:
        min = cont
    return min

def get_max():
    """ Function doc
    """
    max = 0.0
    for file in args.files:
        tempdata = np.loadtxt(file, usecols=(args.column-1,))
        maxtemp = np.amax(tempdata)
        if maxtemp > max:
            max = maxtemp
    temp = int(max)
    cont = 10
    while (temp-10) > 0:
        cont += 10
        temp = temp - 10
    if int(max) == cont:
        max = cont + 10
    else:
        max = cont
    return max

def main():
    """ Main function
    """
    gnufile = """set terminal pngcairo size 2048,1080 enhanced font 'Verdana,25'
set output '"""
    gnufile += args.outfile + "'\n"
    gnufile += """set style fill solid 1.00 border lt 0
set key right top vertical Left reverse noenhanced autotitle columnhead nobox
set key samplen 3 spacing 5 width 0 font 'Verdana,20'
set style data boxplot
set xtics nomirror
set ytics nomirror
unset border
set border 1 | 2

set xtics ("""
    for i in range(len(args.files)+1):
        gnufile += "%d, " %(i)
    gnufile += "%d)\n" %(len(args.files)+1)
    gnufile += "set xrange [0:%d]\n" %(len(args.files)+1)
    gnufile += "set yrange [%d:%d]\n\n" %(get_min(), get_max())
    gnufile += "plot '%s' using (1):%d title '%s'" %(args.files[0], args.column, args.files[0].split('.')[0])
    for i in range(1, len(args.files)):
        gnufile += ",\\\n     '%s' using (%i):%d title '%s'" %(args.files[i], i+1, args.column, args.files[i].split('.')[0])
    with open('gnuinput.gpi', 'w') as gnin:
        gnin.write(gnufile)
    system('gnuplot gnuinput.gpi')
    if not args.keep:
        system('rm gnuinput.gpi')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Graphs data distributions in boxplots.")
    parser.add_argument('-f', '--files', action='store', required=True, nargs='+', dest='files', help="The file(s) where the data is. If more than one file is used, separate them with space. Example: File1.txt File2.txt File.txt")
    parser.add_argument('-c', '--col', action='store', required=True, type=int, dest='column', help="The column in the file whe the data to be used is. First column is 1.")
    parser.add_argument('-o', '--out', action='store', required=True, dest='outfile', help="Output name for the graph, you should use the extension .png")
    parser.add_argument('-k', '--keep', action='store_true', dest='keep', help="Flag for keep the temporary files or not. Default is False.")
    args = parser.parse_args()
    main()
