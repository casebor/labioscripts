#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_move_mol.py
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
    #  This script increment the XYZ position of an Atom a determined quantity   #
    #                                                                            #
    ##############################################################################
"""

def main():
    try:
	with open(options.pdb, 'r') as pdb_in:
	    pdb_file = list(pdb_in)
	i = 0
	point_str = options.point.split(',')
	point = [float(point_str[0]), float(point_str[1]), float(point_str[2])]
	while i<len(pdb_file):
	    if 'ATOM' in pdb_file[i][:4] or 'HETATM' in pdb_file[i][:6]:
		crd = [float(pdb_file[i][30:38]), float(pdb_file[i][38:46]), float(pdb_file[i][46:54])]
		crd[0] += point[0]
		crd[1] += point[1]
		crd[2] += point[2]
		pdb_file[i] = '%s% 8.3f% 8.3f% 8.3f%s' %(pdb_file[i][:30], crd[0], crd[1], crd[2], pdb_file[i][54:])
	    i += 1
	with open(options.outfile, 'w') as pdb_out:
	    pdb_out.write(''.join(pdb_file))
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
    parser.add_option('-p', '--point', help='Point to add at the pdb file in format X.XX,Y.YY,Z.ZZ',\
     action='store', type='string', dest='point')
    parser.add_option('-f', '--pdb', help='The pdb file of the protein alone. Only these atoms will move.',\
     action='store', type='string', dest='pdb')
    parser.add_option('-o', '--out', help='The output name of the file', action='store',\
     type='string', dest='outfile', default='outfile.pdb')
    (options, args) = parser.parse_args()
    main()
