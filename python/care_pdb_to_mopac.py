#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_pdb_to_mopac.py
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

def create_mop_file(charge):
    """ Function doc
    """
    string  = ''
    string += '* ===============================\n'       
    string += '* Input file for Mopac\n'
    string += '* ===============================\n'
    string += "PM3 CHARGE=" + str(charge) + " Singlet AUX 1SCF MOZYME"
    string += '\n\n'
    string += 'Mopac file generated by trajectoryEnergy\n'
    for line in open(args.infile, 'r'):
	type_a  = line[0:6]
	x       = line[31:37]
	y       = line[39:45]
	z       = line[47:53]
	atom    = line[77:78]
	if type_a == "ATOM  ":
	    string += "%s %s	1 %s	1 %s	1\n" % (str(atom),str(x),str(y),str(z))
	else:
	    pass
    with open(args.infile[:-4]+'.mop', 'w') as outfile:
	outfile.write(string)

def main():
    """ Main function
    """
    charge = 1
    create_mop_file(charge)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculates different energy terms using MOPAC package.')
    parser.add_argument('-i', '--infile', required=True, help='Input file in pdb format')
    args = parser.parse_args()
    main()
