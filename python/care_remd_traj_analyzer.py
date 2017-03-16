#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_remd_traj_analyzer.py
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

from os import system
from optparse import OptionParser

def main():
    
    temps = options.temperatures.split(',')
    for temp in temps:
	cpp_in = ''
	for i in range(1, options.steps+1):
	    cpp_in += 'trajin remd-%3s-nc-rep.000 remdtraj remdtrajtemp %s\n' %(str(i).rjust(3,'0'), temp)
	cpp_in += 'trajout remd-%s.nc\ngo\nquit\n'%(temp)
	with open('.cpp.in', 'w') as cpp_file:
	    cpp_file.write(cpp_in)
	system('cpptraj -p %s -i .cpp.in' %(options.parm))
	system('rm .cpp.in')
    
    return 0

if __name__ == '__main__':
    usage = 'usage: \"%prog args\"'
    parser = OptionParser(usage)
    parser.add_option('-t', '--temps', action='store', type='string', dest='temperatures', help='The temperatures used in the REMD simulation, can be used to get only the desired temperatures. The temperatures must be in one line and coma separated.')
    parser.add_option('-p', '--parm', action='store', type='string', dest='parm', help='Name of the topology parameter file.')
    parser.add_option('-s', '--steps', action='store', type='int', dest='steps', help='Number of the steps in the simulation.')
    (options, args) = parser.parse_args()
    main()
