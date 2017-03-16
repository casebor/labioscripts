#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_add_mols.py
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
import math

def get_mass_center(pdb_str):
    """ Returns the mass center of a molecule.
    """
    pdb_list = pdb_str.split('\n')
    point = [0.0, 0.0, 0.0]
    atoms = 0
    for line in pdb_list:
	if 'ATOM' == line[:4] or 'HETATM' == line[:6]:
	    crd = [float(line[30:38]), float(line[38:46]), float(line[46:54])]
	    point[0] += crd[0]
	    point[1] += crd[1]
	    point[2] += crd[2]
	    atoms += 1
	elif 'ENDMDL' == line[:6] or 'END' == line[:3]:
	    break
    point[0] /= atoms
    point[1] /= atoms
    point[2] /= atoms
    return point

def move_mol(pdb_str, point):
    """ Move all the atoms of a molecule the coordinates of a given point.
    """
    pdb_list = pdb_str.split('\n')
    i = 0
    while i<len(pdb_list):
	if 'ATOM' == pdb_list[i][:4] or 'HETATM' == pdb_list[i][:6]:
	    crd = [float(pdb_list[i][30:38]), float(pdb_list[i][38:46]), float(pdb_list[i][46:54])]
	    crd[0] += point[0]
	    crd[1] += point[1]
	    crd[2] += point[2]
	    pdb_list[i] = '%s% 8.3f% 8.3f% 8.3f%s' %(pdb_list[i][:30], crd[0], crd[1], crd[2], pdb_list[i][54:])
	i += 1
    return '\n'.join(pdb_list)

def get_bounds(pdb_str):
    """ Returns the maximun distance from the mass center of a molecule
	to the axis X, Y and Z.
    """
    pdb_list = pdb_str.split('\n')
    bound = [0.0, 0.0, 0.0]
    atoms = 0
    for line in pdb_list:
	if 'ATOM' == line[:4] or 'HETATM' == line[:6]:
	    crd = [math.fabs(float(line[30:38])), math.fabs(float(line[38:46])), math.fabs(float(line[46:54]))]
	    if crd[0] > bound[0]:
		bound[0] = crd[0]
	    if crd[1] > bound[1]:
		bound[1] = crd[1]
	    if crd[2] > bound[2]:
		bound[2] = crd[2]
	elif 'ENDMDL' == line[:6] or 'END' == line[:3]:
	    break
    # Add a distance to avoid collitions of atoms
    return [bound[0]+1, bound[1]+1, bound[2]+1]

def main():
    """ Main function
    """
    output_mol = ''
    mol_str = args.molecule.read()
    prot_str = args.protein.read()
    mol_mc = get_mass_center(mol_str)
    prot_mc = get_mass_center(prot_str)
    mol_zero_mc = move_mol(mol_str, [-mol_mc[0],-mol_mc[1],-mol_mc[2]])
    prot_zero_mc = move_mol(prot_str, [-prot_mc[0],-prot_mc[1],-prot_mc[2]])
    mol_bounds = get_bounds(mol_zero_mc)
    prot_bounds = get_bounds(prot_zero_mc)
    box_point = [prot_bounds[0]+mol_bounds[0],prot_bounds[1]+mol_bounds[1],prot_bounds[2]+mol_bounds[2]]
    mol_point = [mol_bounds[0]*2,mol_bounds[1]*2,mol_bounds[2]*2]
    mols_added = 0
    qty_mols_per_prot_x = prot_bounds[0]/(mol_bounds[0]*2)
    qty_mols_per_prot_y = prot_bounds[1]/(mol_bounds[1]*2)
    qty_mols_per_prot_z = prot_bounds[2]/(mol_bounds[2]*2)
    mols_x = int(qty_mols_per_prot_x)*2+2
    mols_y = int(qty_mols_per_prot_y)*2+1
    mols_z = int(qty_mols_per_prot_z)*2+1
    max_mols = 2*(mols_y*mols_z) + 2*(mols_x*mols_z) + 2*(mols_x*mols_y)
    mols_per_cycle = 2*mols_x + 2*mols_y + 2*mols_z
    cycles = int(max_mols/mols_per_cycle)+1
    output_mol += prot_zero_mc
    for i in range(cycles):
	if mols_added == args.number:
	    break
	if i==0:
	    f = 0
	elif i%2!=0:
	    f = int(i/2)+1
	else:
	    f = -i/2
	points = [[ box_point[0],0,f*(mol_point[2])],
		  [-box_point[0],0,f*(mol_point[2])],
		  [f*(mol_point[0]), box_point[1],0],
		  [f*(mol_point[0]),-box_point[1],0],
		  [0,f*(mol_point[1]), box_point[2]],
		  [0,f*(mol_point[1]),-box_point[2]]]
	cont = 0
	cont_x = cont_y = cont_z = 0
	ji = 0
	while cont<mols_per_cycle and mols_added<args.number:
	    if ji==0:
		j = 0
	    elif ji%2!=0:
		j = int(ji/2)+1
	    else:
		j = -ji/2
	    if cont_x<mols_x:
		temp_mol = move_mol(mol_zero_mc, points[0])
		temp_mol = move_mol(temp_mol, [0,j*mol_point[1],0])
		output_mol += temp_mol
		mols_added += 1
		cont += 1
		if mols_added == args.number:
		    break
		temp_mol = move_mol(mol_zero_mc, points[1])
		temp_mol = move_mol(temp_mol, [0,-j*mol_point[1],0])
		output_mol += temp_mol
		mols_added += 1
		cont += 1
		if mols_added == args.number:
		    break
	    if cont_y<mols_y:
		temp_mol = move_mol(mol_zero_mc, points[2])
		temp_mol = move_mol(temp_mol, [0,0,j*mol_point[2]])
		output_mol += temp_mol
		mols_added += 1
		cont += 1
		if mols_added == args.number:
		    break
		temp_mol = move_mol(mol_zero_mc, points[3])
		temp_mol = move_mol(temp_mol, [0,0,-j*mol_point[2]])
		output_mol += temp_mol
		mols_added += 1
		cont += 1
		if mols_added == args.number:
		    break
	    if cont_z<mols_z:
		temp_mol = move_mol(mol_zero_mc, points[4])
		temp_mol = move_mol(temp_mol, [j*mol_point[0],0,0])
		output_mol += temp_mol
		mols_added += 1
		cont += 1
		if mols_added == args.number:
		    break
		temp_mol = move_mol(mol_zero_mc, points[5])
		temp_mol = move_mol(temp_mol, [-j*mol_point[0],0,0])
		output_mol += temp_mol
		mols_added += 1
		cont += 1
		if mols_added == args.number:
		    break
	    ji += 1
    args.out.write(output_mol)
    print 'The maximum number of molecules you can add in one run to this protein is:', max_mols
    if args.number > max_mols:
	print 'Maximum number of molecules reached, you need to run this script again with the output as input for another round of addition using:', args.number-max_mols, 'as quantity.'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Adds small molecules around a protein. Uses pdb formatted files.')
    parser.add_argument('-m', '--molecule', type=argparse.FileType('r'), required=True, help='The molecule PDB file to be added around the protein. IMPORTANT!!! To facilitate the use of this script, the molecule center of mass will be moved to (0,0,0), but the original file will remain untouched.')
    parser.add_argument('-p', '--protein', type=argparse.FileType('r'), required=True, help='The protein PDB file to use. IMPORTANT!!! To facilitate the use of this script, the protein center of mass will be moved to (0,0,0), but the original file will remain untouched.')
    parser.add_argument('-n', '--number', type=int, required=True, help='This parameter defines the number of molecules to be added to the protein.')
    parser.add_argument('-o', '--out', type=argparse.FileType('w'), required=True, help='The name of the output file. If the file exist, will be overwritten.')
    args = parser.parse_args()
    main()
