#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_get_mass_center.py
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
    """ Main function """
    lista = args.infile
    point =[0.0, 0.0, 0.0]
    atoms = 0
    for linea in lista:
	if 'ATOM' == linea[:4] or 'HETATM' == linea[:6]:
	    crd = [float(linea[30:38]), float(linea[38:46]), float(linea[46:54])]
	    point[0] += crd[0]
	    point[1] += crd[1]
	    point[2] += crd[2]
	    atoms += 1
	elif 'ENDMDL' == linea[:6] or 'END' == linea[:3]:
	    break
    point[0] /= atoms
    point[1] /= atoms
    point[2] /= atoms
    print point

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Returns the Mass Center of a pdb molecule.')
    parser.add_argument('-i', '--input',type=argparse.FileType('r'), required=True, dest='infile', help='The PDB file you want the Mass Center.')
    args = parser.parse_args()
    main()

