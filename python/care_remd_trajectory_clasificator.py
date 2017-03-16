#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_remd_trajectory_clasificator.py
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

def main():
    """ Main function """
    trajname = args.trajin[:-3]
    log_list = list(args.log)
    temps = args.temps.split(',')
    numexchg = 0
    log_i = 0
    #j = 0
    script = ''
    while numexchg==0 and log_i<len(log_list):
	if 'numexchg' in log_list[log_i]:
	    numexchg = int(log_list[log_i].split()[-1])
	log_i += 1
    for temp in temps:
	cppin = ''
	frames = 1000
	traj_temp = 0
	log_i = 0
	while log_i<len(log_list):
	    if '# exchange' in log_list[log_i]:
		exch = int(log_list[log_i].split()[-1])-1
		log_i += 1
		for i in range(len(temps)):
		    temp0 = log_list[log_i].split()[4]
		    if temp == temp0:
			ini_frm = exch*frames+1
			end_frm = (exch+1)*frames
			cppin += 'trajin %s%s\n' %(trajname, str(i).rjust(3,'0'))
			cppin += 'trajout temp-%s-%3s.nc onlyframes %d-%d\n' %(temp, str(traj_temp).rjust(3,'0'), ini_frm, end_frm)
			cppin += 'go\nquit\n\n'
			#with open('remd_traj-%s.in'%(j), 'w') as cpp:
			with open('remd_traj.in', 'w') as cpp:
			    cpp.write(cppin)
			#system('cpptraj -p %s -i remd_traj-%s.in \n' %(args.parm, j))
			system('cpptraj -p %s -i remd_traj.in \n' %(args.parm))
			#script += 'cpptraj -p %s -i remd_traj-%s.in \n' %(args.parm, j)
			#j += 1
			cppin = ''
			traj_temp += 1
		    log_i += 1
	    else:
		log_i += 1
	for k in range(numexchg):
	    cppin += 'trajin temp-%s-%3s.nc\n' %(temp, str(k).rjust(3,'0'))
	cppin += 'trajout remd-%s.nc\ngo\nquit\n\n' %(temp)
	#with open('remd_traj-%s.in'%(j), 'w') as cpp:
	with open('remd_traj.in', 'w') as cpp:
	    cpp.write(cppin)
	system('cpptraj -p %s -i remd_traj.in\n' %(args.parm))
	#script += 'cpptraj -p %s -i remd_traj-%s.in\n' %(args.parm, j)
	#j += 1
	system('rm temp-*.nc remd_traj.in\n')
    #with open('remd_traj.sh', 'w') as cpp:
	#cpp.write(script)
    #system('sh remd_traj.sh')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='REMD Trajectory analyzer.')
    parser.add_argument('-l', '--log', required=True, type=argparse.FileType('r'), help='Logfile where the data for the exchanges is.')
    parser.add_argument('-y', '--trajin', required=True, help='REMD trajectory file, can be any of the replicas.')
    parser.add_argument('-p', '--parm', required=True, help='REMD topology file.')
    #parser.add_argument('-e', '--exchg', required=True, type=int, help='REMD number of exchanges.')
    parser.add_argument('-t', '--temps', required=True, help='REMD temperatures in comma separated format. Ex: 373.43,404.88,438.30')
    args = parser.parse_args()
    main()
