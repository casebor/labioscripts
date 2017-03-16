#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  moveX.py
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

from optparse import OptionParser

"""
	##############################################################################
	#                                                                            #
	#  This script increment the X position of an Atom a determined quantity     #
	#                                                                            #
	##############################################################################
"""

def get_num_atoms():
	arcPdb = open(options.pdb)
	liPdb = list(arcPdb)
	arcPdb.close()
	lin = liPdb[-3].split()
	return int(lin[1])

def main():
	try:
		atoms = get_num_atoms()
		arch = open(options.inputFile, 'r')
		liCom = list(arch)
		arch.close()
		i = 2
		atCont = 0
		while atCont < atoms and i < len(liCom):
			liTemp = liCom[i]
			cordX = float(liTemp[:12])
			cordX += options.distX
			strCrdX = '%3.7f'%(cordX)
			liTemp = '%12s%s'%(strCrdX, liTemp[12:])
			atCont += 1
			if atCont < atoms:
				cordX = float(liTemp[36:48])
				cordX += options.distX
				strCrdX = '%3.7f'%(cordX)
				liTemp = '%s%12s%s'%(liTemp[:36], strCrdX, liTemp[48:])
				atCont += 1
			liCom[i] = liTemp
			i += 1
		arch = open(options.inputFile, 'w')
		arch.write(''.join(liCom))
		arch.close()
	except IOError as io:
		print "I/O error({0}): {1}".format(io.errno, io.strerror)
		parser.print_help()
	except TypeError as te:
		print str(te) + ' - some argument is missed!!!'
		parser.print_help()
	return 0

if __name__ == '__main__':
	usage = 'usage: %prog [options] args'
	parser = OptionParser(usage)
	parser.add_option('-n', '--num', help='This is the number that is going to be increased in\
	 the X coordinates of the ATOMS, is a real number.', action='store', type='float', dest='distX')
	parser.add_option('-f', '--file', help='Defines the input file that is going to be edited.',\
	 action='store', type='string', dest='inputFile')
	parser.add_option('-p', '--pdb', help='The pdb file of the protein alone. Only these atoms will move.',\
	 action='store', type='string', dest='pdb')
	#parser.add_option('-a', '--atoms', help='This is the number of atoms that are going to be\
	# moved. It is an integer', action='store', type='int', dest='atoms')
	(options, args) = parser.parse_args()
	main()
