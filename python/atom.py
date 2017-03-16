#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  atom.py
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

class Atom():
	
	"""
	##################################################################################
	#                                                                                #
	#  This class represents an Atom, with it's XYZ coordinates and XYZ velocities.  #
	#  All the variables are treated as strings, but in the set functions, we make   #
	#  sure that the values are numbers.                                             #
	#                                                                                #
	##################################################################################
	"""
	
	global POS_X, POS_Y, POS_Z, VEL_X, VEL_Y, VEL_Z
	
	def __init__(self, px, py, pz, vx='0.0000000', vy='0.0000000', vz='0.0000000'):
		float(px)
		float(py)
		float(pz)
		float(vx)
		float(vy)
		float(vz)
		self.POS_X = px
		self.POS_Y = py
		self.POS_Z = pz
		self.VEL_X = vx
		self.VEL_Y = vy
		self.VEL_Z = vz
	
	def set_vels(self, vx, vy, vz):
		float(vx)
		float(vy)
		float(vz)
		self.VEL_X = vx
		self.VEL_Y = vy
		self.VEL_Z = vz
	
	def set_pos(self, px, py, pz):
		float(px)
		float(py)
		float(pz)
		self.POS_X = px
		self.POS_Y = py
		self.POS_Z = pz
	
	def get_pos(self):
		return [self.POS_X, self.POS_Y, self.POS_Z]
	
	def get_vels(self):
		return [self.VEL_X, self.VEL_Y, self.VEL_Z]
	
	def get_pos_x(self):
		cadX = str(self.POS_X).split('.')
		return '%4s.%7s' %(cadX[0], cadX[1].ljust(7, '0'))
	
	def get_pos_y(self):
		cadY = str(self.POS_Y).split('.')
		return '%4s.%7s' %(cadY[0], cadY[1].ljust(7, '0'))
	
	def get_pos_z(self):
		cadZ = str(self.POS_Z).split('.')
		return '%4s.%7s' %(cadZ[0], cadZ[1].ljust(7, '0'))
	
	def get_vel_x(self):
		cadX = str(self.VEL_X).split('.')
		return '%4s.%7s' %(cadX[0], cadX[1].ljust(7, '0'))
	
	def get_vel_y(self):
		cadY = str(self.VEL_Y).split('.')
		return '%4s.%7s' %(cadY[0], cadY[1].ljust(7, '0'))
	
	def get_vel_z(self):
		cadZ = str(self.VEL_Z).split('.')
		return '%4s.%7s' %(cadZ[0], cadZ[1].ljust(7, '0'))
