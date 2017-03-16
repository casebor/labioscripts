#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  probityScore.py
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

import sys, math

#                      0             1         2       3        4
# usage: python probityScore.py clashScore rotalize ramalyze probScore



def main():
	#             Original:
	#clashFile = open(sys.argv[1], 'r')
	#rotFile = open(sys.argv[2], 'r')
	#ramFile = open(sys.argv[3], 'r')
	#clashList = list(clashFile)
	#rotList = list(rotFile)
	#ramList = list(ramFile)
	#clashFile.close()
	#rotFile.close()
	#ramFile.close()
	#probScores = ''
    #    probCad = ''
	#for i in range(0, len(clashList)):
	#	probScore = (  0.426 * math.log(1 + float(clashList[i]))   ) + ( 0.33 * math.log(1 + max(0, (float(rotList[i]) - 1)))  ) + (  0.25 * math.log(1 + max(0, (100 - float(ramList[i])) - 2)) )  + 0.5
	#	probCad += '%f\n' %(probScore)
	#probFile = open(sys.argv[4], 'w')
	#probFile.write(probCad)
	#probFile.close()
	#             Modified:
	probScore = (  0.426 * math.log(1 + float(sys.argv[1]))   ) + ( 0.33 * math.log(1 + max(0, (float(sys.argv[2]) - 1)))  ) + (  0.25 * math.log(1 + max(0, (100 - float(sys.argv[3])) - 2)) )  + 0.5
	print probScore
	return 0

if __name__ == '__main__':
	main()



















