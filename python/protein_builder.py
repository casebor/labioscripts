#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  protein_builder.py
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

from Bio.PDB import PDBParser

"""
    ######################################################################################
    #                                                                                    #
    #  Makes the .pdb file of a protein sequence, aligned at the X axis and in the       #
    #  negative direction.                                                               #
    #  This constructs the protein only with their backbone atoms, N-Ca-C=O.             #
    #                                                                                    #
    ######################################################################################
"""

class NoProtError(Exception):
    def __init__(self, value):
	self.value = value
    def __str__(self):
	return repr(self.value)

def get_seq(pdb_file):
    """Returns an array with the aminoacids of the pdb file specified
    
    ######################################################################################
    #                                                                                    #
    #  This function makes use of the Biopython module, so it will not work if this      #
    #  module is not installed.                                                          #
    #  This function reads a pdb file and extracts only the sequence of aminoacids of    #
    #  the first chain, note that only the residues with a valid 3 letter code will be   #
    #  used.                                                                             #
    #                                                                                    #
    ######################################################################################
    """
    parser = PDBParser()
    structure = parser.get_structure(pdb_file[:-4], pdb_file)
    resids = structure.get_residues()
    residues = []
    for r in resids:
	aa = r.get_resname()
	if is_aa(aa):
	    residues.append(aa)
    if len(residues) == 0:
	print('404 - No Sequence Found!!!')
	raise NoProtError('404 - No Sequence Found!!!')
    return residues

def get_atoms(pdb_file):
    """Returns an array with the atoms of the pdb file specified
    
    ######################################################################################
    #                                                                                    #
    #  This function makes use of the Biopython module, so it will not work if this      #
    #  module is not installed.                                                          #
    #  This function reads a pdb file and extracts only the atoms of the first chain.    #
    #                                                                                    #
    ######################################################################################
    """
    parser = PDBParser()
    structure = parser.get_structure(pdb_file[:-4], pdb_file)
    atms = structure.get_atoms()
    atoms = []
    for a in atms:
	atoms.append(a.get_name())
    if len(atoms) == 0:
	print('404 - No Atoms Found!!!')
	raise NoProtError('404 - No Atoms Found!!!')
    return atoms

def is_aa(aa):
	aminoacids = ('ALA', 'ARG', 'ASN', 'ASP', 'CYS', 
		      'GLN', 'GLU', 'GLY', 'HIS', 'ILE', 
		      'LEU', 'LYS', 'MET', 'PHE', 'PRO', 
		      'SER', 'THR', 'TRP', 'TYR', 'VAL')
	return aa in aminoacids

def add_aa_atoms(aa, protein):
    """Returns the "protein" string modified.
    
    ######################################################################################
    #                                                                                    #
    #  This function modifies the protein string in the following way:                   #
    #  Adds the missing atoms of an aminoacid                                            #
    #                                                                                    #
    ######################################################################################
    """
    

def crt_body(aa_chain):
    """Returns a string containing the pdb coordinates file of the specified aminoacid
       chain
    """
    atoms = len(aa_chain)*3
    pto_a = [-1.216, 0.829, 0.0]
    pto_b = [-2.5, 0.0, 0.0]
    factor = -1.242
    pts = [pto_a, pto_b]
    res = 0
    protein = '%-6s%5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n'\
              %('ATOM', 1, 'N', '', aa_chain[res], '', res+1, '', 0.0, 0.0, 0.0, 1.0, 10.0, 'N', '')
    atoms -= 1
    i = 0
    while atoms>0:
	protein += '%-6s%5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n'\
	           %('ATOM', 1, 'CA', '', aa_chain[res], '', res+1, '', pts[i][0], pts[i][1], pts[i][2], 1.0, 10.0, 'C', '')
	pts[i][0] -= 2.5
	atoms -= 1
	i += 1
	pts.append(pto_a)
	pts.append(pto_b)
	protein += '%-6s%5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n'\
	           %('ATOM', 1, 'C', '', aa_chain[res], '', res+1, '', pts[i][0], pts[i][1], pts[i][2], 1.0, 10.0, 'C', '')
	protein += '%-6s%5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n'\
	           %('ATOM', 1, 'O', '', aa_chain[res], '', res+1, '', pts[i][0], pts[i][1]+factor, pts[i][2], 1.0, 10.0, 'O', '')
	pts[i][0] -= 2.5
	atoms -= 1
	i += 1
	factor *= -1
	pts.append(pto_a)
	pts.append(pto_b)
	if atoms>0:
	    res += 1
	    protein += '%-6s%5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n'\
	               %('ATOM', 1, 'N', '', aa_chain[res], '', res+1, '', pts[i][0], pts[i][1], pts[i][2], 1.0, 10.0, 'N', '')
	    pts[i][0] -= 2.5
	    atoms -= 1
	    i += 1
    return protein
