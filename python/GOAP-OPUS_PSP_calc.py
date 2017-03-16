#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from os import path

# Usage: %GOAP-OPUS-PSP_calc.py traj.pdb n#_models
#                0                 1         2

def main():
    
	#OPUS_PSP# First create the config.psp file (needed for the program to work :S)
	#OPUS_PSP# Depending of where the OPUS_PSP directory is, change the write comand
	#temp = open('config.psp', 'w')
	#temp.write('/home/tars/Programs/OPUS_PSP/energy_dir/')
	#temp.close()
	
	#OPUS_PSP# The content of the input file for the OPUS_PSP program
	#OPUS_PSP# containing the list of pdb's
	pdb_list = ''

	#GOAP# The pattern for the .inp file for GOAP program,
	#GOAP# we asume that the pdb's are in this working directory
	patt = '/home/tars/Programs/goap-alone/ ./\n'

	#Get Base File Name
	input_name = os.path.splitext(sys.argv[1])[0]
	model_name = "../Models/" + os.path.basename(input_name) + "_M"

	# Generate the input file for the GOAP program to run (Normal for should be 1 - 50001)
	for model in range(1, int(sys.argv[2]) + 1):

		#OPUS_PSP# Add the name to the list in OPUS_PSP
		pdb_list += os.path.basename(model_name) + str(model) + '.dat\n'

		#GOAP# Add the filenames to the input file for GOAP
		patt += os.path.basename(model_name) + str(model) + '.dat\n'

		#GOAP# Remove the Hydrogens of the pdb (optional)
		os.system('phenix.trim_pdb ' + model_name + str(model) + '.dat')

		#GOAP# Move the pdb file without the H's to the working directory (where this python script is located) and change the name
		os.system('mv ' + os.path.basename(model_name) + str(model) + '_no_h.pdb ' + os.path.basename(model_name) + str(model) + ".dat")


	# Create the input file for GOAP
	goap_file = os.path.basename(input_name) + "_GOAP.inp"
	goap_in = open(goap_file, 'w')
	goap_in.write(patt)
	goap_in.close()

	# Create the input file for OPUS_PSP
	opus_psp_file = os.path.basename(input_name) + "_OPUS_PSP.inp"
	psp_in = open(opus_psp_file, 'w')
	psp_in.write(pdb_list)
	psp_in.close()

	# Check Results Directory
	directory = "../Results/GOAP_OPUS_PSP/"

	if (not os.path.exists(directory)):
    		os.makedirs(directory)

	# Set GOAP Output File
	goap_output = directory + os.path.basename(input_name) + "_GOAP.dat"

	if(os.path.isfile(goap_output)):
		os.system("rm " + goap_output)

	# Set OPUS Output File
	opus_output = directory + os.path.basename(input_name) + "_OPUS_PSP.dat"

	if(sys.argv[2] == 1):
		os.system("rm " + opus_output)
		os.system("rm " + goap_output)

	# Run GOAP
	os.system("goap < " + goap_file + " >> " + goap_output)

	# Run OPUS_PSP
	os.system("opus_psp < " + opus_psp_file + " | grep '" + path.basename(sys.argv[1])[:6] + "' >> " + opus_output)

	# Delete Temporary Files
	os.system("rm " + goap_file)
	os.system("rm " + opus_psp_file)

	for model in range(1, int(sys.argv[2]) + 1):
		os.system("rm " + os.path.basename(model_name) + str(model) + ".dat")

	#Finally...	
	return 0

if __name__ == '__main__':
    main()
















