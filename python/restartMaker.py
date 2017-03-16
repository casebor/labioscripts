#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  restartMaker_v0.py
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

#             0               1              2               3          4      5          6          7 
# usage: nuevoMD_v0.py protRest.restrt protTop.prmtop fromRest.restrt resIni resFin funnil.inpcrd flagFinal

import sys, shutil, atom as at, mdtraj as md

"""
    ##############################################################################
    #                                                                            #
    #  This script changes the restart file of a MD cycle by adding residues     #
    #  in between the protein and the funnel, this is, add residues to the       #
    #  protein only in the C-end tail. The only use of this script is for a      #
    #  cotranslational approach for MD in Amber.                                 #
    #                                                                            #
    ##############################################################################
"""

def get_atoms(lista, atomLim):
    """
    ##############################################################################
    #                                                                            #
    #  This function returns an array with the atoms extracted from an Amber     #
    #  restart file from the beggining to the end, using atomLim as limiting     #
    #  number of atoms.                                                          #
    #                                                                            #
    ##############################################################################
    """
    atoms = []
    if len(lista)>0:
	i = 2
	atms = 0
	while atms < atomLim:
	    atm1 = at.Atom(lista[i][0:12], lista[i][12:24], lista[i][24:36])
	    atoms.append(atm1)
	    atms += 1
	    if atms < atomLim:
		atm2 = at.Atom(lista[i][36:48], lista[i][48:60], lista[i][60:72])
		atoms.append(atm2)
		atms += 1
	    i += 1
	atms = 0
	i = (len(lista)/2)+1
	while atms < atomLim:
	    atoms[atms].set_vels(lista[i][0:12], lista[i][12:24], lista[i][24:36])
	    atms += 1
	    if atms < atomLim:
		atoms[atms].set_vels(lista[i][36:48], lista[i][48:60], lista[i][60:72])
		atms += 1
	    i += 1
    return atoms

def get_atoms_fun(funList):
    """
    ##############################################################################
    #                                                                            #
    #  This function returns an array with the atoms extracted from an Amber     #
    #  input coordinates file, it is different from a restart file because       #
    #  it does not have velocities in it.                                        #
    #                                                                            #
    ##############################################################################
    """
    i = 2
    fun = []
    while i < len(funList):
	atm1 = at.Atom(funList[i][0:12], funList[i][12:24], funList[i][24:36])
	fun.append(atm1)
	if len(funList[i])>40:
	    atm2 = at.Atom(funList[i][36:48], funList[i][48:60], funList[i][60:72])
	    fun.append(atm2)
	i += 1
    return fun

def generate_prot(baseProt):
    """
    ##############################################################################
    #                                                                            #
    #  This function returns a String containing all the atoms in the array      #
    #  builded in an Amber restart file format.                                  #
    #                                                                            #
    ##############################################################################
    """
    protein = 'default_name\n%6s\n' %(str(len(baseProt)))
    if len(baseProt)%2 == 0:
	for i in range(0, len(baseProt), 2):
	    protein += '%12s%12s%12s%12s%12s%12s\n' %(baseProt[i].get_pos_x(), baseProt[i].get_pos_y(), baseProt[i].get_pos_z(), baseProt[i+1].get_pos_x(), baseProt[i+1].get_pos_y(), baseProt[i+1].get_pos_z())
	for i in range(0, len(baseProt), 2):
	    protein += '%12s%12s%12s%12s%12s%12s\n' %(baseProt[i].get_vel_x(), baseProt[i].get_vel_y(), baseProt[i].get_vel_z(), baseProt[i+1].get_vel_x(), baseProt[i+1].get_vel_y(), baseProt[i+1].get_vel_z())
    else:
	for i in range(0, len(baseProt)-1, 2):
	    protein += '%12s%12s%12s%12s%12s%12s\n' %(baseProt[i].get_pos_x(), baseProt[i].get_pos_y(), baseProt[i].get_pos_z(), baseProt[i+1].get_pos_x(), baseProt[i+1].get_pos_y(), baseProt[i+1].get_pos_z())
	protein += '%12s%12s%12s\n' %(baseProt[-1].get_pos_x(), baseProt[-1].get_pos_y(), baseProt[-1].get_pos_z())
	for i in range(0, len(baseProt)-1, 2):
	    protein += '%12s%12s%12s%12s%12s%12s\n' %(baseProt[i].get_vel_x(), baseProt[i].get_vel_y(), baseProt[i].get_vel_z(), baseProt[i+1].get_vel_x(), baseProt[i+1].get_vel_y(), baseProt[i+1].get_vel_z())
	protein += '%12s%12s%12s\n' %(baseProt[-1].get_vel_x(), baseProt[-1].get_vel_y(), baseProt[-1].get_vel_z())
    return protein

def main():
    protFile = open(sys.argv[1], 'r')
    protLista = list(protFile)
    protFile.close()
    global ATMS_PROT, REST_PROT, TOP_PROT, ATMS_FUN
    REST_PROT = md.load(sys.argv[1], top=sys.argv[2])
    TOP_PROT = REST_PROT.topology
    ATMS_PROT = get_atoms(protLista, REST_PROT.n_atoms)
    funFile = open(sys.argv[6], 'r')
    funList = list(funFile)
    funFile.close()
    ATMS_FUN = get_atoms_fun(funList)
    atms = TOP_PROT.select('resid %s to %s' %(sys.argv[4], sys.argv[5]))
    atmIni = int(atms[0])
    if sys.argv[7] == '1':
	atmFin = len(ATMS_PROT)
    else:
	atmFin = int(atms[-1]) + 2
    fromFile = open(sys.argv[3], 'r')
    fromList = list(fromFile)
    fromFile.close()
    if sys.argv[4] == '0':
	atoms = []
    else:
	atoms = TOP_PROT.select('resid 0 to %s' %(int(sys.argv[4])-1))
    #atoms = TOP_PROT.select('resid 0 to %s' %(int(sys.argv[4])-1))
    baseProt = get_atoms(fromList, len(atoms))
    #if len(baseProt) > 0 and sys.argv[7] != '1':
    #	del baseProt[-1]
    
    baseProt = baseProt + ATMS_PROT[atmIni:atmFin] + ATMS_FUN
    #protein = 'default_name\n%6s\n' %(str(len(baseProt)))
    outProt = generate_prot(baseProt)
    #outProt = generate_prot(atmIni, atmFin)
    shutil.copy(sys.argv[3], sys.argv[3]+'.orig')
    outFile = open(sys.argv[3],'w')
    outFile.write(outProt)
    outFile.close()
    return 0

if __name__ == '__main__':
    main()
