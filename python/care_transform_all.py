#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_transform_all.py
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

import sys, os

def main():
    ps = sys.argv[1]
    num = sys.argv[2]
    parm = sys.argv[3]
    temps = ['300K', '350K', '400K', '450K']
    for i in range(4):
	cppin = 'trajin %s/trajec/md-%s.nc start 1 stop 500\n' %(temps[i], num)
	cppin += 'trajout %s-%s.pdb\ngo' %(ps, temps[i])
	with open('cpp.in', 'w') as cpp:
	    cpp.write(cppin)
	os.system('cpptraj -p %s -i cpp.in' %(parm))
	os.system('rm cpp.in')
    return 0

if __name__ == '__main__':
    main()
