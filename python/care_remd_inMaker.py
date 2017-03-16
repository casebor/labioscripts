#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_remd_inMaker.py
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

import protein_builder as pb
import infile_maker as im
from os       import system, path
from shutil   import copyfile
from optparse import OptionParser



def make_files(num_files):
    """
    ##################################################################################
    #                                                                                #
    #  This function will make the input files for the REMD with the respective      #
    #  restriction and restraint masks automatically.                                #
    #  All the files created with this function will be in the out_dir location.     #
    #                                                                                #
    ##################################################################################
    """
    global JUMP_FACTOR, AA_NUM, TEMPS, CYCLES, PARMTOP, PROT_SEQ, DISANG, PROT_ATMS, SEED_N
    # Create the pdb file in a extended conformation
    prot_body = pb.crt_body(PROT_SEQ)
    with open(options.out_dir + options.input_file, 'w') as pf:
	pf.write(prot_body)
    copyfile(options.funnel, options.out_dir + options.funnel)
    # Create the leap input file for the tleap module of Amber
    with open(options.out_dir + 'leap.in', 'w') as leap:
	leap.write(im.make_leap(options.input_file, options.funnel))
    # Create the minimization file for the initial step of the REMD
    with open(options.out_dir + 'min.mdin', 'w') as mi:
	mi.write(im.make_minin(AA_NUM))
    # Create the equilibration files
    for i,t in enumerate(TEMPS):
	name = '%sremd-000-mdin-rep.%3s' %(options.out_dir, str(i).rjust(3, '0'))
	with open(name, 'w') as tin:
	    b_mask = '":1-%s"' %(AA_NUM)
	    tin.write(im.make_mdin('1', '0', t, '10000', b_mask, b_mask, SEED_N, '1', DISANG, PROT_ATMS))
    # Group file for the equilibration step
    with open(options.out_dir + 'remd-step-000.grp', 'w') as eq_grp:
	eq_grp.write(im.make_grp_file('remd', PARMTOP, len(TEMPS), CYCLES))
	CYCLES += 1
    # Create all the input files for the REMD
    for fi in range(num_files[0]):
	b_mask = '":1-%s"' %(AA_NUM)
	r_mask = '":%s-%s"' %((CYCLES+1)*options.jump, AA_NUM)
	for i,t in enumerate(TEMPS):
	    name = '%sremd-%3s-mdin-rep.%3s' %(options.out_dir, str(CYCLES).rjust(3, '0'), str(i).rjust(3, '0'))
	    with open(name, 'w') as tin:
		tin.write(im.make_remdin(t, options.md_steps, r_mask, b_mask, DISANG, SEED_N, options.exchg, PROT_ATMS))
	grp_file = '%sremd-step-%3s.grp' %(options.out_dir, str(CYCLES).rjust(3, '0'))
	with open(grp_file, 'w') as grp:
	    grp.write(im.make_grp_file('remd', PARMTOP, len(TEMPS), CYCLES))
	CYCLES += 1
    for fi in range(num_files[1]):
	b_mask = '":1-%s"' %(AA_NUM)
	r_mask = '":%s"' %(AA_NUM)
	for i,t in enumerate(TEMPS):
	    name = '%sremd-%3s-mdin-rep.%3s' %(options.out_dir, str(CYCLES).rjust(3, '0'), str(i).rjust(3, '0'))
	    with open(name, 'w') as tin:
		tin.write(im.make_remdin(t, options.md_steps, r_mask, b_mask, DISANG, SEED_N, options.exchg, PROT_ATMS))
	grp_file = '%sremd-step-%3s.grp' %(options.out_dir, str(CYCLES).rjust(3, '0'))
	with open(grp_file, 'w') as grp:
	    grp.write(im.make_grp_file('remd', PARMTOP, len(TEMPS), CYCLES))
	CYCLES += 1

def make_script(num_files):
    """
    ##################################################################################
    #                                                                                #
    #  This function creates a bash script for the REMD simulation to run            #
    #  sequencially without paralellization using Amber.                             #
    #                                                                                #
    ##################################################################################
    """
    global JUMP_FACTOR, AA_NUM, TEMPS, CYCLES, PARMTOP, PROT_SEQ, DISANG
    script = """#!/bin/bash\n
# Script made automatically for the REMD simulation,
# if you are going to use paralellization, just add the
# command to the beggining of every sander order.
	
clear
tleap -f leap.in

"""
    # Create the Chilarities restraint file
    script += 'makeCHIR_RST %s %s.chir\n' %(options.input_file, options.input_file[:-4])
    # protFun is the name of the protein-funnel complex
    prot_fun = '%s-%s' %(options.input_file[:-4], options.funnel[:-4])
    # Run the minimization step
    script += 'pmemd -O -i min.mdin -o min.out -r min.rst -c %s.inpcrd -p %s.prmtop -ref %s.inpcrd\n\n'\
			     %(prot_fun, prot_fun, prot_fun)
    # n_jump is the distance that the protein is going to move on the X axis through the funnel
    n_jump = str(options.jump*JUMP_FACTOR)
    # Move all the X.X coordinates of the protein atoms to make it enter the funnil. See 
    # moveX.py for more information
    script += 'moveX.py -f min.rst -n %s -p %s\n' %(n_jump, options.input_file)
    # Run the equilibration step
    script += 'mpirun -n %s pmemd.MPI -ng %s -rem 0 -remlog remd-000.log -groupfile remd-step-000.grp\n\n'\
	      %(len(TEMPS)*2, len(TEMPS))
    # Run all the remd steps in the beginning of the funnel
    for i in range(1, num_files[0]):
	for j,t in enumerate(TEMPS):
	    name = 'remd-%3s-rep-%3s' %(str(i-1).rjust(3, '0'), str(j).rjust(3, '0'))
	    script += 'moveX.py -f %s.rst -n %s -p %s\n' %(name, n_jump, options.input_file)
	script += 'mpirun -n %s pmemd.MPI -ng %s -rem 1 -remlog remd-%3s.log -groupfile remd-step-%3s.grp\n\n'\
		  %(len(TEMPS)*2, len(TEMPS), str(i).rjust(3, '0'), str(i).rjust(3, '0'))
    # The last step is a bit different if the division between the AA_NUM and the 
    # JUMP_FACTOR is not exact
    if AA_NUM%options.jump != 0:
	n_jump = str((AA_NUM%options.jump)*JUMP_FACTOR)
    for j,t in enumerate(TEMPS):
	    name = 'remd-%3s-rep-%3s' %(str(num_files[0]-1).rjust(3, '0'), str(j).rjust(3, '0'))
	    script += 'moveX.py -f %s.rst -n %s -p %s\n' %(name, n_jump, options.input_file)
    script += 'mpirun -n %s pmemd.MPI -ng %s -rem 1 -remlog remd-%3s.log -groupfile remd-step-%3s.grp\n\n'\
	      %(len(TEMPS)*2, len(TEMPS), str(num_files[0]).rjust(3, '0'), str(num_files[0]).rjust(3, '0'))
    # Run all the remd steps through the funnel, we move the jump option defined, but
    # maintain only the las aminoacid fixed
    n_jump = str(options.jump*JUMP_FACTOR)
    for i in range(num_files[0], CYCLES-1):
	for j,t in enumerate(TEMPS):
	    name = 'remd-%3s-rep-%3s' %(str(i).rjust(3, '0'), str(j).rjust(3, '0'))
	    script += 'moveX.py -f %s.rst -n %s -p %s\n' %(name, n_jump, options.input_file)
	script += 'mpirun -n %s pmemd.MPI -ng %s -rem 1 -remlog remd-%3s.log -groupfile remd-step-%3s.grp\n\n'\
		  %(len(TEMPS)*2, len(TEMPS), str(i+1).rjust(3, '0'), str(i+1).rjust(3, '0'))
    # make directories for separate all the files generated till now
    script += 'mkdir trajec mdout mdinfo_files\n'
    script += 'mv *-nc-* trajec\n'
    script += 'mv *-mdinfo-* mdinfo_files\n'
    script += 'mv *-mdout-* mdout\n\n'
    return script

def main():
    try:
	global JUMP_FACTOR, AA_NUM, TEMPS, CYCLES, PARMTOP, PROT_SEQ, DISANG, PROT_ATMS, SEED_N
	JUMP_FACTOR = 3.73663
	SEED_N = str(options.seed_n)
	# First step, we make sure that the output directory exists, if does not, 
	# we make one with the supplied name
	if not path.exists(options.out_dir):
	    print 'The specified directory does not exists, \n\
	    I will make one directory with the specified name...'
	    system('mkdir %s' %(options.out_dir))
	    options.out_dir += '/'
	else:
	    print 'The specified directory exists, \n\
	    All the files with the same name will be replaced...'
	    if options.out_dir[-1] != '/':
		options.out_dir += '/'
	PROT_SEQ  = pb.get_seq(options.input_file)
	PROT_ATMS = str(len(pb.get_atoms(options.input_file)))
	AA_NUM    = len(PROT_SEQ)
	TEMPS     = options.temps.split(',')
	CYCLES    = 0
	PARMTOP   = options.input_file[:-4] + '-' + options.funnel[:-4]
	DISANG    = options.input_file[:-4] + '.chir'
	# Description of num_files: 
	#	1st --> Number of aa adition CYCLES at the beggining of the funnel
	#	2nd --> Number of CYCLESs tha the protein pass through the funnel
	if AA_NUM%options.jump == 0:
	    num_files = int(AA_NUM/options.jump)-1, int(options.length/(JUMP_FACTOR*options.jump))+2
	else:
	    num_files = int(AA_NUM/options.jump), int(options.length/(JUMP_FACTOR*options.jump))+1
	make_files(num_files)
	with open('%sscript.sh' %(options.out_dir), 'w') as sc:
	    sc.write(make_script(num_files))
	system('chmod 777 %sscript.sh' %(options.out_dir))
	msg = """
	############################################################################
	#                                                                          #
	#  Generating the input files, topology files, pdb files ......            #
	#  Generating the script to use in the terminal ......                     #
	#  Given the permissions needed to the script ......                       #
	#  Done!!!                                                                 #
	#  All the files needed for the simulation were created,                   #
	#  now you just have to type './script.x' in a terminal where you set      #
	#  the -o flag and that's all.                                             #
	#                                                                          #
	############################################################################
	"""
	print(msg)
    except IOError as ioe:
	print('Some input file(s) does not exist!!!\nMake sure that you have written a valid file.')
	print(ioe)
    #except NameError as ne:
    #	print ne
    #except TypeError as te:
    #	print te
    return 0

if __name__ == '__main__':

    usage = 'usage: \"%prog [options] args\"'
    parser = OptionParser(usage)
    parser.add_option('-o', '--out', action='store', type='string', dest='out_dir', default='out_dir',
		      help='Defines the name of your output directory. Default is out_dir')
    parser.add_option('-j', '--jump', action='store', type='int', default=1, 
		      dest='jump', help='The number of aminoacids that you want to jump per simulation CYCLES. Default is 1.')
    parser.add_option('-n', '--nscm', action='store', type='string', default='1000', 
		      dest='nscm', help='Number of steps for the remotion of movement of center of mass in the last CYCLESof the simulation. Default is 1000 steps.')
    parser.add_option('-s', '--steps', action='store', type='string', dest='md_steps', 
		      help='The number of steps for every exchange CYCLES in the REMD simulation.')
    parser.add_option('-i', '--input', action='store', type='string', dest='input_file', 
		      help='The .pdb file that you are going to use in you Molecular Dynamics simulation.')
    parser.add_option('-l', '--lenght', action='store', type='float', default=70.0, 
		      dest='length', help='This command is optional, it represents the length of the funnel. Default is 70.0 A.')
    parser.add_option('-f', '--funnil', action='store', type='string', dest='funnel', 
		      help='The pdb file with the funnil.')
    parser.add_option('-t', '--temperatures', action='store', type='string', 
		      dest='temps', help='Define the temperatures for your REMD simulation putting all together and comma separated. Example: temp1.0,temp1.1,temp2.1,temp2.2')
    parser.add_option('-e', '--exchange', action='store', type='string', default='250', 
		      dest='exchg', help='Defines the number of exchanges for the simulation. The default value is 250 steps. You have to be careful, because the exchange number times the steps is going to be the total simulation time.')
    parser.add_option('-g', '--seed', action='store', type='int', dest='seed_n', default=71277, help='The seed number for the simulations, the default is 71277.')
    (options, args) = parser.parse_args()
    
    main()








