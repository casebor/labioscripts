#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  shapes.py
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

import math
from optparse import OptionParser
"""
	##############################################################################
	#                                                                            #
	#  This script increment the X position of an Atom a determined quantity     #
	#                                                                            #
	##############################################################################
"""

def amberAtomType(atom):
	'''amberAtoms = ('H', 'HC', 'HO', 'HS', 'HW', 'H2', 'H3', 'C', 'CA', 'CB', 'CC', 'CK', 'CM', 'CN',\
	 'CQ', 'CR', 'CT', 'CV', 'CW', 'C*', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CP', 'C2', 'C3',\
	 'N', 'NA', 'NB', 'NC', 'NT', 'N2', 'N3', 'N*', 'O', 'OH', 'OS', 'OW', 'O2', 'S', 'SH', 'P',\
	 'CU', 'C0', 'I', 'IM', 'MG', 'QC', 'QK', 'QL', 'QN', 'QR', 'LP')'''
	amberAtoms = {'C', 'O', 'N', 'S', 'P', 'MG', 'F', 'Ar', 'CL', 'NA', 'H', 'BR', 'CA', 'ZN', 'H'}
	return atom in amberAtoms

def isANearB(elemA, aX, aY, aZ, radA, cadPdb):
	resp = False
	cads = cadPdb.split('\n')
	i = 0
	while i<len(cads) and not resp:
		if elemA in cads[i]:
			cadsA = cads[i].split()
			x = float(cadsA[5])
			y = float(cadsA[6])
			z = float(cadsA[7])
			distAB = ((aX-x)**2 + (aY-y)**2 + (aZ-z)**2)**0.5
			if distAB<radA:
				resp = True
		i += 1
	return resp

def complexOK():
	if len(options.complexF)<7:
		return False
	else:
		elems = options.complexF.split('-')
		if len(elems)<>4:
			parser.error('Option complex must have 4 elements, and they must be valid Amber ATOMS!!!')
			quit()
		else:
			for i in elems:
				if not amberAtomType(i):
					parser.error('Option complex must have 4 elements, and they must be valid Amber ATOMS!!!')
					quit()
			return True

def main():
	atPos = 1
	cad = ''
	dAtAt = 3.6
	dAtAt2 = 3.6
	cont = 1
	i = 0.0
	arco = 3.6
	if options.shapeS.upper() == 'CONE':
		while (i<options.TxC):
			perim = 2*math.pi*options.Ri
			razon = perim/(int(perim/arco))
			ang = razon/options.Ri
			temp = ang
			while ang <= (2*math.pi)+0.1:
				j = options.Ri*math.cos(ang)
				k = options.Ri*math.sin(ang)
				ang += temp
				if len(options.elem2)>0 and not isANearB(options.elem2, i, j, k, options.interval, cad):
					cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(atPos, options.elem2, options.elem2, atPos, i, j, k)
				else:
					cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(atPos, options.elem, options.elem, atPos, i, j, k)
				atPos += 1
			if cont%3 == 0:
				dAtAt2 -= 0.2
			cont += 1
			i += dAtAt2
			options.Ri = options.Ri+1.3*math.log10(options.Ri)**2
	elif options.shapeS.upper() == 'TUBE':
		while (i<options.TxT):
			perim = 2*math.pi*options.Ri
			razon = perim/(int(perim/arco))
			ang = razon/options.Ri
			temp = ang
			while ang < (2*math.pi)+0.1:
				j = options.Ri*math.cos(ang)
				k = options.Ri*math.sin(ang)
				ang += temp
				if len(options.elem2)>0 and not isANearB(options.elem2, i, j, k, options.interval, cad):
					cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(atPos, options.elem2, options.elem2, atPos, i, j, k)
				else:
					cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(atPos, options.elem, options.elem, atPos, i, j, k)
				atPos += 1
			i += dAtAt
	elif options.shapeS.upper() == 'FUNNEL' and not complexOK():
		while (i<options.TxT+options.TxC):
			if i<=options.TxT:
				perim = 2*math.pi*options.Ri
				razon = perim/(int(perim/arco))
				ang = razon/options.Ri
				temp = ang
				while ang < (2*math.pi)+0.1:
					j = options.Ri*math.cos(ang)
					k = options.Ri*math.sin(ang)
					ang += temp
					if len(options.elem2)>0 and not isANearB(options.elem2, i, j, k, options.interval, cad):
						cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(atPos, options.elem2, options.elem2, atPos, i, j, k)
					else:
						cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(atPos, options.elem, options.elem, atPos, i, j, k)
					atPos += 1
			else:
				perim = 2*math.pi*options.Ri
				razon = perim/(int(perim/arco))
				ang = razon/options.Ri
				temp = ang
				while ang <= (2*math.pi)+0.1:
					j = options.Ri*math.cos(ang)
					k = options.Ri*math.sin(ang)
					ang += temp
					if len(options.elem2)>0 and not isANearB(options.elem2, i, j, k, options.interval, cad):
						cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(atPos, options.elem2, options.elem2, atPos, i, j, k)
					else:
						cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(atPos, options.elem, options.elem, atPos, i, j, k)
					atPos += 1
				options.Ri += 1.3*math.log10(options.Ri)**2
			i += dAtAt
	elif options.shapeS.upper() == 'FUNNEL' and complexOK():
		elems = options.complexF.split('-')
		elem1 = elems[0]
		elem2 = elems[1]
		elem3 = elems[2]
		elem4 = elems[3]
		while (i<options.TxT+options.TxC):
			if i<=options.TxT:
				perim = 2*math.pi*options.Ri
				razon = perim/(int(perim/arco))
				ang = razon/options.Ri
				temp = ang
				while ang < (2*math.pi)+0.1:
					j = options.Ri*math.cos(ang)
					k = options.Ri*math.sin(ang)
					ang += temp
					if not isANearB(elem2, i, j, k, options.interval, cad):
						cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(atPos, elem2, elem2, atPos, i, j, k)
					else:
						cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(atPos, elem1, elem1, atPos, i, j, k)
					atPos += 1
			else:
				perim = 2*math.pi*options.Ri
				razon = perim/(int(perim/arco))
				ang = razon/options.Ri
				temp = ang
				while ang <= (2*math.pi)+0.1:
					j = options.Ri*math.cos(ang)
					k = options.Ri*math.sin(ang)
					ang += temp
					if not isANearB(elem4, i, j, k, options.interval, cad):
						cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(atPos, elem4, elem4, atPos, i, j, k)
					else:
						cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(atPos, elem3, elem3, atPos, i, j, k)
					atPos += 1
				options.Ri += 1.3*math.log10(options.Ri)**2
			i += dAtAt
	else:
		print 'Error in shape type'
		parser.print_help()
		quit()
	if len(options.outFile) > 0:
		arch = open(options.outFile, 'w')
	else:
		if not complexOK():
			if len(options.elem2)>0:
				outF = options.shapeS + '-' + options.elem + '-' + options.elem2 + '.pdb'
			else:
				outF = options.shapeS + '-' + options.elem + '.pdb'
		else:
			elems = options.complexF.split('-')
			outF = options.shapeS + '-' + elems[0] + '-' + elems[1] + '-' + elems[2] + '-' + elems[3] + '.pdb'
		arch = open(outF, 'w')
	arch.write(cad)
	arch.close()
	return 0

if __name__ == '__main__':
	
	usage = 'usage: \"%prog [options] args\" or \"%prog\"'
	parser = OptionParser(usage)
	parser.add_option('-o', '--out', action='store', type='string', dest='outFile', help='Defines the name of the output pdb file. Default is the SHAPE+_+ELEMENT+.pdb', default='')
	parser.add_option('-w', '--with', action='store', type='string', dest='elem2', help='Use this option to add other ATOM in your shape in regular intervals. You can change the interval with -i or --interval', default='')
	parser.add_option('-s', '--shape', action='store', type='string', dest='shapeS', help='Defines the shape of the object to be created. Values admitted are CONE, TUBE or FUNNEL. Default is CONE', default='CONE')
	parser.add_option('-r', '--radius', action='store', type='float', dest='Ri', help='This option set the radius of the desired shape in ANGSTROMS. Default is 10.0 A', default='10.0')
	parser.add_option('-e', '--element', action='store', type='string', dest='elem', help='Is the element used to make the structure', default='Ar')
	parser.add_option('-c', '--complex', action='store', type='string', dest='complexF', help='Use this option ONLY if you want to make your FUNNEL with different elements on the TUBE part than those in the CONE part. The syntax is: elem1TUBE-elem2TUBE-elem1CONE-elem2CONE, note that you need to use the \'-\' between elements. You can change the interval with -i or --interval', default='')
	parser.add_option('-d', '--distcone', action='store', type='float', dest='TxC', help='If you have chosen the cone shape, this option set the HEIGHT of the cone in ANGSTROMS; if you have chosen the funnel shape, this set the HEIGHT part of the funnel. Default is 40.0 A', default='40.0')
	parser.add_option('-i', '--interval', action='store', type='float', dest='interval', help='Set the interval for the addition of other ATOMS. Default 6.0A. Use this option only if you use -w, --with, -c or --complex!!!', default='6.0')
	parser.add_option('-l', '--disttunnel', action='store', type='float', dest='TxT', help='If you have chosen the tunnel shape, this option ser the LENGTH of the tunnel in ANGSTROMS; if you have chosen the funnel shape, this set the LENGTH of the tunnel part of the funnel. Default is 40.0 A', default='40.0')
	(options, args) = parser.parse_args()
	
	if (options.TxT<0) or (options.TxC<0) or (options.Ri<0):
		parser.error('Options -l, -d and -r must be positive or 0!!!')
		exit
	if not amberAtomType(options.elem):
		parser.error('Option element must be a valid Amber ATOM!!!')
		quit()
	if len(options.elem2)>0 and not amberAtomType(options.elem2):
		parser.error("Option with must be a valid Amber ATOM!!!\n\t'C', 'O', 'N', 'S', 'P', 'MG', 'F', 'Ar', 'CL', 'NA', 'H', 'BR', 'CA', 'ZN', 'H'")
		quit()
		
	main()
