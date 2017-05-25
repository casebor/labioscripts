#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_get_triangle_area.py
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
import os
import numpy as np

def make_index_files (residues):
    """ Function doc """
    for res in residues:
        order = 'gmx make_ndx -f %s -o _temporary_resid_%s.ndx<<EOF\n' %(args.gro, res)
        order += 'del 0-25\n'
        order += 'r %s\n' %(res)
        order += 'q\nEOF\n'
        os.system(order)

def make_position_files (residues):
    """ Function doc """
    for res in residues:
        order = 'gmx traj -f %s -s %s -n _temporary_resid_%s.ndx -oxt _temporary_resid_%s.pdb -com<<EOF\n' %(args.trajin, args.topol, res, res)
        os.system(order)
        order2 = 'grep "ATOM" _temporary_resid_%s.pdb | awk \'{print $6"\t"$7"\t"$8"\t"$9}\' > _temporary_pos_%s.txt' %(res, res)
        os.system(order2)

def get_area (residues):
    """ Function doc """
    point_A = np.loadtxt('_temporary_pos_%s.txt'%(residues[0]), usecols=(1,2,3))
    point_B = np.loadtxt('_temporary_pos_%s.txt'%(residues[1]), usecols=(1,2,3))
    point_C = np.loadtxt('_temporary_pos_%s.txt'%(residues[2]), usecols=(1,2,3))
    areas = '#Frame\tArea\tAB\tAC\tBC\n'
    for i in range(len(point_A)):
        vec_AB = point_B[i] - point_A[i]
        vec_AC = point_C[i] - point_A[i]
        vec_BC = point_B[i] - point_C[i]
        cross_vec = np.cross(vec_AB, vec_AC)
        dist_AB = np.linalg.norm(vec_AB)
        dist_AC = np.linalg.norm(vec_AC)
        dist_BC = np.linalg.norm(vec_BC)
        area = (np.linalg.norm(cross_vec))/2.0
        areas += 'Frame\t%d\t%f\t%f\t%f\t%f\n' %(i, area, dist_AB, dist_AC, dist_BC)
    with open(args.outfile, 'w') as outfile:
        outfile.write(areas)

def main():
    """ Main function """
    residues = args.resids.split(',')
    if len(residues) == 3:
        make_index_files(residues)
        make_position_files(residues)
        get_area(residues)
        if not args.keep:
            os.system('rm _temporary_*')
    else:
        print("You must enter three residues!!!")
        quit()
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Your script description')
    parser.add_argument('-x', '--trajin', action='store', required=True, dest='trajin', help="The trajectory file from GROMACS. Usually a .xtc file.")
    parser.add_argument('-g', '--gro', action='store', required=True, dest='gro', help="The .gro file used in the GROMACS simulation. This file is needed for the generation of indexes.")
    parser.add_argument('-r', '--resids', action='store', required=True, dest='resids', help="The index number of the residues used to generate the triangle. Use comma separated, example: 118,152,198")
    parser.add_argument('-t', '--topol', action='store', required=True, dest='topol', help="The topology file of the simulation.")
    parser.add_argument('-k', '--keep', action='store_true', help="Flag to keep the temporary files created. Default is False")
    parser.add_argument('-c', '--calpha', action='store_true', help="Flag to use the alpha carbons instead of center of mass. Default is False")
    parser.add_argument('-o', '--out', action='store', dest='outfile', default='areas.txt', help="Output file where the data will be stored. Default is areas.txt")
    args = parser.parse_args()
    main()
