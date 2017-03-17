#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  inputMaker_v3.py
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

import protein_builder as pb, shutil, os
from optparse import OptionParser

def make_leap():
	"""
	#############################################################################
	#                                                                           #
	#  This makes the input file for tleap. For this step you must have the     #
	#  pdb of the protein and the funnil in the same place this script is.      #
	#                                                                           #
	#############################################################################
	"""
	leapIn = 'source leaprc.ff14SB_Ar\n'
	leapIn += 'prot = loadPdb %s\n' %(options.inputFile)
	leapIn += 'fun = loadPdb %s\n' %(options.funnil)
	leapIn += 'complex = combine {prot fun}\n'
	leapIn += 'saveAmberParm prot %s.prmtop %s.inpcrd\n' %(options.inputFile[:-4], options.inputFile[:-4])
	leapIn += 'saveAmberParm complex %s-%s.prmtop %s-%s.inpcrd\n' \
	%(options.inputFile[:-4], options.funnil[:-4], options.inputFile[:-4], options.funnil[:-4])
	leapIn += 'savePdb prot %s.pdb\n' %(options.inputFile[:-4])
	leapIn += 'savePdb complex %s-%s.pdb\n' %(options.inputFile[:-4], options.funnil[:-4])
	leapIn += 'quit\n'
	leapFile = open(options.outDir + 'leap.in', 'w')
	leapFile.write(leapIn)
	leapFile.close()

def make_min_input():
	"""
	#############################################################################
	#                                                                           #
	#  This makes the input file for the minimization step, if the parameters   #
	#  for the minimization are going to be changed, you must do it in the      #
	#  patternMin string.                                                       #
	#                                                                           #
	#############################################################################
	"""
	lins = patternMin.split('\n')
	# Separate the lines of the minimization pattern file
	cads = lins[3].split()
	# Create and add the mask
	cads[2] += '":1-%s,"' %(str(AA_NUM))
	# Then, we recreate the line of the file that contains the mask
	lins[3] = '    %s %s %s' %(cads[0], cads[1], cads[2])
	# And recreate the minimization file
	minIn = '\n'.join(lins)
	minFile = open(options.outDir + 'min.in', 'w')
	minFile.write(minIn)
	minFile.close()

def make_files(numFiles):
	"""
	#############################################################################
	#                                                                           #
	#  This function will make the input files for the MD, sending the          #
	#  respective restriction and restraint masks to the make_input function    #
	#  automatically. All the files created with this function will be in the   #
	#  outDir location.                                                         #
	#                                                                           #
	#############################################################################
	"""
	fileName = options.outDir + 'md-01.in'
	arch = open(fileName, 'w')
	cad = make_input('1', '0', options.temp, str(options.mdSteps), "':"+str(1+options.jump)+"-"+str(AA_NUM)+"'", '":1-'+str(AA_NUM)+'"')
	arch.write(cad)
	arch.close()
	i = 2
	while i<numFiles[0]:
		fileName = options.outDir + 'md-' + str(i).rjust(2, '0') + '.in'
		arch = open(fileName, 'w')
		cad = make_input('5', '1', options.temp, str(options.mdSteps), "':"+str(1+(options.jump*i))+"-"+str(AA_NUM)+"'", '":1-'+str(AA_NUM)+'"')
		arch.write(cad)
		arch.close()
		i += 1
	for cont in range(0, numFiles[1]):
		fileName = options.outDir + 'md-' + str(i).rjust(2, '0') + '.in'
		arch = open(fileName, 'w')
		cad = make_input('5', '1', options.temp, str(options.mdSteps), "':"+str(AA_NUM)+"'", '":1-'+str(AA_NUM)+'"')
		arch.write(cad)
		arch.close()
		i += 1
	fileName = options.outDir + 'md-' + str(i).rjust(2, '0') + '.in'
	arch = open(fileName, 'w')
	#cad = make_input('5', '1', options.temp, str(options.mdSteps*2), '', '') # Changed for 50ns at the end
	cad = make_input('5', '1', options.temp, '25000000', '', '', '-1.0')              # Changed for 50ns at the end
	arch.write(cad)
	arch.close()

def make_input(ntx, irest, temp, steps, restrM, bellyM, vlimit='20.0'):
	"""
	#############################################################################
	#                                                                           #
	#  This function makes the inputs for the Molecular Dynamics in a String    #
	#  format. ntx, irest and nscm are the same variables that you use in       #
	#  Amber; temp is the temperature, in the first step of the MD you will     #
	#  raise the temperature from 10.0 to the temperature specified in the      #
	#  input command line. Steps refers to ntslim in Amber, and this steps are  #
	#  the same for every input file for the MD, with the exception of the      #
	#  last input file that does not have any restriction and the number of     #
	#  steps is the double of the others. restrM and bellyM are the restraint   #
	#  and restriction masks for Amber respectivelly.All the parameters are     #
	#  treated as Strings.                                                      #
	#                                                                           #
	#############################################################################
	"""
	lins = patternIn.split('\n')
	i = 0
	while i<len(lins):
		if 'ntx=' in lins[i]:
			cads = lins[i].split()
			cads[0] += ntx + ','
			cads[1] += irest + ','
			lins[i] = '    '
			lins[i] += ' '.join(cads)
		elif 'ibelly=' in lins[i]:
			cads = lins[i].split()
			if len(bellyM)>0:
				cads[0] += '1,'
				cads[4] += bellyM + ','
				if len(restrM)>0:
					cads[1] += '1,'
					cads[3] += restrM + ','
				else:
					cads[1] += '0,'
					cads[2] = ''
			else:
				cads[0] += '0,'
				cads[1] += '0,'
				cads[2], cads[3], cads[4] = '', '', ''
			lins[i] = '    '
			lins[i] += ' '.join(cads)
		elif 'nstlim=' in lins[i]:
			cads = lins[i].split()
			cads[0] += steps + ','
			if len(bellyM)>0:
				cads[1] += '0,'
			else:
				cads[1] += options.nscm + ','
			lins[i] = '    '
			lins[i] += ' '.join(cads)
		elif 'tempi=' in lins[i]:
			cads = lins[i].split()
			if ntx=='1':
				cads[1] += '10.0,'
			else:
				cads[1] += temp + ','
			cads[2] += temp + ','
			lins[i] = '    '
			lins[i] += ' '.join(cads)
		elif 'vlimit=' in lins[i]:
			lins[i] += vlimit + ','
		i += 1
	mdIn = '\n'.join(lins)
	return mdIn

def make_script(numFiles):
	"""
	#############################################################################
	#                                                                           #
	#  This function creates a bash script for the MD simulation to run         #
	#  sequencially without paralellization using sander.                       #
	#                                                                           #
	#############################################################################
	"""
	# First we run the minimization step
	scri = """#!/bin/bash\n
# Script made automatically for the MD simulation,
# if you are going to use paralellization, just add the
# command to the beggining of every sander order.
	
clear
tleap -f leap.in

"""
	scri += options.prog + ' -O -i min.in -o min.out -r min.rst -c '
	# protFun is the name of the protein-funnel complex
	protFun = '%s-%s' %(options.inputFile[:-4], options.funnil[:-4])
	nJump = str(options.jump*jumpFactor)
	scri += '%s.inpcrd -p %s.prmtop -ref %s.inpcrd\n\n' %(protFun, protFun, protFun)
	# Move all the X.X coordinates of the protein atoms to make it enter the funnil. See 
	# moveX.py for more information
	scri += 'moveX.py -f min.rst -n %s -p %s\n' %(nJump, options.inputFile)
	# Now we move on with all the steps for the md simulation
	scri += options.prog + ' -O -i md-01.in -o md-01.out -c min.rst -p %s.prmtop -r md-01.rst -x md-01.nc -ref min.rst\n\n' %(protFun)
	# Variable i will contain the cycle number of the simulation, this is, represents the total
	# number of cycles the simulation will have. It starts in 1, not 0!!!
	i = 2
	tope = numFiles[0]
	if not numFiles[2]:
		tope -= 1
	while i<tope:
		scri += 'moveX.py -f md-%s.rst -n %s -p %s\n' %(str(i-1).rjust(2, '0'), nJump, options.inputFile)
		scri += options.prog + ' -O -i md-%s.in -o md-%s.out -c md-%s.rst -p %s.prmtop -r md-%s.rst -x md-%s.nc -ref md-%s.rst\n\n'\
		 %(str(i).rjust(2, '0'), str(i).rjust(2, '0'), str(i-1).rjust(2, '0'), protFun, str(i).rjust(2, '0'), str(i).rjust(2, '0'), str(i-1).rjust(2, '0'))
		i += 1
	# In the last cycle of the simulation, we want to make the protein move trough the tunnel just 
	# the perfect distance; depending of the number of aminoacids remaining, we are going to multuply
	# this number with the factor (jumpFactor) to get the desired distance.
	if numFiles[2] == True:
		scri += 'moveX.py -f md-%s.rst -n %s -p %s\n'\
		 %(str(i-1).rjust(2, '0'), str((options.jump-1)*jumpFactor), options.inputFile)
		tope = numFiles[1] - 1
	else:
		scri += 'moveX.py -f md-%s.rst -n %s -p %s\n'\
		 %(str(i-1).rjust(2, '0'), str((AA_NUM%options.jump)*jumpFactor), options.inputFile)
		tope = numFiles[1]
	scri += options.prog + ' -O -i md-%s.in -o md-%s.out -c md-%s.rst -p %s.prmtop -r md-%s.rst -x md-%s.nc -ref md-%s.rst\n\n'\
	 %(str(i).rjust(2, '0'), str(i).rjust(2, '0'), str(i-1).rjust(2, '0'), protFun, str(i).rjust(2, '0'), str(i).rjust(2, '0'), str(i-1).rjust(2, '0'))
	i += 1
	# Add more steps of simulation in order to make the protein go trough the funnil channel, 
	# depending of the lenght of the tunnel, this adds more or less steps
	for k in range(0, tope):
		scri += 'moveX.py -f md-%s.rst -n %s -p %s\n'\
		 %(str(i-1).rjust(2, '0'), nJump, options.inputFile)
		scri += options.prog + ' -O -i md-%s.in -o md-%s.out -c md-%s.rst -p %s.prmtop -r md-%s.rst -x md-%s.nc -ref md-%s.rst\n\n'\
		 %(str(i).rjust(2, '0'), str(i).rjust(2, '0'), str(i-1).rjust(2, '0'), protFun, str(i).rjust(2, '0'), str(i).rjust(2, '0'), str(i-1).rjust(2, '0'))
		i += 1
	# Make the new restart file, modifying the number of atoms
	scri += 'restartProteinExtractor.py -f md-%s.rst -r %s.inpcrd -o md-%s-noFun.rst\n\n'\
	 %(str(i-1).rjust(2, '0'), options.inputFile[:-4], str(i-1).rjust(2, '0'))
	# After we have finished with the md cycles of the protein-funnil complex, we add one more cycle 
	# for the protein to fold alone, this step uses a different topology and the modified restart file
	scri += '#' + options.prog + ' -O -i md-%s.in -o md-%s.out -c md-%s-noFun.rst -p %s.prmtop -r md-%s.rst -x md-%s.nc -ref md-%s-noFun.rst\n\n'\
	 %(str(i).rjust(2, '0'), str(i).rjust(2, '0'), str(i-1).rjust(2, '0'), options.inputFile[:-4], str(i).rjust(2, '0'), str(i).rjust(2, '0'), str(i-1).rjust(2, '0'))
	# Join all the complex protein-funnil trajectory files into one alone. See joinTraj_v0.py for
	# information of this script
	scri += 'joinTraj.py %s.nc %s.prmtop ' %(protFun, protFun)
	for l in range(1, i):
		scri += 'md-%s.nc ' %(str(l).rjust(2, '0'))
	elem = ','.join(options.funnil.split('.')[0].split('-')[1:])
	scri += '\ncare_extract-cpptraj.sh -p %s.prmtop -y %s.nc -e %s -o %s.nc' %(protFun, protFun, elem, options.inputFile[:-4])
	scri += '\n\n'
	# make directories for separate all the files generated till now
	scri += 'mkdir trajec mdout\n'
	scri += 'mv *.nc trajec\n'
	scri += 'mv *.out mdout\n\n'
	# Finally create the script in the output directory
	archScri = open(options.outDir + 'script.x', 'w')
	archScri.write(scri)
	archScri.close()

def main():
	try:
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
		archIn = open(options.inputFile, 'r')
		protSeq = pb.get_seq(options.inputFile)
		prot = pb.crt_body(protSeq)
		archOut = open(options.outDir + options.inputFile, 'w')
		archOut.write(prot)
		archOut.close()
		shutil.copyfile(options.funnil, options.outDir + options.funnil)
		global AA_NUM
		AA_NUM = len(protSeq)
		make_min_input()
		if AA_NUM%options.jump == 0:
			numFiles = int((AA_NUM)/options.jump), int(options.length/(jumpFactor*options.jump))+2, True
		else:
			numFiles = int((AA_NUM)/options.jump)+1, int(options.length/(jumpFactor*options.jump))+1, False
		make_files(numFiles)
		make_leap()
		make_script(numFiles)
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
	except IOError as ioe:
		print 'The output Directory does not exist!!!\nMake sure that you have written a valid direction.'
		print ioe
	#except NameError as ne:
	#	print ne
	#except TypeError as te:
	#	print te
	return 0

if __name__ == '__main__':

	usage = 'usage: \"%prog [options] args\"'
	parser = OptionParser(usage)
	parser.add_option('-o', '--out', action='store', type='string', dest='outDir', help='Defines the name of your output directory. Default is ./')
	parser.add_option('-j', '--jump', action='store', type='int', default=4, dest='jump', help='The number of aminoacids that you want to jump per simulation cycle. Default is 4.')
	parser.add_option('-n', '--nscm', action='store', type='string', default='5000', dest='nscm', help='Number of steps for the remotion of movement of center of mass in the last cycleof the simulation. Default is 5000 steps.')
	parser.add_option('-s', '--steps', action='store', type='int', dest='mdSteps', help='The number of steps for every cycle in the Molecular Dynamics simulation.')
	parser.add_option('-i', '--input', action='store', type='string', dest='inputFile', help='The .pdb file that you are going to use in you Molecular Dynamics simulation.')
	parser.add_option('-l', '--lenght', action='store', type='float', default=70.0, dest='length', help='This command is optional, it represents the length of the funnel. Default is 70.0 A.')
	parser.add_option('-f', '--funnil', action='store', type='string', dest='funnil', help='The pdb file with the funnil.')
	parser.add_option('-p', '--program', action='store', type='string', default='sander', dest='prog', help='The binary used to run the simulation, can be defined as "sander", "pmemd" or "pmemd.cuda.MPI". Default "sander".')
	parser.add_option('-t', '--temperature', action='store', type='string', dest='temp', help='This is the final temperature that your system is going to reach in the simulation.')
	(options, args) = parser.parse_args()
	
	global patternIn, patternMin, jumpFactor, patternEnergy
	patternIn = """# Input md file generated automatically

 &cntrl
    imin=0,
    ntx= irest= ntrx=1,
    ntxo=1, ntpr=500, ntave=0, ntwr=10000,
    iwrap=0, ntwx=500, ntwv=0, ioutfm=1, ntwe=0,
    ibelly= ntr= restraint_wt=1.0, restraintmask= bellymask=

    nstlim= nscm= t=0.0, dt=0.002, nrespa=1,
    ntt=2, tempi= temp0= ig=71277, tautp=5.0,
    gamma_ln=0, vlimit=

    ntp=0, pres0=1.0, comp=44.6, taup=1.0,

    ntc=2, tol=0.00001, jfastw=0,

    ntf=2, ntb=0, dielc=1.0, cut=9.0, nsnb=10,

    igb=1, intdiel=1.0, extdiel=78.5, saltcon=0.0, rgbmax=10.0,
    rbornstat=0, offset=0.09, gbsa=1, surften=0.005,      
    nmropt=0,
/
 &wt TYPE='END'
 /
"""
	patternMin = """# Input minimization file generated automatically
 &cntrl
    imin=1, ntx=1, irest=0, ntpr=10, ntwr=250, ntwprt=0,
    ibelly=1, ntr=0, bellymask=
    maxcyc=500, ncyc=100, ntmin=1, dx0=0.01, drms=0.0001,
    ntc=1, ntf=1, ntb=0, cut=15, igb=1, saltcon=0.0, rgbmax=10.0,
    gbsa=1, surften=0.005, rdt=0.00
 &end
"""
	patternEnergy = """# Energy calculation file
 &cntrl
    imin=5,
    ntx=1, irest=0, ntrx=1,
    ntpr=50, ntwr=0,
    iwrap=0, ntwx=0, ntwv=0, ioutfm=1, ntwe=0,
    ibelly=0, ntr=0,

    t=0.0, dt=0.002, nrespa=1,
    ntt=2, ig=71277, tautp=5.0,
    gamma_ln=0, vlimit=20.0,

    ntp=0, pres0=1.0, comp=44.6, taup=1.0,
    
    ntc=2, tol=0.00001, jfastw=0,

    ntf=2, ntb=0, dielc=1.0, cut=999.0, nsnb=10,

    igb=1, intdiel=1.0, extdiel=78.5, saltcon=0.0, rgbmax=10.0,
    rbornstat=0, offset=0.09, gbsa=1, surften=0.005,
    nmropt=0,
 &end
"""
	jumpFactor = 3.73663
	
	main()








