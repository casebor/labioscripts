#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_graph_gdt_ranges.py
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

import argparse
from os import system
import numpy as np

def edit_input():
    """
    """
    with open(args.infile, 'r') as orig:
	data_list = list(orig)
	ranges = data_list[1].split()[1:]
	pos = 2
	names = []
	while pos<len(data_list):
	    names.append(data_list[pos].split()[0])
	    pos += 1
    data_matrix = np.loadtxt(args.infile, skiprows=2, usecols=range(1,11))
    data_matrix = data_matrix.T
    out_data = '# GDT Proportions\nRanges '
    out_data += ' '.join(names) + '\n'
    for i,ran in enumerate(ranges):
	out_data += ran
	for data in data_matrix[i]:
	    out_data += ' %d' %(data)
	out_data += ' %d\n' %(data_matrix[i].sum())
    with open(args.infile+'.temp', 'w') as temp:
	temp.write(out_data)
    args.infile = args.infile+'.temp'

def main():
    """ Main function """
    if args.transform:
	edit_input()
    with open(args.infile, 'r') as temp:
	temp_list = list(temp)
	limit = len(temp_list[-1].split())
	xtics = []
	for i in range(2, len(temp_list)):
	    xtics.append(temp_list[i].split()[0])
    colors = ['#000000','#800080','#ff00ff','#ff0000','#ff8000','#ffff00','#66ff33','#00ffff','#1a1aff','#000080']
    #colors = ['#a70224','#d9352b','#f17048','#fcad60','#fbdf8c','#fdfcbc','#dbef90','#addb6f','#62ba63','#1a964d','#0b663a']
    if args.rmsd:
	colors.reverse()
    gnu = """set terminal pngcairo size 2048,1080 enhanced font 'Verdana,15'
set output '"""
    gnu += args.outfile + "'\n"
    gnu += """set boxwidth .75 absolute
set style fill solid 1.00 border lt 0
set key outside right top vertical Left reverse noenhanced autotitle columnhead nobox
set key invert samplen 3 spacing 5 width 0 height 2.4
set style histogram rowstacked title textcolor lt 0
set style data histograms
set xtics border in scale 0,0 nomirror rotate by -45 autojustify
"""
    if args.rmsd:
	gnu += 'set title "RMSD Ranges Distribution"\n'
    else:
	gnu += 'set title "GDT Ranges Distribution"\n'
    gnu += """set yrange [ 0.00 : 100.00 ] noreverse nowriteback
"""
    gnu += "set xrange [ -0.75 : %.1f ]\n" %(len(xtics)-0.25)
    gnu += "plot '%s' using (100.*$2/$%d):xtic(1) title column(2) lc rgb '%s',\\" %(args.infile, limit, colors[0])
    for i in range(3, limit-1):
	gnu += "\n     '%s' using (100.*$%d/$%d):xtic(1) title column(%d) lc rgb '%s',\\" %(args.infile, i, limit, i, colors[i-2])
    gnu += "\n     '%s' using (100.*$%d/$%d):xtic(1) title column(%d) lc rgb '%s'\n" %(args.infile, limit-1, limit, limit-1, colors[9])
    with open(args.outfile+'-temp.gnu', 'w') as out:
	out.write(gnu)
    system('gnuplot %s-temp.gnu' %(args.outfile))
    if args.keep:
	system('rm %s-temp.gnu' %(args.outfile))
	if args.transform:
	    system('rm %s' %(args.infile))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates a GNU plot of gdt distribution among ranges. The type of the plot is an stacked histogram.')
    parser.add_argument('-i', '--in', action='store', required=True, dest='infile', help='The input file with the GDT indices grouped.')
    parser.add_argument('-o', '--out', action='store', required=True, default='plot.png' ,dest='outfile', help='Specifies the name for the output file. The default name is plot.')
    parser.add_argument('-r', '--rmsd', action='store_true', help='If the data is from a RMSD measurement use this flag, otherwise do not specify it.')
    parser.add_argument('-k', '--keep', action='store_false', help='Flag for keep the temporary files created for gnuplot. Default is False')
    parser.add_argument('-t', '--transform', action='store_true', required=False, dest='transform', help='Transform the type of graph. Instead of group by treatments, group by ranges.')
    args = parser.parse_args()
    main()
