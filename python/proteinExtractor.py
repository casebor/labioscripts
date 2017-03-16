#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  proteinExtractor.py
#  
#  Copyright 2015 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
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

import mdtraj as md
import sys

#        0                   1           2            3              4       
# ProteinExtractor.py complex.prmtop complex.nc protein.prmtop protein.inpcrd

"""
    ##############################################################################
    #                                                                            #
    #  This script extracts only the protein from the trajectory file,           #
    #  and save it in a mdcrd format.                                            #
    #                                                                            #
    #  python proteinExtractor_v0.py [compTopo] [compTraj] [protTopo] [protInp]  #
    #                                                                            #
    #  compTopo = Topology file of the complex protein-funnil                    #
    #  compTraj = Trajectory file of the md simulation                           #
    #  protTopo = Topology file only of the protein                              #
    #  protInp = Restart or Input coordinates File for the protein               #
    #                                                                            #
    ##############################################################################
"""

def main():
    # Open the netcdf file of the complex from the command line, must have the topology parameter file!!!
    trajC = md.load(sys.argv[2], top=sys.argv[1])
    # Open the netcdf file of the protein from the command line, must have the topology parameter file!!!
    trajP = md.load(sys.argv[4], top=sys.argv[3])
    # Get the number of residues of the protein alone
    aa = trajP.n_residues
    # Make one topology object for the selection of the protein residues
    topoC = trajC.topology
    # Make the selection depending of the number of aminoacids of the protein
    protSel = topoC.select('resid 0 to '+str(aa-1))
    # Make the trajectory only for the protein
    protTraj = trajC.atom_slice(protSel)
    # Make the name for the file to be saved
    protTemp = sys.argv[2][:-3].split('-')
    protFile = '%s-without' %(protTemp[0])
    for i in range(2, len(protTemp)):
	    protFile += '-%s' %(protTemp[i])
    # Save the trajectory in mdcrd format with the same name of the trajectory, but with .mdcrd extension
    protTraj.save_mdcrd(protFile+'.mdcrd')
    return 0

if __name__ == '__main__':
    main()

