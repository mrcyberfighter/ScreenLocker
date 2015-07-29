#!/usr/bin/python
# -*- coding: utf-8 -*-

########################################################################
# ScreenLocker an simply screensaver displaying animations,            #
# with password protection and music file playing possiblities.        #
# Copyright (C) 2014 Bruggemann Eddie.                                 #
#                                                                      #
# This file is part of ScreenLocker.                                   # 
# ScreenLocker is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# ScreenLocker is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    # 
# along with ScreenLocker. If not, see http://www.gnu.org/licenses/    #
########################################################################
import pygame
from pygame.locals import *

def get_char(key) :
  num={224:'0', 38 :'1',233 :'2',34 :'3',39 :'4',40 :'5',45 :'6',232 :'7',95 :'8',231 :'9'}
  num_keypad={K_KP0 : "0",K_KP1 : "1",K_KP2 : "2",K_KP3 : "3",K_KP4 : "4",K_KP5 : "5",K_KP6 : "6",K_KP7 : "7",K_KP8 : "8",K_KP9 : "9"}
  alpha={K_a :'a',K_b :'b',K_c :'c',K_d :'d',K_e :'e',K_f :'f',K_g :'g',K_h :'h',K_i :'i',K_j :'j',K_k :'k',K_l :'l',K_m :'m',K_n :'n',K_o :'o',K_p :'p',K_q :'q',K_r :'r',K_s :'s',K_t :'t',K_u :'u',K_v :'v',K_w :'w',K_x :'x',K_y :'y',K_z :'z'}       
  if key in [K_NUMLOCK,K_CAPSLOCK,K_RSHIFT,K_LSHIFT] :
    return True
  elif key in num_keypad.keys() :
    return num_keypad.get(key)
  elif key in num.keys() :
    return num.get(key)
  elif ( (pygame.key.get_mods() & KMOD_SHIFT or  (pygame.key.get_mods() & KMOD_CAPS) ) and (key in alpha) ) :
    return alpha.get(key).upper()
  elif key in alpha and not ( (pygame.key.get_mods() & KMOD_SHIFT) or  (pygame.key.get_mods() & KMOD_CAPS) or (pygame.key.get_mods() & KMOD_CTRL) or (pygame.key.get_mods() & KMOD_ALT)  ) : 
    return alpha.get(key) 
  else :
    return False