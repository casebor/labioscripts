#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_graph_histograms.py
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

import argparse, numpy as np
from os import system

def main():
    """ Main function
    """
    data = np.loadtxt(args.infile, comments=args.exclude)
    data = data[:,args.column-1]
    data_max = np.max(data)
    factor = (data_max-args.min)/args.bins
    ranges = np.zeros(args.bins, dtype=np.int)
    for d in data:
	pos = int((d-args.min)/factor)
	if d == data_max:
	    pos = -1
	ranges[pos] += 1
    out_str = ''
    for i in range(args.bins):
	out_str += '%.3f-%.3f    %d\n' %(args.min+(i*factor), args.min+(i+1)*factor, ranges[i])
    temp_name = args.outfile.split('.')
    temp_name = '.'.join(temp_name[:-1])
    temp_name = '.'+temp_name
    with open(temp_name, 'w') as temp:
	temp.write(out_str)
    gnu = """set terminal pngcairo size 2048,1080 enhanced font 'Verdana,15'
set output '"""
    gnu += args.outfile + "'\n"
    gnu += """set boxwidth 1.5
set style fill solid 1.00 border lt 0
#set key under
set key off
set style histogram title textcolor lt 0
set style data histograms
set xtics border in scale 0,0 nomirror rotate by -45 autojustify
#set title "GDT Ranges Distribution"
#set yrange [ 0.00 : 100.00 ] noreverse nowriteback
plot """
    gnu += "'%s' using 2:xtic(1)\n" %(temp_name)
    with open(temp_name+'.gnu', 'w') as out:
	out.write(gnu)
    system('gnuplot %s.gnu' %(temp_name))
    system('rm %s %s.gnu' %(temp_name, temp_name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Graphs data into histogram format.')
    parser.add_argument('-m', '--min', required=True, type=float, default=0.00, help='Optional: You can define the minimum value of your data. Default 0.00')
    parser.add_argument('-b', '--bins', required=True, type=int, help='How many bins you want in the histogram.')
    parser.add_argument('-i', '--infile', required=True, help='The file that holds the data.')
    parser.add_argument('-c', '--column', required=False, type=int, default=1, help='The column number where the data to be plotted is. Begins with 1. Default 1.')
    parser.add_argument('-o', '--outfile', default='histogram.png', help='The output name of the file. Default is histogram.png')
    parser.add_argument('-e', '--exclude', required=False, default='#', help='Optional: You can define which lines will be ignored by using a character. Default is #.')
    args = parser.parse_args()
    main()
