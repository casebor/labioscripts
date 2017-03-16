#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, ntpath, subprocess

#Usage: python get_from_tra.py pbd_file model_number
#                    0            1          2
#Get Inputs
input_file = sys.argv[1]
model = sys.argv[2]

#Index File
input_name = os.path.splitext(input_file)[0]
index_file = input_name + "_index.txt"

#Set Outputs
output_file = input_file[:-4] + "_M" + model + ".pdb"

#Check if Model Was Already Retrieved
if(not os.path.isfile(output_file)):
	
	#Create Index if wasn't already created
	if(not os.path.isfile(index_file)):
		print("Creating Index File From: " + input_name)
		sys.stdout.flush()
		os.system("sed -n '/MODEL/ =' " + input_file + " > " + index_file)
		print("Index from " + input_name + " created!")
	
	#Get Model
	line = subprocess.check_output("sed -n ' " + model + " 'p " + index_file, shell=True).strip()
	os.system("sed -n ' " + line + " {n; :loop /ENDMDL/ q; p; n; b loop;}' " + input_file + " > " + output_file)
