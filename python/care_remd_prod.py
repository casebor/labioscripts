#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_remd_prod.py
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
from os import system

def copy_input_file(number, destination):
    """
    """
    with open('remd-%3s-mdin-rep.%3s'%(str(args.step).rjust(3,'0'), str(number).rjust(3,'0')), 'r') as temp_in:
	out = ''
	for line in temp_in:
	    if 'ibelly' in line:
		out += '    ibelly=0, ntr=0,\n'
	    elif 'nstlim' in line:
		out += '    nstlim=500000, t=0.0, dt=0.002, nrespa=1,\n'
	    elif 'numexchg' in line:
		temp = line.split()[1]
		out += '    ntt=2, %s numexchg=50, ig=71277, tautp=5.0,\n' %(temp)
	    elif 'vlimit' in line:
		out += '    gamma_ln=0, vlimit=-1.0, nscm=10000,\n'
	    else:
		out += line
    with open('%s/remd-%3s-mdin-rep.%3s'%(destination, str(args.step+1).rjust(3,'0'), str(number).rjust(3,'0')), 'w') as temp_out:
	temp_out.write(out)

def copy_group_file(destination):
    """
    """
    out = ''
    with open('remd-step-%3s.grp'%(str(args.step).rjust(3,'0')), 'r') as grp_in:
	ts = str(args.step+1).rjust(3,'0') # This step = ts
	ps = str(args.step).rjust(3,'0') # Previous step = ps
	for i in range(args.reps):
	    rep = str(i).rjust(3,'0')
	    out += '-O -i remd-%3s-mdin-rep.%3s -o remd-%3s-mdout-rep.%3s -c remd-%3s-rep-%3s.rst -p %s -r remd-%3s-rep-%3s.rst -x remd-%3s-nc-rep.%3s -inf remd-%3s-mdinfo-rep.%3s\n'%(ts, rep, ts, rep, ps, rep, args.parm, ts, rep, ts, rep, ts, rep)
    with open('%s/remd-step-%3s.grp'%(destination, str(args.step+1).rjust(3,'0')), 'w') as grp_out:
	grp_out.write(out)

def main():
    """ Main function
    """
    system('mkdir production')
    for i in range(args.reps):
	copy_input_file(i, 'production')
	system('care_restart_protein_extractor.py -f remd-%3s-rep-%3s.rst -r %s -o production/remd-%3s-rep-%3s.rst'
	     %(str(args.step).rjust(3,'0'), str(i).rjust(3,'0'), args.ref, str(args.step).rjust(3,'0'), str(i).rjust(3,'0')))
    copy_group_file('production')
    system('cp *.chir production')
    system('cp %s production'%(args.parm))
    #system('cd production')
    #system('mpirun -n 12 pmemd.cuda.MPI -ng 6 -rem 1 -remlog remd-%3s.log -groupfile remd-step-%3s.grp'
	 #%(str(args.step+1).rjust(3,'0'), str(args.step+1).rjust(3,'0')))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add a production step to the simulations. For this script to work you need the last group and mdin files of the REMD, the chilarity file, all the last step restart files, the input coordinates and the parameter topology file of the protein alone.')
    parser.add_argument('-r', '--ref', required=True, help='The reference input file to use in the extraction. Use the inpcrd file of the protein alone.')
    parser.add_argument('-s', '--step', required=True, type=int, help='The number of the last step of the simulation.')
    parser.add_argument('-n', '--reps', required=True, type=int, help='How many replicas has the simulation.')
    parser.add_argument('-p', '--parm', required=True, help='Parameter topology file for the protein alone.')
    args = parser.parse_args()
    main()
