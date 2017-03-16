#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_generate_pdbs.py
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

import sys, os, ntpath, subprocess
from optparse import OptionParser

def main():
    input_name = os.path.splitext(options.trajin)[0]
    index_file = input_name + "_index.txt"
    # Create Index if wasn't already created
    if(not os.path.isfile(index_file)):
	print("Creating Index File From: " + input_name)
	sys.stdout.flush()
	os.system("sed -n '/MODEL/ =' " + options.trajin + " > " + index_file)
	print("Index from " + input_name + " created!")
    # Creates all the models
    i = 1
    with open(index_file, 'r') as ind:
	for line in ind:
	    output_file = options.trajin[:-4] + "_M" + str(i) + ".pdb"
	    os.system("sed -n ' " + line.strip() + " {n; :loop /ENDMDL/ q; p; n; b loop;}' " + options.trajin + " > " + output_file)
	    i += 1
    return 0

if __name__ == '__main__':
    usage = 'usage: \"%prog args\"'
    parser = OptionParser(usage)
    parser.add_option('-y', '--traj', action='store', type='string', dest='trajin', help='The trajectory input file in PDB format.')
    (options, args) = parser.parse_args()
    main()
