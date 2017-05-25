#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_rotate_mol.py
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
from math import sin, cos, degrees, radians
import numpy as np

def main():
    """ Main function """
    if args.axis > 2 or args.axis < 0:
        print 'Invalid option for axis, valid options are 0, 1 or 2.\n'
        parser.print_help()
    angle = radians(args.angle)
    cos_angle = cos(angle)
    sin_angle = sin(angle)
    if args.axis == 0:
        rot_matrix = np.array([[1,0,0], [0,cos_angle,-sin_angle], [0,sin_angle,cos_angle]])
    elif args.axis == 1:
        rot_matrix = np.array([[cos_angle,0,sin_angle], [0,1,0], [-sin_angle,0,cos_angle]])
    else:
        rot_matrix = np.array([[cos_angle,-sin_angle,0], [sin_angle,cos_angle,0], [0,0,1]])
    pdb_file = list(args.infile)
    for i in range(len(pdb_file)):
        if 'ATOM' in pdb_file[i] or 'HETATM' in pdb_file[i]:
            crd = np.array([float(pdb_file[i][30:38]), float(pdb_file[i][38:46]), float(pdb_file[i][46:54])])
            crd = np.dot(rot_matrix,crd)
            pdb_file[i] = '%s% 8.3f% 8.3f% 8.3f%s' %(pdb_file[i][:30], crd[0], crd[1], crd[2], pdb_file[i][54:])
    args.outfile.write(''.join(pdb_file))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rotates a molecule in the 3D space.')
    parser.add_argument('-i', '--input', required=True, type=argparse.FileType('r'), dest='infile', help='Input PDB file to rotate among one axis in 3D space.')
    parser.add_argument('-o', '--output', required=True, type=argparse.FileType('w'), dest='outfile', help='Defines the name of the modified molecule file.')
    parser.add_argument('-a', '--axis', required=True, type=int, dest='axis', help='Which axis is going to be used to rotate the molecule. The avaliable options are 0 to use the X axis, 1 to use Y axis and 2 to use Z axis.')
    parser.add_argument('-n', '--angle', required=True, type=float, dest='angle', help='The angle in degrees to rotate the molecule.')
    args = parser.parse_args()
    main()
