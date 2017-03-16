#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  funnelMaker.py
#  
#  Copyright 2015 labio <labio@labio-Studio-XPS-8100>
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
	#####################################################################################
	#                                                                                   #
	#   The elements of the funnel, the radius 1, radius 2, radius 3 and length can     #
	#   be changed to get different shapes and compositions.                            #
	#                                                                                   #
	#####################################################################################
"""

def add_cap():
	global AT_POS, ELEMENTS
	cad = ''
	i = -3.6
	temp = int(options.rad1/3.6)
	cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(AT_POS, ELEMENTS[0], ELEMENTS[0], AT_POS, i, 0.0, 0.0)
	AT_POS += 1
	for t in range(1, temp+1):
		rad = 3.6 * t
		perim = 2*math.pi*rad
		razon = perim/(int(perim/3.6))
		ang = razon/rad
		temp = razon/rad
		while temp <= (2*math.pi)+0.1:
			j = rad*math.cos(temp)
			k = rad*math.sin(temp)
			cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(AT_POS, ELEMENTS[0], ELEMENTS[0], AT_POS, i, j, k)
			AT_POS += 1
			temp += ang
	return cad

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

def main():
	# We use as shape for the tunnel a truncated cone: r, R, H, L
	global ELEMENTS, AT_POS
	ELEMENTS = options.elems.split('-')
	AT_POS = 1
	# Create the variables for the positions in X
	i = 0
	rad = options.rad1
	# We measure the distance between atoms in L, if another atoms besides Cl is used, 
	# you should change the 3.6 value
	distL = math.sqrt(options.tunnel**2 + (options.rad2 - options.rad1)**2)
	angle = math.acos(options.tunnel/distL)
	numAtsL = int(options.tunnel/3.6)
	distAtAtL = options.tunnel/numAtsL
	radInc = distAtAtL*math.sin(angle)
	# We add the cap to the funnel
	#cad = add_cap()
	cad = ''
	dAtAt = 3.6
	while rad <= options.rad2 + 0.1:
		perim = 2*math.pi*rad
		razon = perim/(int(perim/dAtAt))
		ang = razon/rad
		temp = ang
		while ang < (2*math.pi)+0.1:
			j = rad*math.cos(ang)
			k = rad*math.sin(ang)
			if not isANearB(ELEMENTS[1], i, j, k, 6.0, cad):
				cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(AT_POS, ELEMENTS[1], ELEMENTS[1], AT_POS, i, j, k)
			else:
				cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(AT_POS, ELEMENTS[0], ELEMENTS[0], AT_POS, i, j, k)
			AT_POS += 1
			ang += temp
		# Increment the radius and X position
		rad += radInc
		i += distAtAtL
	
	while i <= (options.tunnel + options.cone):
		perim = 2*math.pi*rad
		razon = perim/(int(perim/3.6))
		ang = razon/rad
		temp = ang
		while ang <= (2*math.pi)+0.1:
			j = rad*math.cos(ang)
			k = rad*math.sin(ang)
			if not isANearB(ELEMENTS[3], i, j, k, 6.0, cad):
				cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(AT_POS, ELEMENTS[3], ELEMENTS[3], AT_POS, i, j, k)
			else:
				cad += 'ATOM  %5d %4s %3s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n' %(AT_POS, ELEMENTS[2], ELEMENTS[2], AT_POS, i, j, k)
			AT_POS += 1
			ang += temp
		dAtAt -= 0.3
		rad += 3.6
		i += dAtAt
	
	arcOut = open(options.outFile, 'w')
	arcOut.write(cad)
	arcOut.close()
	return 0

if __name__ == '__main__':
	
	usage = 'usage: \"%prog [options] args\" or \"%prog\"'
	parser = OptionParser(usage)
	parser.add_option('-o', '--out', action='store', type='string', dest='outFile',\
	 help='Defines the name of the output pdb file. Default is the SHAPE+_+ELEMENT+.pdb', default='')
	parser.add_option('-r', '--rad1', action='store', type='float', dest='rad1',\
	 help='This option set the radius of the desired shape in ANGSTROMS. Default is 7.5 A', default='7.5')
	parser.add_option('-s', '--rad2', action='store', type='float', dest='rad2',\
	 help='This option set the radius of the desired shape in ANGSTROMS. Default is 10.0 A', default='10.0')
	parser.add_option('-e', '--element', action='store', type='string', dest='elems',\
	 help='Is the element used to make the structure. Use "-" to separate the elements.', default='CL-CL-CL-CL')
	parser.add_option('-d', '--distcone', action='store', type='float', dest='cone',\
	 help='If you have chosen the cone shape, this option set the HEIGHT of the cone in ANGSTROMS. Default is 20.0 A', default='20.0')
	parser.add_option('-l', '--disttunnel', action='store', type='float', dest='tunnel',\
	 help='If you have chosen the tunnel shape, this option ser the LENGTH of the tunnel in ANGSTROMS. Default is 80.0 A', default='80.0')
	(options, args) = parser.parse_args()
	
	main()

