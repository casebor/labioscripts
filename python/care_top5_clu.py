#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_top5_clu.py
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

import argparse
import numpy as np
from os import path

colors = ['0x000080', '0x1a1aff', '0x00ffff', '0x66ff33', '0xffff00', '0xff8000', '0xff0000', '0xff00ff', '0x800080', '0x000000']

def get_rmsd_color(rmsd):
    """ Returns a rgb color in gnuplot hexadecimal format depending of
	the value of the RMSD.
    """
    if rmsd <= 1.0:
	rgb_color = colors[0]
    elif rmsd > 1.0 and rmsd <= 1.5:
	rgb_color = colors[1]
    elif rmsd > 1.5 and rmsd <= 2.0:
	rgb_color = colors[2]
    elif rmsd > 2.0 and rmsd <= 2.5:
	rgb_color = colors[3]
    elif rmsd > 2.5 and rmsd <= 3.0:
	rgb_color = colors[4]
    elif rmsd > 3.0 and rmsd <= 3.5:
	rgb_color = colors[5]
    elif rmsd > 3.5 and rmsd <= 4.0:
	rgb_color = colors[6]
    elif rmsd > 4.0 and rmsd <= 4.5:
	rgb_color = colors[7]
    elif rmsd > 4.5 and rmsd <= 5.0:
	rgb_color = colors[8]
    else:
	rgb_color = colors[9]
    return rgb_color

def get_gdt_color(gdt):
    """ Returns a rgb color in gnuplot hexadecimal format depending of
	the value of the GDT.
    """
    if gdt > 0.9:
	rgb_color = colors[0]
    elif gdt > 0.8 and gdt <= 0.9:
	rgb_color = colors[1]
    elif gdt > 0.7 and gdt <= 0.8:
	rgb_color = colors[2]
    elif gdt > 0.6 and gdt <= 0.7:
	rgb_color = colors[3]
    elif gdt > 0.5 and gdt <= 0.6:
	rgb_color = colors[4]
    elif gdt > 0.4 and gdt <= 0.5:
	rgb_color = colors[5]
    elif gdt > 0.3 and gdt <= 0.4:
	rgb_color = colors[6]
    elif gdt > 0.2 and gdt <= 0.3:
	rgb_color = colors[7]
    elif gdt > 0.1 and gdt <= 0.2:
	rgb_color = colors[8]
    else:
	rgb_color = colors[9]
    return rgb_color

def main():
    """ Main function """
    if args.rmsd_file is None and args.gdt_file is None:
	print "Error!!!\nYou didn't specified nor a RMSD file nor a GDT file.\nPlease specify only one of them."
	quit()
    if args.rmsd_file is not None and args.gdt_file is not None:
	print "Error!!!\nYou specified both RMSD file and GDT file.\nPlease specify only one of them."
	quit()
    clust_qty = np.zeros((5,), dtype=np.int)
    clust_metric = np.zeros((5,), dtype=np.float32)
    with open(args.infile,'r') as temporal_file:
	clust_file = list(temporal_file)
	if len(clust_file) > 7:
	    for i in range(1,6):
		clust_qty[i-1] = clust_file[i].split()[-1]
	else:
	    for i in range(1,len(clust_file)-1):
		clust_qty[i-1] = clust_file[i].split()[-1]
	total_struc = clust_file[-1].split()[-1]
    if args.rmsd_file is not None:
	out = "#Cluster	Population	RMSD	Total	Color\n"
	with open(args.rmsd_file,'r') as temporal_file:
	    clust_file = list(temporal_file)
	    if len(clust_file) > 6:
		for i in range(1,6):
		    clust_metric[i-1] = clust_file[i].split()[-1]
	    else:
		for i in range(1,len(clust_file)):
		    clust_metric[i-1] = clust_file[i].split()[-1]
	for i in range(5):
	    out += "Cluster_%d	%d	%f	%s	%s\n" %(i+1, clust_qty[i], clust_metric[i], total_struc, get_rmsd_color(clust_metric[i]))
    else:
	out = "#Cluster	Population	GDT	Total	Color\n"
	with open(args.infile,'r') as temporal_file:
	    clust_file = list(temporal_file)
	    if len(clust_file) > 5:
		for i in range(5):
		    clust_metric[i] = clust_file[i].split()[-1]
	    else:
		for i in range(len(clust_file)):
		    clust_metric[i] = clust_file[i].split()[-1]
	for i in range(5):
	    out += "Cluster_%d	%d	%f	%s	%s\n" %(i+1, clust_qty[i], clust_metric[i], total_struc, get_gdt_color(clust_metric[i]))
    args.outfile.write(out)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Obtain the best 5 more populated clusters using RMSD or GDT-TS as additional data.')
    parser.add_argument('-i', '--in', action='store', required=True, dest='infile', help='File containing data of the clusters and population of each.')
    parser.add_argument('-r', '--rmsd', action='store', required=False, dest='rmsd_file', help='File with the RMSD values of each centroid.')
    parser.add_argument('-g', '--gdt', action='store', required=False, dest='gdt_file', help='File with the GDT values of each centroid.')
    parser.add_argument('-o', '--out', action='store', type=argparse.FileType('w'), required=True, dest='outfile', help='Specifies the name for the output file.')
    args = parser.parse_args()
    main()
