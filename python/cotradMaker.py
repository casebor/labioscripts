#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cotradMaker.py
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

import proteinMaker as pm, shutil, os
from optparse import OptionParser

def make_leap(numComp):
	"""
	#############################################################################
	#                                                                           #
	#  This makes the input file for tleap. For this step you must have the     #
	#  pdb of the protein and the funnil in the same place this script is.      #
	#                                                                           #
	#############################################################################
	"""
	leapIn = 'source leaprc.ff14SB_Ar\n'
	leapIn += 'protein = loadPdb %s\n' %(options.inputFile)
	leapIn += 'fun = loadPdb %s\n' %(options.funnil)
	leapIn += 'complex = combine {protein fun}\n'
	# We make all the complexes of protein fragment - funnel, depending of numComp
	for i in range(1, numComp):
		leapIn += 'prot-%s = loadPdb prot-%s.pdb\n' %(str(i).rjust(3, '0'), str(i).rjust(3, '0'))
		leapIn += 'comp-%s = combine {prot-%s fun}\n' %(str(i).rjust(3, '0'), str(i).rjust(3, '0'))
		leapIn += 'saveAmberParm comp-%s comp-%s.prmtop comp-%s.inpcrd\n'\
		 %(str(i).rjust(3, '0'), str(i).rjust(3, '0'), str(i).rjust(3, '0'))
		leapIn += 'savePdb prot-%s prot-%s.pdb\n' %(str(i).rjust(3, '0'), str(i).rjust(3, '0'))
	leapIn += 'saveAmberParm protein %s.prmtop %s.inpcrd\n' %(options.inputFile[:-4], options.inputFile[:-4])
	leapIn += 'savePdb protein %s.pdb\n' %(options.inputFile[:-4])
	leapIn += 'saveAmberParm complex complex-%s.prmtop complex-%s.inpcrd\n'\
	 %(options.inputFile[:-4], options.inputFile[:-4])
	leapIn += 'saveAmberParm fun %s.prmtop %s.inpcrd\n' %(options.funnil[:-4], options.funnil[:-4])
	leapIn += 'quit\n'
	leapFile = open(options.outDir + 'leap.in', 'w')
	leapFile.write(leapIn)
	leapFile.close()

def make_comp_files(aaSeq, numComp):
	"""
	#############################################################################
	#                                                                           #
	#  This function generates the pdb files of the protein with                #
	#  different lenghts                                                        #
	#                                                                           #
	#############################################################################
	"""
	for i in range(1, numComp):
		aaTemp = aaSeq[0:options.jump*i]
		compTemp = open(options.outDir + 'prot-%s.pdb'%(str(i).rjust(3, '0')), 'w')
		compTemp.write(pm.crt_body(aaTemp))
		compTemp.close()

def make_input_files(aaSeq, numComp):
	"""
	#############################################################################
	#                                                                           #
	#  This function generates all the Amber input files to use, every input    #
	#  file is used in one cycle of simulation, this function includes the      #
	#  minimization and energy calculation inputs                               #
	#                                                                           #
	#############################################################################
	"""
	if not os.path.exists(options.outDir):
		os.system('mkdir %s' %(options.outDir))
	# Minimization file
	minList = PATTERN_MIN.split('\n')
	minList[3] += '":%s-%s",' %(1, len(aaSeq))
	minFile = open(options.outDir + 'min.in', 'w')
	minFile.write('\n'.join(minList))
	minFile.close()
	# Minimization file
	# Prequel simulation step, only for the protein
	mdList = PATTERN_IN.split('\n')
	mdList[4]  = '	ntx=1, irest=0, ntrx=1,'
	mdList[7]  = '	ibelly=1, ntr=1, restraint_wt=1.0, restraintmask=\':1-%s\', bellymask=":1-%s",' %(len(aaSeq), len(aaSeq))
	mdList[9]  = '	nstlim=10000, nscm=10000, t=0.0, dt=0.002, nrespa=1,'
	mdList[10] = '	ntt=2, tempi=10.0, temp0=%s, ig=20247, tautp=5.0,' %(options.temp)
	mdInFile = open(options.outDir + 'md-000.in', 'w')
	mdInFile.write('\n'.join(mdList))
	mdInFile.close()
	# Prequel simulation step, only for the protein
	# All the inputs for the simulation, beggining with the size incremental steps
	i = 1
	while i < numComp:
		mdList = PATTERN_IN.split('\n')
		mdList[7]  = '	ibelly=1, ntr=1, restraint_wt=1.0, restraintmask=\':%s\', bellymask=":1-%s",' %(i * options.jump, i * options.jump)
		mdList[9]  = '	nstlim=%s, nscm=10000, t=0.0, dt=0.002, nrespa=1,' %(options.mdSteps)
		#mdList[9]  = '	nstlim=%s, nscm=10000, t=0.0, dt=0.002, nrespa=1,' %(options.mdSteps * i * options.jump)
		mdList[10] = '	ntt=2, tempi=%s, temp0=%s, ig=20247, tautp=5.0,' %(options.temp, options.temp)
		mdInFile = open(options.outDir + 'md-%s.in' %(str(i).rjust(3, '0')), 'w')
		mdInFile.write('\n'.join(mdList))
		mdInFile.close()
		i += 1
	# Only one incremental step remains, but we will merge it into the steps that the simulation
	# uses for the protein make it trought the funnel channel. Now we make the md inputs for the 
	# protein to go through the funnel, this depends of the jump and the length of the funnel number
	# of steps = funnel length / (jump * JUMP_FACTOR)
	lim = int(options.length/(options.jump*JUMP_FACTOR)) + 1 + i
	while i < lim:
		mdList = PATTERN_IN.split('\n')
		mdList[7]  = '	ibelly=1, ntr=1, restraint_wt=1.0, restraintmask=\':%s\', bellymask=":1-%s",' %(len(aaSeq), len(aaSeq))
		mdList[9]  = '	nstlim=%s, nscm=10000, t=0.0, dt=0.002, nrespa=1,' %(options.mdSteps)
		#mdList[9]  = '	nstlim=%s, nscm=10000, t=0.0, dt=0.002, nrespa=1,' %(options.mdSteps * len(aaSeq))
		mdList[10] = '	ntt=2, tempi=%s, temp0=%s, ig=20247, tautp=5.0,' %(options.temp, options.temp)
		mdInFile = open(options.outDir + 'md-%s.in' %(str(i).rjust(3, '0')), 'w')
		mdInFile.write('\n'.join(mdList))
		mdInFile.close()
		i += 1
	# The last input file it's a clasic molecular dynamics step, without the funnel and the steps
	# of simulation are the double of the normal ones (ESTO AUN NO ESTA TOTALMENTE DECIDIDO!!!)
	mdList = PATTERN_IN.split('\n')
	mdList[7]  = '	ibelly=0, ntr=0,'
	mdList[9]  = '	nstlim=%s, nscm=500, t=0.0, dt=0.002, nrespa=1,' %(options.mdSteps * 2)
	#mdList[9]  = '	nstlim=%s, nscm=500, t=0.0, dt=0.002, nrespa=1,' %(options.mdSteps * len(aaSeq) * 2)
	mdList[10] = '	ntt=2, tempi=%s, temp0=%s, ig=20247, tautp=5.0,' %(options.temp, options.temp)
	mdInFile = open(options.outDir + 'md-%s.in' %(str(i).rjust(3, '0')), 'w')
	mdInFile.write('\n'.join(mdList))
	mdInFile.close()
	# Now the only input file left is the energy calculation input, don't need any changes
	mdInFile = open(options.outDir + 'energy.in', 'w')
	mdInFile.write(PATTERN_ENERGY)
	mdInFile.close()
	
def make_script(aaSeq, numComp):
	"""
	#############################################################################
	#                                                                           #
	#  This function creates a bash script for the MD simulation to run         #
	#  sequencially without parallelization using sander                        #
	#                                                                           #
	#############################################################################
	"""
	# First we make the minimization step
	scri = """#!/bin/bash
# Script made automatically for the MD simulation,
# if you are going to use paralellization, just add the
# command to the beggining of every sander order.

clear
tleap -f leap.in

sander -O -i min.in -o min.out -r min.restrt -c """
	# Now add all the orders sequentially
	scri += '%s.inpcrd -p %s.prmtop\n' %(options.inputFile[:-4], options.inputFile[:-4])
	# We increase the temperature of the protein till reach the final temperature, this file will
	# serve to take the atom coordinates and velocities in the incremental part of the simulation
	scri += 'sander -O -i md-000.in -o md-000.out -c min.restrt -p %s.prmtop -r %s.restrt -x %s.nc -ref min.restrt\n'\
	 %(options.inputFile[:-4], options.inputFile[:-4], options.inputFile[:-4])
	scri += '> md-000.restrt\n\n'
	jumpDist = JUMP_FACTOR * options.jump
	# First we move the protein through the x-axis
	# %(options.inputFile[:-4], options.inputFile[:-4], options.jump - 1, options.funnil[:-4])
	# We begin the incremental size steps of the simulation
	i = 1
	#atmsProt = get_num_atoms(options.inputFile[:-4]+'.inpcrd')
	#atmsFun = get_num_atoms(options.funnil[:-4]+'.inpcrd')
	while i < numComp:
		scri += 'moveX.py -f %s.restrt -n %s -p %s.pdb\n' %(options.inputFile[:-4], jumpDist, options.inputFile[:-4])
		#atmsComp = get_num_atoms('comp-%s.inpcrd' %(str(i).rjust(3, '0')))
		#atmsToMove = atmsComp - atmsFun
		scri += 'moveX.py -f md-%s.restrt -n %s -p prot-%s.pdb\n' %(str(i-1).rjust(3, '0'), jumpDist, str(i-1).rjust(3, '0'))
		scri += 'restartMaker.py %s.restrt %s.prmtop md-%s.restrt %s %s %s.inpcrd 0\n'\
		 %(options.inputFile[:-4], options.inputFile[:-4], str(i-1).rjust(3, '0'), str((i-1)*options.jump), str(i*options.jump - 1), options.funnil[:-4])
		scri += 'sander -O -i md-%s.in -o md-%s.out -c md-%s.restrt -p comp-%s.prmtop -r md-%s.restrt -x md-%s.nc -ref md-%s.restrt\n\n'\
		 %(str(i).rjust(3, '0'), str(i).rjust(3, '0'), str(i-1).rjust(3, '0'), str(i).rjust(3, '0'), str(i).rjust(3, '0'), str(i).rjust(3, '0'), str(i-1).rjust(3, '0'))
		i += 1
	# This is the last incremental step, we make it separated of the others to avoid complications 
	# in the code, if you can change it to work.... JUST DO IT!!!
	jumpTemp = JUMP_FACTOR * (len(aaSeq) - (i-1)*options.jump)
	scri += 'moveX.py -f %s.restrt -n %s -p %s.pdb\n' %(options.inputFile[:-4], jumpTemp, options.inputFile[:-4])
	#atmsComp = get_num_atoms('comp-%s.inpcrd' %(str(i).rjust(3, '0')))
	#atmsToMove = atmsComp - atmsFun
	scri += 'moveX.py -f md-%s.restrt -n %s -p prot-%s.pdb\n' %(str(i-1).rjust(3, '0'), jumpTemp, str(i-1).rjust(3, '0'))
	scri += 'restartMaker.py %s.restrt %s.prmtop md-%s.restrt %s %s %s.inpcrd 1\n'\
	 %(options.inputFile[:-4], options.inputFile[:-4], str(i-1).rjust(3, '0'), str((i-1)*options.jump), str(len(aaSeq) - 1), options.funnil[:-4])
	scri += 'sander -O -i md-%s.in -o md-%s.out -c md-%s.restrt -p complex-%s.prmtop -r md-%s.restrt -x md-%s.nc -ref md-%s.restrt\n\n'\
	 %(str(i).rjust(3, '0'), str(i).rjust(3, '0'), str(i-1).rjust(3, '0'), options.inputFile[:-4], str(i).rjust(3, '0'), str(i).rjust(3, '0'), str(i-1).rjust(3, '0'))
	i += 1
	# This part add the steps for the protein go through the funnel channel, and the last step of 
	# the simulation is embedded here too
	lim = int(options.length/(options.jump*JUMP_FACTOR)) + i
	while i < lim + 1:
		if i == lim:
			scri += 'restartProteinExtractor.py -f md-%s.restrt -r %s.inpcrd -o md-%s-noFun.restrt\n'\
			 %(str(i-1).rjust(3, '0'), options.inputFile[:-4], str(i-1).rjust(3, '0'))
			scri += 'sander -O -i md-%s.in -o md-%s.out -c md-%s-noFun.restrt -p %s.prmtop -r md-%s.restrt -x md-%s.nc\n\n'\
			 %(str(i).rjust(3, '0'), str(i).rjust(3, '0'), str(i-1).rjust(3, '0'), options.inputFile[:-4], str(i).rjust(3, '0'), str(i).rjust(3, '0'))
		else:
			scri += 'moveX.py -f md-%s.restrt -n %s -p %s.pdb\n' %(str(i-1).rjust(3, '0'), jumpDist, options.inputFile[:-4])
			scri += 'sander -O -i md-%s.in -o md-%s.out -c md-%s.restrt -p complex-%s.prmtop -r md-%s.restrt -x md-%s.nc -ref md-%s.restrt\n\n'\
			 %(str(i).rjust(3, '0'), str(i).rjust(3, '0'), str(i-1).rjust(3, '0'), options.inputFile[:-4], str(i).rjust(3, '0'), str(i).rjust(3, '0'), str(i-1).rjust(3, '0'))
		i += 1
	scriptFile = open(options.outDir + 'script.x', 'w')
	scriptFile.write(scri)
	scriptFile.close()

def main():
	# First step, we make sure that the output directory exists, if does not, 
	# we make one with the supplied name
	if not os.path.exists(options.outDir):
		print 'The specified directory does not exists, \n\
		I will make one directory with the specified name...'
		os.system('mkdir %s' %(options.outDir))
		options.outDir += '/'
	else:
		# this step is only because I did not figured out how to solve the problem of putting
		# all the generated files in the output directory; this will be improved in newer versions
		if options.outDir[-1] != '/':
			options.outDir += '/'
	# inFile is the file that contains the protein to be simulated, can have the formats described 
	# in help (AUN FALTA ESA PARTE!!!!)
	inFile = open(options.inputFile, 'r')
	# aaSeq is the list of aminoacids of the protein in format of THREE LETTER CODE
	aaSeq = pm.get_seq(inFile)
	inFile.close()
	# If the number of residues in the protein divided by the jump defined is not an exact division, 
	# then the number of complexes pseudoProtein-funnil will be the integer part of the ratio plus one
	if (len(aaSeq)%options.jump) == 0:
		numComps = int(len(aaSeq)/options.jump)
	else:
		numComps = int(len(aaSeq)/options.jump) + 1
	# We generate the prmtop files of the protein-funnel complexes
	make_comp_files(aaSeq, numComps)
	# Make the complete protein prmtop file
	protOut = open(options.outDir + options.inputFile, 'w')
	protOut.write(pm.crt_body(aaSeq))
	protOut.close()
	# Make the leap file to use in tleap
	make_leap(numComps)
	# Generates all the input files for the simulation, including the minimization step
	make_input_files(aaSeq, numComps)
	# Now we generate the script file to run the simulation in a linux terminal
	make_script(aaSeq, numComps)
	shutil.copy(options.funnil, options.outDir + options.funnil)
	os.system('chmod 777 %sscript.x' %(options.outDir))
	
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
	print msg
	
	return 0

if __name__ == '__main__':
	
	usage = 'usage: \"%prog [options] args\"'
	parser = OptionParser(usage)
	parser.add_option('-o', '--out', action='store', type='string', dest='outDir', help='Defines the name of your output directory. Default is ./')
	parser.add_option('-j', '--jump', action='store', type='int', default=4, dest='jump', help='The number of aminoacids that you want to jump per simulation cycle. Default is 4.')
	parser.add_option('-n', '--nscm', action='store', type='string', default='250', dest='nscm', help='Number of steps for the remotion of movement of center of mass in the last cycleof the simulation. Default is 250 steps.')
	parser.add_option('-s', '--steps', action='store', type='int', dest='mdSteps', help='The number of steps for every cycle in the Molecular Dynamics simulation.')
	parser.add_option('-i', '--input', action='store', type='string', dest='inputFile', help='The .pdb file that you are going to use in you Molecular Dynamics simulation.')
	parser.add_option('-l', '--lenght', action='store', type='float', default=40.0, dest='length', help='This command is optional, it represents the length of the funnel. Default is 40.0 A.')
	parser.add_option('-f', '--funnil', action='store', type='string', dest='funnil', help='The pdb file with the funnil.')
	parser.add_option('-t', '--temperature', action='store', type='string', dest='temp', help='This is the final temperature that your system is going to reach in the simulation.')
	(options, args) = parser.parse_args()
	
	global PATTERN_IN, PATTERN_MIN, PATTERN_ENERGY, JUMP_FACTOR
	PATTERN_IN = """# Input md file generated automatically

 &cntrl
	imin=0,
	ntx=5, irest=1, ntrx=1,
	ntxo=1, ntpr=500, ntave=0, ntwr=10000,
	iwrap=0, ntwx=500, ntwv=-1, ioutfm=1, ntwe=0,
	ibelly= ntr= restraint_wt=1.0, restraintmask= bellymask=

	nstlim= nscm= t=0.0, dt=0.002, nrespa=1,
	ntt=2, tempi= temp0= ig=20247, tautp=5.0,
	gamma_ln=0, vlimit=20.0,

	ntp=0, pres0=1.0, comp=44.6, taup=1.0,

	ntc=2, tol=0.00001, jfastw=0,

	ntf=2, ntb=0, dielc=1.0, cut=999.0, nsnb=10,

	igb=1, intdiel=1.0, extdiel=78.5, saltcon=0.0, rgbmax=10.0,
	rbornstat=0, offset=0.09, gbsa=1, surften=0.005,      
	nmropt=0,
/
 &wt TYPE='END'
 /
"""
	PATTERN_MIN = """# Input minimization file generated automatically
 &cntrl
	imin=1, ntx=1, irest=0, ntpr=10, ntwr=250, ntwprt=0,
	ibelly=1, ntr=0, bellymask=
	maxcyc=500, ncyc=100, ntmin=1, dx0=0.01, drms=0.0001,
	ntc=1, ntf=1, ntb=0, cut=15, igb=1, saltcon=0.0, rgbmax=10.0,
	gbsa=1, surften=0.005, rdt=0.01
 &end
"""
	PATTERN_ENERGY = """# Energy calculation file
 &cntrl
	imin=5,
	ntx=1, irest=0, ntrx=1,
	ntpr=50, ntwr=0,
	iwrap=0, ntwx=0, ntwv=0, ioutfm=1, ntwe=0,
	ibelly=0, ntr=0,

	t=0.0, dt=0.002, nrespa=1,
	ntt=2, ig=20247, tautp=5.0,
	gamma_ln=0, vlimit=20.0,

	ntp=0, pres0=1.0, comp=44.6, taup=1.0,
	
	ntc=2, tol=0.00001, jfastw=0,

	ntf=2, ntb=0, dielc=1.0, cut=999.0, nsnb=10,

	igb=1, intdiel=1.0, extdiel=78.5, saltcon=0.0, rgbmax=10.0,
	rbornstat=0, offset=0.09, gbsa=1, surften=0.005,
	nmropt=0,
 &end
"""
	JUMP_FACTOR = 3.73663

	main()
	
