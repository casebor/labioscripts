#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_invert_protein.py
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

def main():
    """ Main function
    """
    resid_num = res = 0
    with open(args.infile, 'r') as inf:
	atoms = list(inf)
    atoms.reverse()
    out = []
    for atom in atoms:
	#if atom[:6] == 'ATOM  ' and not (atom[13:16]=='OXT' or atom[13:16]=='H1 ' or atom[13:16]=='H2 ' or atom[13:16]=='H3 '):
	if atom[:6] == 'ATOM  ':
	    r_num = int(atom[23:27])
	    if res != r_num:
		res = r_num
		resid_num += 1
	    at = '%s     %s%4s%s' %(atom[:6], atom[11:22], str(resid_num).rjust(4), atom[26:])
	    out.append(at)
    if args.outfile == 'default':
	out_n = args.infile.split('.')
	args.outfile = ''.join(out_n[:-1]) + '_reverse.pdb'
    with open(args.outfile, 'w') as out_f:
	out_f.write(''.join(out))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inverts the index sequence of an aminoacid chain.')
    parser.add_argument('-i', '--infile', required=True, help='The PDB file to be inverted.')
    parser.add_argument('-o', '--outfile', default='default', help='The name of the inverted aminoacid chain. Default is the input name with "_reverse.pdb" at the end.')
    args = parser.parse_args()
    main()
