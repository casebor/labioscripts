#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  care_cluster_distribution.py
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
import numpy as np

def main():
    """ Main function
    """
    clus_info = args.info.next()
    clust_qty = int(clus_info.split()[1])
    data = np.loadtxt(args.cluster, usecols=(1,), dtype=int)
    clusters = [0]*clust_qty
    for i in data:
	clusters[i-1] += 1
    out_data = '#Cluster\tStructures\n'
    total = 0
    for i,cluster in enumerate(clusters):
	out_data += 'Cluster_%d\t%d\n' %(i+1, cluster)
	total += cluster
    out_data += 'Total\t%d\n' %(total)
    args.outfile.write(out_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze clustering results from cpptraj. Needs as input the info and cluster files, generating one output file with the quantity of structures per cluster.')
    parser.add_argument('-i', '--info', action='store', type=argparse.FileType('r'), required=True, help='The info file generated with cpptraj.')
    parser.add_argument('-c', '--cluster', action='store', required=True, help='The cluster file generated with cpptraj.')
    parser.add_argument('-o', '--outfile', action='store', type=argparse.FileType('w'), required=True, help='The output file to save the structures distribution.')
    args = parser.parse_args()
    main()
