#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  proteinExtractor_netcdfToPdb.py
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

import mdtraj as md
import sys

####################################################################################################
#                                                                                                  #
# This script takes a trajectory file from netcdf file and extracts only the protein atoms, in     #
# other words, takes the funnil atoms out of the trajectory                                        #
# compTraj can be a single file or a list of many files, just ensure you use the '-cy' flag once   #
#                                                                                                  #
# usage: python proteinExtractor.py -cp compTopo -ct compTraj -pp protPdb                          #
#                                                                                                  #
####################################################################################################

def is_command(cad):
    """ Returns True if the parameter is a command """
    return cad == '-cp' or cad == '-ct' or cad == '-pp'
    

def main():
    
    # List of trajectories to use
    trajs = []
    i = 1
    if len(sys.argv) <= 1:
	print usage
	quit()
    while i < len(sys.argv):
	#print sys.argv[i]
	if sys.argv[i] == '-ct':
	    i += 1
	    while not is_command(sys.argv[i]) and i < len(sys.argv):
		trajs.append(sys.argv[i])
		i += 1
	    i -= 1
	elif sys.argv[i] == '-cp':
	    i += 1
	    # Complex topology file
	    complex_top = sys.argv[i]
	elif sys.argv[i] == '-pp':
	    i += 1
	    # PDB file of the protein alone
	    prot_pdb = md.load_pdb(sys.argv[i])
	else:
	    print 'Error trying to parse the commands'
	    print usage
	    quit()
	#print i
	i += 1
    
    residues = prot_pdb.n_residues - 1
    for tr in trajs:
	complex_tr = md.load_netcdf(tr, top=complex_top)
	atom_select = complex_tr.topology.select('resid 0 to ' + str(residues))
	prot_select = complex_tr.atom_slice(atom_select)
	prot_select.save_pdb(tr[:-3] + '.pdb')
    
    return 0

if __name__ == '__main__':
    
    usage = 'usage: python proteinExtractor.py -cp compTopo -ct compTraj -pp protPdb'
    
    main()























