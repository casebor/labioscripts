#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_gdt_ranges.py
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
from os import path

def main():
    """ Main function """
    data = np.loadtxt(args.infile, usecols=(args.column-1,))
    gdts = np.zeros(10)
    if data.size == 1:
	value = float(data)
	index = int(value*10)
	if index == 10:
	    index = 9
	gdts[index] += 1
    else:
	for value in data:
	    index = int(value*10)
	    if index == 10:
		index = 9
	    gdts[index] += 1
    gdts_inv = np.flipud(gdts)
    out = '# GDT range quantity\n'
    out +=  'Treatment X>0.9 X>0.8 X>0.7 X>0.6 X>0.5 X>0.4 X>0.3 X>0.2 X>0.1 X<=0.1\n'
    #out +=  'Treatment 0.9<Y<=1.0 0.8<Y<=0.9 0.7<Y<=0.8 0.6<Y<=0.7 0.5<Y<=0.6 0.4<Y<=0.5 0.3<Y<=0.4 0.2<Y<=0.3 0.1<Y<=0.2 Y<=0.1\n'
    #out +=  'Treatment Y<=0.1 0.1<Y<=0.2 0.2<Y<=0.3 0.3<Y<=0.4 0.4<Y<=0.5 0.5<Y<=0.6 0.6<Y<=0.7 0.7<Y<=0.8 0.8<Y<=0.9 0.9<Y<=1.0\n'
    #out +=  '%s ' %(path.splitext(args.infile)[0])
    out +=  '%s ' %('.'.join((path.basename(args.infile)).split('.')[:-1]))
    for value in gdts_inv:
	out += '%d ' %(value)
    out += '%d\n' %(gdts_inv.sum())
    args.outfile.write(out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Divide results of GDT indices into 10 ranges.')
    parser.add_argument('-i', '--in', action='store', required=True, dest='infile', help='The input file with the GDT indices.')
    parser.add_argument('-o', '--out', action='store', type=argparse.FileType('w'), required=True, dest='outfile', help='Specifies the name for the output file.')
    parser.add_argument('-c', '--col', action='store', type=int, required=False, default=1, dest='column', help='The column where is the GDT data. Begin with 1.')
    args = parser.parse_args()
    main()
