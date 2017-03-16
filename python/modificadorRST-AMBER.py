#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  modificadorRST-AMBER.py
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

import sys, restartMaker as rm
from optparse import OptionParser

"""
	##############################################################################
	#                                                                            #
	#  This script just takes an Amber restart file with a protein-funnel        #
	#  complex and extracts only the protein from it.                            #
	#                                                                            #
	##############################################################################
"""

def main():
	try:
		# We open the restart file to be modified, and put the data in restList
		restFile = open(options.inputFile, 'r')
		restList = list(restFile)
		restFile.close()
		# We open the input coordinates file to get the number of atoms of the protein, 
		# and put the data in refList
		refFile = open(options.refFile, 'r')
		refList = list(refFile)
		refFile.close()
		# We get the number of atoms in the protein
		numAtmsRef = int(refList[1].split()[0])
		# And the atoms from the restart file, only of the protein
		atoms = rm.get_atoms(restList, numAtmsRef)
		# We generate the protein in an AMBER restart format
		protein = rm.generate_prot(atoms)
		# And save the protein with the specified name
		protFile = open(options.outFile, 'w')
		protFile.write(protein)
		protFile.close()
	except IOError as io:
		print "I/O error({0}): {1}".format(io.errno, io.strerror)
		parser.print_help()
	except TypeError as te:
		print str(te) + ' - some argument is missed!!!'
		parser.print_help()
	except IndexError as ie:
		print str(ie) + ' - check your input or ref file!!!'
		parser.print_help()
	return 0

if __name__ == '__main__':
	
	usage = 'usage: %prog [options] args'
	parser = OptionParser(usage)
	parser.add_option('-f', '--file', help='Defines the input file that is going to be edited.', action='store', type='string', dest='inputFile')
	parser.add_option('-r', '--ref', help='This is the file that contains the desired output number of ATOMS.', action='store', type='string', dest='refFile')
	parser.add_option('-o', '--out', help='This is the name for the output file to be generated with the modified number of ATOMS. It is a topology format file. Default outRST.prmtop', action='store', type='string', dest='outFile', default='outRST.prmtop')
	(options, args) = parser.parse_args()
	
	main()
