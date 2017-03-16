#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_graph_gdt.py
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

from os import system
from os.path import isfile, basename
from optparse import OptionParser

def error_input():
    print("ERROR in input file(s)")
    quit()

def get_x_vals(filename):
    with open(filename, 'r') as arq:
	numx = len(list(arq))
    return str(numx)

def main():
    
    gnufile = """set term pdf enhanced color dashed font "Times-Roman, 13"
set style line 90 lt 1 lc 3
set style line 90 lt rgb "#808080"
set style line 81 lt 0
set style line 81 lt rgb "#808080"
set grid back linestyle 81
set border 3 linestyle 90
set output \""""
    
    # Check that all the files exist
    if not len(options.infiles)==0:
	files = options.infiles.split(',')
	for f in files:
	    if not isfile(f):
		error_input()
    else:
	error_input()
    
    # Select the colors for the files
    colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
    if len(files) > 12:
	colors = []
    
    gnufile += options.output + '.pdf"\n'
    xvals = get_x_vals(files[0])
    gnufile += 'set xrange [ 0 : ' + xvals + ' ] noreverse nowriteback\n'
    gnufile += 'set yrange [ 0 : 1 ] noreverse nowriteback\n'
    gnufile += 'set xtics font ", 6"\n'
    gnufile += 'set ytics font ", 8"\n'
    gnufile += 'set border 2 front linewidth 1.000\n'
    gnufile += 'set xtics  norangelimit nomirror\n'
    gnufile += 'set ytics border in scale 1,0.5 nomirror norotate  autojustify\n'
    gnufile += 'set style fill solid 0.45 border\n'
    gnufile += 'set xlabel "Time (ps)"\n'
    gnufile += 'set ylabel "GDT"\n'
    gnufile += 'set key box\n'
    gnufile += 'set key horizontal reverse samplen 2 width -2 maxrows 2 maxcols 12  font ", 8"\n'
    gnufile += 'set key horizontal center bottom outside\n'
    gnufile += 'set title "GDT SCORE"\n'
    
    # Create the line styles
    for i in range(len(files)):
	gnufile += 'set style line ' + str(i+1) + ' lt 1 lw 1 ps 0.225 linecolor rgb "' + colors[i] + '"\n'
    
    # Plot the data
    if options.smooth:
	gnufile += 'plot "' + files[0] + '" using:3 with lines ls 1 title "' + basename(files[0]).split('.')[0] + '" smooth bezier'
    else:
	gnufile += 'plot "' + files[0] + '" using:3 with lines ls 1 title "' + basename(files[0]).split('.')[0] + '" '
    for i in range(1, len(files)):
	if options.smooth:
	    gnufile += ', "' + files[i] + '" using:3 with lines ls ' + str(i+1) + ' title "' + basename(files[i]).split('.')[0] + '" smooth bezier'
	else:
	    gnufile += ', "' + files[i] + '" using:3 with lines ls ' + str(i+1) + ' title "' + basename(files[i]).split('.')[0] + '" '
    gnufile += '\n'
    
    # Create a temporary file, run gnuplot and erase the temporary file
    with open('.tempgnu.ini', 'w') as arq:
	arq.write(gnufile)
    system('gnuplot .tempgnu.ini')
    system('rm .tempgnu.ini')
    
    return 0

if __name__ == '__main__':
    usage = 'usage: \"%prog args\"'
    parser = OptionParser(usage)
    parser.add_option('-i', '--in', action='store', type='string', dest='infiles', help='The input data file(s) where the data is. If you use more than one file, please write them comma separated without spaces.\t\tFile1.txt,File2.txt,File3.txt\t\t\tIMPORTANT!!! --> I will assume all the files have the same number of data.')
    parser.add_option('-o', '--out', action='store', type='string', dest='output', help='Name for the output file. Default is "plot".', default='plot')
    parser.add_option('-s', '--smooth', action='store_true', dest='smooth', help='If you want a Smooth Bezier curve add this flag. Default is False.', default=False)
    (options, args) = parser.parse_args()
    main()
