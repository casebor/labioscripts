#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_get_min_rmsd.py
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


import argparse, numpy as np

def main():
    """ Main function
    """
    data = np.loadtxt(args.infile, comments="#")
    minimo = np.argmin(data[:,1])
    print "%d\t%f" %(int(data[minimo][0]), data[minimo][1])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the minimum value from a RMSD file.')
    parser.add_argument('-i', '--in', action='store', required=True, dest='infile', help='The input file with the RMSD values.')
    args = parser.parse_args()
    main()
