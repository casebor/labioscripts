#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_graph_secstruct.py
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
from optparse import OptionParser
from os.path import isfile, basename
from numpy import loadtxt

def error_input():
    print("ERROR in input file")
    parser.print_help()
    quit()

def main():
    with open(options.infile, 'r') as infile:
	residues = infile.readline().split()[1:]
    name_in = basename(options.infile).split('.')[0]
    name_out = basename(options.output).split('.')[0]
    data = loadtxt(options.infile, dtype=int)
    data = data[:,1:].T
    gnufile = """set terminal pngcairo size 2048,1080 enhanced font 'Verdana,15'
set output \""""
    gnufile += name_out + """.png"
set title "Secondary Structure Composition"
unset key
set view map
set tic scale 0
set ytics("""
    for i, res in enumerate(residues):
	gnufile += '"%s" %s, ' %(res, i)
    gnufile = gnufile[:-2] + """)
set cbrange [-0.500:7.500]
#set cbtics 0.000 7.000 1.0
set palette maxcolors 8
set palette defined (0 "#000000", 1 "#0000FF", 4 "#00FF00", 7 "#FF0000")
set cbtics("None" 0.000, "Para" 1.000, "Anti" 2.000, "3-10" 3.000, "Alpha" 4.000, "Pi" 5.000, "Turn" 6.000, "Bend" 7.000)
set xlabel "Frame"
set ylabel ""
"""
    gnufile += 'set yrange [-0.5: %s.5]\n' %(len(residues)-1)
    gnufile += 'set xrange [-0.5: %s.5]\n' %(len(data[0])-1)
    gnufile += 'splot "%s_data.txt" matrix with image' %(name_in)
    with open(name_in + '.gnu', 'w') as gnuin:
	gnuin.write(gnufile)
    dataout = ''
    for row in data:
	for column in row:
	    dataout += '%s ' %(column)
	dataout += '\n'
    with open(name_in + '_data.txt', 'w') as d_out:
	d_out.write(dataout)
    system('gnuplot %s.gnu' %(name_in))
    system('rm %s.gnu %s_data.txt' %(name_in, name_in))
    return 0

if __name__ == '__main__':
    usage = 'usage: \"%prog args\"'
    parser = OptionParser(usage)
    parser.add_option('-i', '--in', action='store', type='string', dest='infile', help='The input data file where the data is.')
    parser.add_option('-o', '--out', action='store', type='string', dest='output', help='Name for the output file. Default is "plot.png".', default='plot')
    (options, args) = parser.parse_args()
    main()
