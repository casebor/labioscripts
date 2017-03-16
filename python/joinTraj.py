#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  joinTraj.py
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

import mdtraj as md
import sys

'''
The first option is the topology parameter file and then you just add the trajectory files in the 
order that they are going to be joined. The output name is the topology name, without the extension 
as default.
'''

#              0          1          2         3         4         5         6     ...
# python joinTraj.py output.nc traj.prmtop traj-1.nc traj-2.nc traj-3.nc traj-4.nc ...

def main():
	mdFile = md.load(sys.argv[3], top=sys.argv[2])
	i = 4
	while i<len(sys.argv):
		temp = md.load(sys.argv[i], top=sys.argv[2])
		mdFile = mdFile.join(temp)
		i +=1
	#trajFile = sys.argv[1].split('.')[0] + '.nc'
	mdFile.save_netcdf(sys.argv[1], force_overwrite=True)
	return 0

if __name__ == '__main__':
	main()

