#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_edit_mopac_results.py
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

import argparse

def write_results(models):
    """ Function doc
    """
    heat_form = []
    total_en = []
    elect_en = []
    core_core_rep = []
    for model in range(1, models+1):
	with open(args.trajin[:-4]+'_M'+str(model)+'.arc', 'r') as tempfile:
	    for line in tempfile:
		line1 = line.split()
		if line[10:27] == 'HEAT OF FORMATION':
		    energy = "%s	%s %s\n"% (str(model), line1[4], line1[5])
		    heat_form.append(energy)
		if line[10:22] == 'TOTAL ENERGY':
		    energy = "%s	%s %s\n"% (str(model), line1[2], line1[3])
		    total_en.append(energy)
		if line[10:27] == 'ELECTRONIC ENERGY':
		    energy = "%s	%s %s\n"% (str(model), line1[2], line1[3])
		    elect_en.append(energy)
		if line[10:29] == 'CORE-CORE REPULSION':
		    energy = "%s	%s %s\n"% (str(model), line1[2], line1[3])
		    core_core_rep.append(energy)
    with open('heat_of_formation.txt', 'w') as results:
	results.writelines(heat_form)
    with open('total_energy.txt', 'w') as results:
	results.writelines(total_en)
    with open('electronic_energy.txt', 'w') as results:
	results.writelines(elect_en)
    with open('core_core_repulsion.txt', 'w') as results:
	results.writelines(core_core_rep)

def main():
    """ Main function
    """
    models = int(args.models)
    write_results(models)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculates different energy terms using MOPAC package.')
    parser.add_argument('-y', '--trajin', required=True, help='Trajectory file name.')
    parser.add_argument('-m', '--models', required=True, help='Number of models in the trajectory.')
    args = parser.parse_args()
    main()
