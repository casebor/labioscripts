#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cluscoFormatter.py
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

import sys

#                 0             1         2    
# python cluscoFormatter.py input.pdb output.pdb

"""
###################################################################################
#                                                                                 #
#  This script just change the format of .pdb trajectory files to be accepted     #
#  by the ClusCo software                                                         #
#                                                                                 #
###################################################################################
"""

def main():
	# Open the file to be modified
	arc = open(sys.argv[1],'r')
	arcList = list(arc)
	# Create a new string that will contain all the data of the trajectory, every
	# frame of the trajectory has to be precedded with MODEL, and ENDMDL at the end
	cad = 'MODEL\n'
	i = 1
	while i < len(arcList)-1:
		# We iterate trough all the file to search the end of every frame and add the lines
		# ENDMDL and MODEL
		if 'END' in arcList[i]:
			cad += 'ENDMDL\nMODEL\n'
		else:
			cad += arcList[i]
		i += 1
	if 'END' in arcList[i]:
		cad += 'ENDMDL\n'
	b = open(sys.argv[2],'w')
	b.write(cad)
	b.close()
	return 0

if __name__ == '__main__':
	main()

