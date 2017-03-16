#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  proteinMaker.py
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

from optparse import OptionParser

"""
	##############################################################################
	#                                                                            #
	#  Makes the .pdb file of a protein sequence, aligned at the X axis and      #
	#  in the negative direction. This constructs the protein only with their    #
	#  backbone atoms, N-Ca-C=O.                                                 #
	#                                                                            #
	##############################################################################
"""

class NoProtError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def get_seq(pdbFile):
	linAr = list(pdbFile)
	i = 0
	prot = ''
	cad =''
	while i<len(linAr):
		if linAr[i][0:6]=='SEQRES':
			if len(cad)==0:
				cad = linAr[i][11]
			amins = linAr[i].split()
			if linAr[i][11]==cad:
				for j in amins:
					if is_aa(j):
						prot += j + ' '
						#if len(j) == 1:
						#	prot += get3LetCode(j) + ' '
						#else:
						#	prot += j + ' '
			else:
				print 'The input file contains more than one chain, it is going to be used\
				just the first one.'
		elif linAr[i][0:4]=='ATOM':
			i = len(linAr)
		i += 1
	if len(prot)==0:
		print '404 - No Sequence Found!!!'
		raise NoProtError('404 - No Sequence Found!!!')
	return prot.split()

def is_aa(cad):
	AA = ('ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL')
	#aa = ('A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V')
	#return (cad in AA) or (cad in aa)
	return cad in AA
	
def crt_body(aaChain):
	residues = len(aaChain)
	atoms = residues*3
	ptoB = [-1.216, 0.829, 0.0]
	ptoC = [-2.5, 0.0, 0.0]
	fact0 = -1.242
	ptos = [ptoB, ptoC]
	res = 0
	prot = '%-6s%5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n' %('ATOM', 1, 'N', '', aaChain[res], '', res+1, '', 0.0, 0.0, 0.0, 1.0, 10.0, 'N', '')
	atoms -= 1
	i = 0
	while atoms>0:
		prot += '%-6s%5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n' %('ATOM', 1, 'CA', '', aaChain[res], '', res+1, '', ptos[i][0], ptos[i][1], ptos[i][2], 1.0, 10.0, 'C', '')
		ptos[i][0] -= 2.5
		atoms -= 1
		i += 1
		ptos.append(ptoB)
		ptos.append(ptoC)
		prot += '%-6s%5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n' %('ATOM', 1, 'C', '', aaChain[res], '', res+1, '', ptos[i][0], ptos[i][1], ptos[i][2], 1.0, 10.0, 'C', '')
		prot += '%-6s%5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n' %('ATOM', 1, 'O', '', aaChain[res], '', res+1, '', ptos[i][0], ptos[i][1]+fact0, ptos[i][2], 1.0, 10.0, 'O', '')
		ptos[i][0] -= 2.5
		atoms -= 1
		i += 1
		fact0 *= -1
		ptos.append(ptoB)
		ptos.append(ptoC)
		if atoms>0:
			res += 1
			prot += '%-6s%5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n' %('ATOM', 1, 'N', '', aaChain[res], '', res+1, '', ptos[i][0], ptos[i][1], ptos[i][2], 1.0, 10.0, 'N', '')
			ptos[i][0] -= 2.5
			atoms -= 1
			i += 1
	return prot

def get3LetCode(amino):
	if amino=='A':
		return 'ALA'
	elif amino=='R':
		return 'ARG'
	elif amino=='N':
		return 'ASN'
	elif amino=='D':
		return 'ASP'
	elif amino=='C':
		return 'CYS'
	elif amino=='Q':
		return 'GLN'
	elif amino=='E':
		return 'GLU'
	elif amino=='G':
		return 'GLY'
	elif amino=='H':
		return 'HIS'
	elif amino=='I':
		return 'ILE'
	elif amino=='L':
		return 'LEU'
	elif amino=='K':
		return 'LYS'
	elif amino=='M':
		return 'MET'
	elif amino=='F':
		return 'PHE'
	elif amino=='P':
		return 'PRO'
	elif amino=='S':
		return 'SER'
	elif amino=='T':
		return 'THR'
	elif amino=='W':
		return 'TRP'
	elif amino=='Y':
		return 'TYR'
	elif amino=='V':
		return 'VAL'

def main():
	try:
		archIn = open(options.inputFile, 'r')
		protSeq = get_seq(archIn)
		archIn.close()
		prot = crt_body(protSeq)
		archOut = open(options.outFile, 'w')
		archOut.write(prot)
		archOut.close()
		return 0
	except NameError as ne:
		print ne
	except TypeError as te:
		print 'Error, input file may be missing!!'
		print te
	except NoProtError as npe:
		print 'You did not supplied a pdb file or the file does not contain any aminoacid sequence.'
		print npe.value

if __name__ == '__main__':
	
	usage = 'usage: \"%prog [options] args\" or \"%prog\"'
	parser = OptionParser(usage)
	parser.add_option('-f', '--file', action='store', type='string', dest='inputFile', help='The file you are going to use to create your protein. Can be a pdb file or just a text file with your sequence.')
	parser.add_option('-o', '--out', action='store', type='string', dest='outFile', default='output.pdb', help='Defines the name of your output file. Default is output.pdb')
	(options, args) = parser.parse_args()

	main()

