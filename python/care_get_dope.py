#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  get_dope.py
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

import sys
import os.path as osp
from modeller import environ, selection
from modeller.scripts import complete_pdb

def main():
    
    if len(sys.argv) != 2:
	print 'ERROR, incorrect number of inputs!!!'
	print usage
	quit()
    elif not osp.isfile(sys.argv[1]):
	print 'The input file' + sys.argv[1] + ' does not exist!!!'
	print usage
	quit()
    env = environ()
    env.libs.topology.read(file='$(LIB)/top_heav.lib')
    env.libs.parameters.read(file='$(LIB)/par.lib')
    
    mdl = complete_pdb(env, sys.argv[1])
    atmsel = selection(mdl.chains[0])
    score = atmsel.assess_dope()
    
    return 0

if __name__ == '__main__':
    usage = """##############################
#   get_dope.py pdb_model    #
##############################"""
    main()

