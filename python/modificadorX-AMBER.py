#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  modificadorX-AMBER.py
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

def main():
	try:
		arch = open(options.inputFile, 'r')
		liCom = list(arch)
		#pos = options.distX
		i = 2
		# This step is just to avoid errors in the modification of the protein restart file,
		# in newer versions this will be improved
		if options.flagP == 0:
			lim = len(liCom)
		else:
			lim = len(liCom)/2 + 1
		while i < lim:
			liTemp = liCom[i]
			# We search for 0.0000000 because the coordinates of the first Atom of the funnel is 
			# in the 0.0000000 X coordinate, so this means that we finished with the protein Atoms,
			# this will be improved in newer versions
			if liTemp[0:12] != '   0.0000000':
				cordX1 = float(liTemp[0:12])
				#cordX1 += pos
				cordX1 += options.distX
				liTemp0 = '%3.7f'%(cordX1)
				linea = '%12s%12s%12s'%(liTemp0, liTemp[12:24], liTemp[24:36])
				if len(liTemp) > 40 and liTemp[36:48] != '   0.0000000':
					#print '##'+liTemp[36:48]+'##'
					#print '##'+str(len(liTemp))+'##'
					cordX2 = float(liTemp[36:48])
					#cordX2 += pos
					cordX2 += options.distX
					liTemp3 = '%3.7f'%(cordX2)
					linea = '%12s%12s%12s%12s%12s%12s'%(liTemp0, liTemp[12:24], liTemp[24:36], liTemp3, liTemp[48:60], liTemp[60:])
				else:
					liTemp3 = liTemp[36:]
					linea = '%12s%12s%12s%s'%(liTemp0, liTemp[12:24], liTemp[24:36], liTemp3)
				liCom[i] = linea
			else:
				i = len(liCom)+1
			i += 1
		texto = ''
		for j in range(0, len(liCom)):
			texto += liCom[j]
		arch.close()
		arch = open(options.inputFile, 'w')
		arch.write(texto)
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
	parser.add_option('-f', '--file', help='Defines the input file that is going to be edited.', action='store', type='string', dest='inputFile')
	parser.add_option('-n', '--num', help='This is the number that is going to be increased in the X coordinates of the ATOMS, is a real number.', action='store', type='float', dest='distX')
	parser.add_option('-p', '--protein', help='This is a flag to make the script know that the file belongs to the protein', action='store', type='int', dest='flagP', default=0)
	(options, args) = parser.parse_args()
	main()
