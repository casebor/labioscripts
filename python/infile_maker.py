#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  infile_maker.py
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

"""
    Module useful only for the creation of input files of the Amber psoftware.
    This module can create leap, minimization and molecular dynamics input files.
"""

global mdin, remdin, minin

mdin = """# Input md file generated automatically

 &cntrl
    imin=0,
    ntx= irest= ntrx=1,
    ntxo=1, ntpr=500, ntave=0, ntwr=10000,
    iwrap=0, ntwx=500, ntwv=0, ioutfm=1, ntwe=0,
    ibelly= ntr= ntwprt=

    nstlim= t=0.0, dt=0.002, nrespa=1,
    ntt=2, tempi= ig= tautp=5.0,
    gamma_ln=0, vlimit=20.0,

    ntp=0, pres0=1.0, comp=44.6, taup=1.0,

    ntc=2, tol=0.00001, jfastw=0,

    ntf=2, ntb=0, dielc=1.0, cut=999.0, nsnb=10,

    igb=1, intdiel=1.0, extdiel=78.5, saltcon=0.0, rgbmax=10.0,
    rbornstat=0, offset=0.09, gbsa=1, surften=0.005,      
    nmropt=
/
"""
remdin = """# Input remd file generated automatically

 &cntrl
    imin=0,
    ntx=5, irest=1, ntrx=1,
    ntxo=1, ntpr=500, ntave=0, ntwr=10000,
    iwrap=0, ntwx=500, ntwv=0, ioutfm=1, ntwe=0,
    ibelly= ntr= ntwprt=

    nstlim= t=0.0, dt=0.002, nrespa=1,
    ntt=2, temp0= ig= tautp=5.0,
    gamma_ln=0, vlimit=20.0,

    ntp=0, pres0=1.0, comp=44.6, taup=1.0,

    ntc=2, tol=0.00001, jfastw=0,

    ntf=2, ntb=0, dielc=1.0, cut=999.0, nsnb=10,

    igb=1, intdiel=1.0, extdiel=78.5, saltcon=0.0, rgbmax=10.0,
    rbornstat=0, offset=0.09, gbsa=1, surften=0.005,      
    nmropt=1,
 /
 &wt TYPE='END'
 /
DISANG=
"""
minin = """# Input minimization file generated automatically
 &cntrl
    imin=1, ntx=1, irest=0, ntpr=100, ntwr=250, ntwprt=0,
    ibelly=1, ntr=0,
    maxcyc=1000, ncyc=100, ntmin=1, dx0=0.01, drms=0.0001,
    ntc=1, ntf=1, ntb=0, cut=15, igb=1, saltcon=0.0, rgbmax=10.0,
    gbsa=1, surften=0.005, rdt=0.00
 &end
"""

def make_mdin(ntx, irest, temp, steps, restr_m, belly_m, ig, nmr='0', disang=None, ntwprt=None):
    """Returns a string containing the input parameters for an Amber molecular 
       simulation.
       
       All parameters are strings.
    
    ######################################################################################
    #                                                                                    #
    #  This function makes the inputs for the Molecular Dynamics in a String format,     #
    #  where ntx, irest and nscm are the same variables that you use in Amber, temp is   #
    #  the temperature (in the first step of the MD you will raise the temperature from  #
    #  10.0 to the temperature specified, steps refers to ntslim in Amber, and this      #
    #  steps should be the same for every input file for the MD. restrM and bellyM are   #
    #  the restraint and restriction masks for Amber respectivelly.                      #
    #  All the parameters are treated as Strings.                                        #
    #                                                                                    #
    ######################################################################################
    """
    lines = mdin.split('\n')
    i = 0
    while i<len(lines):
	if 'ntx=' in lines[i]:
	    parms = lines[i].split()
	    j = 0
	    while j<len(parms):
		if 'ntx' in parms[j]:
		    parms[j] += ntx + ','
		elif 'irest' in parms[j]:
		    parms[j] += irest + ','
		j += 1
	    lines[i] = '    ' + ' '.join(parms)
	elif 'ibelly' in lines[i]:
	    parms = lines[i].split()
	    j = 0
	    while j<len(parms):
		if 'ibelly' in parms[j]:
		    if len(belly_m)>0:
			parms[j] += '1, bellymask=' + belly_m + ','
		    else:
			parms[j] += '0,'
		elif 'ntr' in parms[j]:
		    if len(restr_m)>0:
			parms[j] += '1, restraint_wt=1.0, restraintmask=' + restr_m + ','
		    else:
			parms[j] += '0,'
		elif 'ntwprt' in parms[j]:
		    if ntwprt is not None:
			parms[j] += ntwprt + ','
		    else:
			parms[j] += ''
		j += 1
	    lines[i] = '    ' + ' '.join(parms)
	elif 'nstlim' in lines[i]:
	    parms = lines[i].split()
	    j = 0
	    while j<len(parms):
		if 'nstlim' in parms[j]:
		    parms[j] += steps + ','
		j += 1
	    lines[i] = '    ' + ' '.join(parms)
	elif 'tempi' in lines[i]:
	    parms = lines[i].split()
	    j = 0
	    while j<len(parms):
		if 'tempi' in parms[j]:
		    if ntx == '1':
			parms[j] += '10.0, temp0=' + temp + ','
		    else:
			parms[j] += temp + ', temp0=' + temp + ','
		if 'ig=' in parms[j]:
		    parms[j] += ig + ','
		j += 1
	    lines[i] = '    ' + ' '.join(parms)
	elif 'nmropt' in lines[i]:
	    parms = lines[i].split()
	    j = 0
	    while j<len(parms):
		if 'nmropt' in parms[j]:
		    parms[j] += nmr + ','
		j += 1
	    lines[i] = '    ' + ' '.join(parms)
	i += 1
    md_in = '\n'.join(lines)
    if nmr != '0' and disang is not None:
	md_in += '&wt TYPE=\'END\'\n /\nDISANG=' + disang
    else:
	print('Error, you did not supply a valid chilarity restriction file')
	quit()
    return md_in

def make_remdin(temp, steps, restr_m, belly_m, disang, ig, n_exchg='0', ntwprt=None):
    """Returns a string containing the input parameters for an Amber REMD 
       molecular simulation.
       
       All parameters are strings.
    
    ######################################################################################
    #                                                                                    #
    #  This function makes the inputs for the Molecular Dynamics in a String format,     #
    #  where temp is the temperature, in the first step of the MD you will raise the     #
    #  temperature from 0.0 to the temperature specified, steps refers to ntslim in      #
    #  Amber, and this steps should be the same for every input file for the REMD,       #
    #  restrM and bellyM are the restraint and restriction masks for Amber               #
    #  respectivelly.                                                                    #
    #  All the parameters are treated as Strings.                                        #
    #                                                                                    #
    ######################################################################################
    """
    lines = remdin.split('\n')
    i = 0
    while i<len(lines):
	if 'ibelly=' in lines[i]:
	    parms = lines[i].split()
	    j = 0
	    while j<len(parms):
		if 'ibelly' in parms[j]:
		    if len(belly_m)>0:
			parms[j] += '1, bellymask=' + belly_m + ','
		    else:
			parms[j] += '0,'
		elif 'ntr' in parms[j]:
		    if len(restr_m)>0:
			parms[j] += '1, restraint_wt=1.0, restraintmask=' + restr_m + ','
		    else:
			parms[j] += '0,'
		elif 'ntwprt' in parms[j]:
		    if ntwprt is not None:
			parms[j] += ntwprt + ','
		    else:
			parms[j] += ''
		j += 1
	    lines[i] = '    ' + ' '.join(parms)
	elif 'nstlim' in lines[i]:
	    parms = lines[i].split()
	    j = 0
	    while j<len(parms):
		if 'nstlim' in parms[j]:
		    parms[j] += steps + ','
		j += 1
	    lines[i] = '    ' + ' '.join(parms)
	elif 'temp0' in lines[i]:
	    parms = lines[i].split()
	    j = 0
	    while j<len(parms):
		if 'temp0' in parms[j]:
		    parms[j] += temp + ','
		    if n_exchg != '0':
			parms[j] += ' numexchg=' + n_exchg + ','
		if 'ig=' in parms[j]:
		    parms[j] += ig + ','
		j += 1
	    lines[i] = '    ' + ' '.join(parms)
	elif 'DISANG' in lines[i]:
	    lines[i] += disang
	i += 1
    remd_in = '\n'.join(lines)
    return remd_in

def make_minin(aa_num):
    """Returns a string with the parameters for the minimization step of the
       molecular simulation in Amber.
       
       Parameter aa_num is an integer.

    ######################################################################################
    #                                                                                    #
    #  This makes the input file for the minimization step, if the parameters for the    #
    #  minimization are going to be changed, you must do it in the minin string.         #
    #                                                                                    #
    ######################################################################################
    """
    # Separate the lines of the minimization pattern
    lines = minin.split('\n')
    i = 0
    while i<len(lines):
	if 'ibelly' in lines[i]:
	    # Create and add the mask
	    lines[i] += ' bellymask=":1-%s,"' %(aa_num)
	i += 1
    # Recreate the minimization pattern
    min_in = '\n'.join(lines)
    return min_in

def make_leap(input_file, funnel):
    """Return a string containing all the orders for the tleap module of the Amber software to 
       perform the REMD. Needs as parameters the pdb name files of the protein and the funnel.
       
       Both parameters are strings consisting only of file names.
    
    ######################################################################################
    #                                                                                    #
    #  This makes the input file for tleap. For this step you must have the              #
    #  pdb of the protein and the funnel in the same place this script is.               #
    #                                                                                    #
    ######################################################################################
    """
    leap_in = 'source leaprc.ff14SB_Ar\n'
    leap_in += 'prot = loadPdb %s\n' %(input_file)
    leap_in += 'fun = loadPdb %s\n' %(funnel)
    #leap_in += 'seq = { LEU LYS ASN ALA LYS GLU ASP ALA ILE ALA GLU LEU LYS LYS ALA GLY ILE THR SER ASP PHE TYR PHE ASN ALA ILE ASN LYS ALA LYS THR VAL GLU GLU VAL ASN ALA LEU LYS ASN GLU ILE LEU LYS ALA }\n'
    #leap_in += 'prot = loadPdbUsingSeq %s seq\n' %(input_file)
    leap_in += 'fun = loadPdb %s\n' %(funnel)
    leap_in += 'complex = combine {prot fun}\n'
    leap_in += 'saveAmberParm prot %s.prmtop %s.inpcrd\n' %(input_file[:-4], input_file[:-4])
    leap_in += 'saveAmberParm complex %s-%s.prmtop %s-%s.inpcrd\n' %(input_file[:-4], funnel[:-4], 
								     input_file[:-4], funnel[:-4])
    leap_in += 'savePdb prot %s.pdb\n' %(input_file[:-4])
    leap_in += 'savePdb complex %s-%s.pdb\n' %(input_file[:-4], funnel[:-4])
    leap_in += 'quit\n'
    return leap_in

def make_grp_file(name, parmtop, num_files, cycle):
    """Returns a string with the commands of a REMD group file for Amber.
       
       Parameters:
		  name: Pattern for input, output, coordinates, trajectory, restart, 
			info and reference files. Type string.
		  parmtop: Topology parameter file. Type string.
		  num_files: Number of files to add at the group file. Type integer.
		  cycle: Flag for the equilibration step. Type integer.
       
    ######################################################################################
    #                                                                                    #
    #  For every replicate a command is made sequentially.                               #
    #                                                                                    #
    ######################################################################################
    """
    grp = ''
    if cycle == 0:
	for i in range(num_files):
	    grp += '-O -i %s-000-mdin-rep.%3s -o %s-000-mdout-rep.%3s -c min.rst -p %s.prmtop -r %s-000-rep-%3s.rst -x %s-000-nc-rep.%3s -inf %s-000-mdinfo-rep.%3s -ref min.rst\n'\
		    %(name, str(i).rjust(3, '0'), name, str(i).rjust(3, '0'), parmtop, name, str(i).rjust(3, '0'), name, str(i).rjust(3, '0'), name, str(i).rjust(3, '0'))
    else:
	for i in range(num_files):
	    grp += '-O -i %s-%3s-mdin-rep.%3s -o %s-%3s-mdout-rep.%3s -c %s-%3s-rep-%3s.rst -p %s.prmtop -r %s-%3s-rep-%3s.rst -x %s-%3s-nc-rep.%3s -inf %s-%3s-mdinfo-rep.%3s -ref %s-%3s-rep-%3s.rst\n'\
		    %(name, str(cycle).rjust(3, '0'), str(i).rjust(3, '0'), name, str(cycle).rjust(3, '0'), str(i).rjust(3, '0'), name, str(cycle-1).rjust(3, '0'), str(i).rjust(3, '0'), parmtop, name, str(cycle).rjust(3, '0'), str(i).rjust(3, '0'), name, str(cycle).rjust(3, '0'), str(i).rjust(3, '0'), name, str(cycle).rjust(3, '0'), str(i).rjust(3, '0'), name, str(cycle-1).rjust(3, '0'), str(i).rjust(3, '0'))
    return grp
