#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_restart_protein_extractor.py
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

#import sys, restartMaker as rm
import atom as at
from optparse import OptionParser

"""
    ##############################################################################
    #                                                                            #
    #  This script just takes an Amber restart file with a protein-funnel        #
    #  complex and extracts only the protein from it.                            #
    #                                                                            #
    ##############################################################################
"""

def get_atoms(lista, atomLim):
    """
    ##############################################################################
    #                                                                            #
    #  This function returns an array with the atoms extracted from an Amber     #
    #  restart file from the beggining to the end, using atomLim as limiting     #
    #  number of atoms.                                                          #
    #                                                                            #
    ##############################################################################
    """
    atoms = []
    if len(lista)>0:
	i = 2
	atms = 0
	while atms < atomLim:
	    atm1 = at.Atom(lista[i][0:12], lista[i][12:24], lista[i][24:36])
	    atoms.append(atm1)
	    atms += 1
	    if atms < atomLim:
		atm2 = at.Atom(lista[i][36:48], lista[i][48:60], lista[i][60:72])
		atoms.append(atm2)
		atms += 1
	    i += 1
	atms = 0
	i = (len(lista)/2)+1
	while atms < atomLim:
	    atoms[atms].set_vels(lista[i][0:12], lista[i][12:24], lista[i][24:36])
	    atms += 1
	    if atms < atomLim:
		atoms[atms].set_vels(lista[i][36:48], lista[i][48:60], lista[i][60:72])
		atms += 1
	    i += 1
    return atoms

def generate_prot(baseProt, restart_info):
    """
    ##############################################################################
    #                                                                            #
    #  This function returns a String containing all the atoms in the array      #
    #  builded in an Amber restart file format.                                  #
    #                                                                            #
    ##############################################################################
    """
    try:
	protein = 'default_name\n%5s%15s%15s\n' %(str(len(baseProt)), restart_info[1], restart_info[2])
    except IndexError:
	protein = 'default_name\n%5s%15s\n' %(str(len(baseProt)), restart_info[1])
    if len(baseProt)%2 == 0:
	for i in range(0, len(baseProt), 2):
	    protein += '%12s%12s%12s%12s%12s%12s\n' %(baseProt[i].get_pos_x(), baseProt[i].get_pos_y(), baseProt[i].get_pos_z(), baseProt[i+1].get_pos_x(), baseProt[i+1].get_pos_y(), baseProt[i+1].get_pos_z())
	for i in range(0, len(baseProt), 2):
	    protein += '%12s%12s%12s%12s%12s%12s\n' %(baseProt[i].get_vel_x(), baseProt[i].get_vel_y(), baseProt[i].get_vel_z(), baseProt[i+1].get_vel_x(), baseProt[i+1].get_vel_y(), baseProt[i+1].get_vel_z())
    else:
	for i in range(0, len(baseProt)-1, 2):
	    protein += '%12s%12s%12s%12s%12s%12s\n' %(baseProt[i].get_pos_x(), baseProt[i].get_pos_y(), baseProt[i].get_pos_z(), baseProt[i+1].get_pos_x(), baseProt[i+1].get_pos_y(), baseProt[i+1].get_pos_z())
	protein += '%12s%12s%12s\n' %(baseProt[-1].get_pos_x(), baseProt[-1].get_pos_y(), baseProt[-1].get_pos_z())
	for i in range(0, len(baseProt)-1, 2):
	    protein += '%12s%12s%12s%12s%12s%12s\n' %(baseProt[i].get_vel_x(), baseProt[i].get_vel_y(), baseProt[i].get_vel_z(), baseProt[i+1].get_vel_x(), baseProt[i+1].get_vel_y(), baseProt[i+1].get_vel_z())
	protein += '%12s%12s%12s\n' %(baseProt[-1].get_vel_x(), baseProt[-1].get_vel_y(), baseProt[-1].get_vel_z())
    return protein

def main():
    try:
	# We open the restart file to be modified, and put the data in restList
	inFile = open(options.inputFile, 'r')
	inList = list(inFile)
	inFile.close()
	# We open the input coordinates file to get the number of atoms of the protein, 
	# and put the data in refList
	refFile = open(options.refFile, 'r')
	refList = list(refFile)
	refFile.close()
	# We get the number of atoms in the protein
	numAtmsRef = int(refList[1].split()[0])
	restart_info = inList[1].split()
	# And the atoms from the restart file, only of the protein
	atoms = get_atoms(inList, numAtmsRef)
	# We generate the protein in an AMBER restart format
	protein = generate_prot(atoms, restart_info)
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
    parser.add_option('-f', '--file', help='Defines the input file that is going to be edited.',\
     action='store', type='string', dest='inputFile')
    parser.add_option('-r', '--ref', help='This is the file that contains the desired output\
     number of ATOMS. The protein restart or input coordinates file goes here',\
     action='store', type='string', dest='refFile')
    parser.add_option('-o', '--out', help='This is the name for the output file to be generated\
     with the modified number of ATOMS. It is a topology format file. Default outRST.rst',\
      action='store', type='string', dest='outFile', default='outRST.rst')
    (options, args) = parser.parse_args()
    
    main()
