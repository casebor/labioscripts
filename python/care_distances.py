#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_distances.py
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
    """ Main function
    """
    lig_res = args.lig_mask.split('-')
    lig_ini = int(lig_res[0])
    lig_end = int(lig_res[1])
    lig_dif = lig_end - lig_ini + 1
    cppin = ''
    for i in range(args.lig_num):
	cppin += 'distance :%s :%d-%d out %s\n' %(args.prot_mask, lig_ini+(lig_dif*i), lig_end+(lig_dif*i), args.out)
    cppin += 'go\nquit\n'
    with open('cpptraj.in', 'w') as cpp:
	cpp.write(cppin)
    system('cpptraj -p %s -y %s -i cpptraj.in' %(args.parm, args.trajin))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Distance between molecules')
    parser.add_argument('-p', '--parm', help='Amber parameter topology file.')
    parser.add_argument('-y', '--trajin', help='Trajectory file.')
    parser.add_argument('-o', '--out', help='Output name for the file')
    parser.add_argument('-m', '--prot_mask', help='Protein mask numbers in format ##-##. Ex: 1-268')
    parser.add_argument('-l', '--lig_mask', help='Molecule mask for the FIRST ligand only. This parameter sets the range of mresidues that harbors the ligand. It is the same that for --prot_mask. Example: 467-468')
    parser.add_argument('-n', '--lig_num', type=int, help='Number of ligands present in the trajectory.')
    args = parser.parse_args()
    main()
