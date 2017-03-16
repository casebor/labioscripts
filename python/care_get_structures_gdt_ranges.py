#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_get_structures_gdt_ranges.py
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
from os import path, system

def main():
    """ Main function
    """
    temp_l = path.splitext(args.infile)[0].split('-')
    trat = temp_l[0]
    temp = temp_l[-1]
    with open(args.infile, 'r') as infile:
	data = list(infile)
    for i in range(1, len(data)):
	if 'None' not in data[i]:
	    temp_data = data[i].split()
	    gdt = temp_data[0]
	    frame = int(temp_data[1]) + 1
	    cppout = 'trajout %s-%s-%s-%d.pdb onlyframes %d\ngo\nquit\n' %(trat, temp, gdt, frame, frame)
	    with open('.tempcpp.in', 'w') as tempcpp:
		tempcpp.write(cppout)
	    system('cpptraj -p %s -y %s -i .tempcpp.in' %(args.parmtop, args.trajin))
    system('rm .tempcpp.in')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract the structures in each GDT range. Next step of care_get_structures_list_gdt_ranges.py')
    parser.add_argument('-i', '--in', action='store', required=True, dest='infile', help='The input file with the indices.')
    parser.add_argument('-y', '--trajin', action='store', required=True, help='The trajectory file.')
    parser.add_argument('-p', '--parmtop', action='store', required=True, help='Amber topology file.')
    args = parser.parse_args()
    main()
