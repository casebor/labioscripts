#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_get_structures_list_gdt_ranges.py
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
import numpy as np

def main():
    """ Main function
    """
    indexes = [None]*10
    if args.rmsd:
	rmsd_data = np.loadtxt(args.infile, usecols=(args.column-1,), skiprows=1)
	for i,rmsd in enumerate(rmsd_data):
	    if rmsd<=1.0:
		if indexes[0] is None:
		    indexes[0] = i
		elif rmsd<rmsd_data[indexes[0]]:
		    indexes[0] = i
	    if rmsd>1.0 and rmsd<=1.5:
		if indexes[1] is None:
		    indexes[1] = i
		elif rmsd<rmsd_data[indexes[1]]:
		    indexes[1] = i
	    if rmsd>1.5 and rmsd<=2.0:
		if indexes[2] is None:
		    indexes[2] = i
		elif rmsd<rmsd_data[indexes[2]]:
		    indexes[2] = i
	    if rmsd>2.0 and rmsd<=2.5:
		if indexes[3] is None:
		    indexes[3] = i
		elif rmsd<rmsd_data[indexes[3]]:
		    indexes[3] = i
	    if rmsd>2.5 and rmsd<=3.0:
		if indexes[4] is None:
		    indexes[4] = i
		elif rmsd<rmsd_data[indexes[4]]:
		    indexes[4] = i
	    if rmsd>3.0 and rmsd<=3.5:
		if indexes[5] is None:
		    indexes[5] = i
		elif rmsd<rmsd_data[indexes[5]]:
		    indexes[5] = i
	    if rmsd>3.5 and rmsd<=4.0:
		if indexes[6] is None:
		    indexes[6] = i
		elif rmsd<rmsd_data[indexes[6]]:
		    indexes[6] = i
	    if rmsd>4.0 and rmsd<=4.5:
		if indexes[7] is None:
		    indexes[7] = i
		elif rmsd<rmsd_data[indexes[7]]:
		    indexes[7] = i
	    if rmsd>4.5 and rmsd<=5.0:
		if indexes[8] is None:
		    indexes[8] = i
		elif rmsd<rmsd_data[indexes[8]]:
		    indexes[8] = i
	    if rmsd>5.0:
		if indexes[9] is None:
		    indexes[9] = i
		elif rmsd<rmsd_data[indexes[9]]:
		    indexes[9] = i
	out_data = '#RMSD	Frame\n'
    else:
	gdt_data = np.loadtxt(args.infile, usecols=(args.column-1,))
	for i,gdt in enumerate(gdt_data):
	    if gdt<0.1:
		if indexes[0] is None:
		    indexes[0] = i
		elif gdt>gdt_data[indexes[0]]:
		    indexes[0] = i
	    if gdt>=0.1 and gdt<0.2:
		if indexes[1] is None:
		    indexes[1] = i
		elif gdt>gdt_data[indexes[1]]:
		    indexes[1] = i
	    if gdt>=0.2 and gdt<0.3:
		if indexes[2] is None:
		    indexes[2] = i
		elif gdt>gdt_data[indexes[2]]:
		    indexes[2] = i
	    if gdt>=0.3 and gdt<0.4:
		if indexes[3] is None:
		    indexes[3] = i
		elif gdt>gdt_data[indexes[3]]:
		    indexes[3] = i
	    if gdt>=0.4 and gdt<0.5:
		if indexes[4] is None:
		    indexes[4] = i
		elif gdt>gdt_data[indexes[4]]:
		    indexes[4] = i
	    if gdt>=0.5 and gdt<0.6:
		if indexes[5] is None:
		    indexes[5] = i
		elif gdt>gdt_data[indexes[5]]:
		    indexes[5] = i
	    if gdt>=0.6 and gdt<0.7:
		if indexes[6] is None:
		    indexes[6] = i
		elif gdt>gdt_data[indexes[6]]:
		    indexes[6] = i
	    if gdt>=0.7 and gdt<0.8:
		if indexes[7] is None:
		    indexes[7] = i
		elif gdt>gdt_data[indexes[7]]:
		    indexes[7] = i
	    if gdt>=0.8 and gdt<0.9:
		if indexes[8] is None:
		    indexes[8] = i
		elif gdt>gdt_data[indexes[8]]:
		    indexes[8] = i
	    if gdt>=0.9 or gdt>=1.0:
		if indexes[9] is None:
		    indexes[9] = i
		elif gdt>gdt_data[indexes[9]]:
		    indexes[9] = i
	out_data = '#GDT_TS	Frame\n'
    for i in indexes:
	if i is None:
	    out_data += 'None	None\n'
	else:
	    if args.rmsd:
		out_data += '%s	%d\n' %(rmsd_data[i], i+1)
	    else:
		out_data += '%s	%d\n' %(gdt_data[i], i)
    args.outfile.write(out_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract the position of a structure in each GDT or RMSD range. Keep in mind that the frame enumeration begins in 0 as the first structure for GDT and in 1 for RMSD.')
    parser.add_argument('-i', '--in', action='store', required=True, dest='infile', help='The input file with the GDT indices.')
    parser.add_argument('-o', '--out', action='store', type=argparse.FileType('w'), required=True, dest='outfile', help='Output file. The number of the frame will be next to the GDT value for the structure.')
    parser.add_argument('-c', '--col', action='store', type=int, required=False, default=1, dest='column', help='The column where is the GDT data. Begin with 1.')
    parser.add_argument('-r', '--rmsd', action='store_true', help='If the data is from a RMSD measurement use this flag, otherwise do not specify it.')
    args = parser.parse_args()
    main()
