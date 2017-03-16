#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  trajProteinExtractor.py
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
from optparse import OptionParser

"""
	##############################################################################
	#                                                                            #
    #  This script extracts only the protein from the trajectory file,           #
    #  and save it in a mdcrd format.                                            #
    #                                                                            #
    #  trajTop = Topology file of the complex protein-funnil                     #
    #  traj = Trajectory file of the md simulation                               #
    #  protTop = Topology file only of the protein                               #
    #  protInp = Restart or Input coordinates File for the protein               #
	#                                                                            #
	##############################################################################
"""

def main():
	# Open the netcdf file of the complex from the command line, must have the topology parameter file!!!
	trajC = md.load(options.traj, top=options.trajTop)
	# Open the netcdf file of the protein from the command line, must have the topology parameter file!!!
	trajP = md.load(options.protInp, top=options.protTop)
	# Get the number of residues of the protein alone
	aa = trajP.n_residues
	# Make one topology object for the selection of the protein residues
	topoC = trajC.topology
	# Make the selection depending of the number of aminoacids of the protein
	protSel = topoC.select('resid 0 to %s' %(str(aa-1)))
	# Make the trajectory only for the protein
	protTraj = trajC.atom_slice(protSel)
	# Save the trajectory in the selected format with the specified output name and extension
	if options.frmt.upper() == 'PDB':
		protTraj.save_pdb(options.outFile + '.pdb')
	elif options.frmt.upper() == 'XTC':
		protTraj.save_xtc(options.outFile + '.xtc')
	elif options.frmt.upper() == 'TRR':
		protTraj.save_trr(options.outFile + '.trr')
	elif options.frmt.upper() == 'DCD':
		protTraj.save_dcd(options.outFile + '.dcd')
	elif options.frmt.upper() == 'BINPOS':
		protTraj.save_binpos(options.outFile + '.binpos')
	elif options.frmt.upper() == 'MDCRD':
		protTraj.save_mdcrd(options.outFile + '.mdcrd')
	else:
		protTraj.save_netcdf(options.outFile + '.nc')
	return 0

if __name__ == '__main__':
	
	usage = 'usage: \"%prog [options] args\"'
	parser = OptionParser(usage)
	parser.add_option('-o', '--out', action='store', type='string', dest='outFile',\
	 help='Defines the name of your output file, Default is output.', default='output')
	parser.add_option('-t', '--traj', action='store', type='string', dest='traj',\
	 help='This is the trajectory file from wich you want to extract the protein.')
	parser.add_option('-p', '--prottop', action='store', type='string', dest='protTop',\
	 help='It\'s the protein topology file, only the protein.')
	parser.add_option('-i', '--protinp', action='store', type='string', dest='protInp',\
	 help='The input coordinates file of the MD simulation, only for the protein.')
	parser.add_option('-c', '--trajtop', action='store', type='string', dest='trajTop',\
	 help='Defines the complex topology of the trajectory.')
	parser.add_option('-f', '--format', action='store', type='string', dest='frmt',\
	 help='Here you define the format of your protein trajectory, currently supported\
	 PDB, XTC TRR, DCD, binpos, NetCDF and MDCRD (AMBER) formats. Default is NetCDF.',\
	  default='NetCDF')
	(options, args) = parser.parse_args()
	
	main()

