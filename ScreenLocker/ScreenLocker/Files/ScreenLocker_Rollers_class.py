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
from sys import exit,path
from time import sleep

from os.path import expanduser
path.append(expanduser('~')+"\Desktop\Windows\ScreenLocker\Files")
from ScreenLocker_keys import get_char
from ScreenLocker_password import Password

#For single use uncomment following lines.
#from Tkinter import Tk

#pygame.init()
#screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN,32)

#tk_objt=Tk()
#screen_width=tk_objt.winfo_screenwidth()
#screen_height=tk_objt.winfo_screenheight()
#del(tk_objt)


class Rollers() :
  def __init__(self,screen_width,screen_height,size="big",colors=["red"],background_color=(0,0,0),speed=0.005,direction="Vertical",music_filepath="",password="",recursion=0) :
    ''' Run the rollers animation with the given settings. '''
    
    self.screen_width=screen_width         # Get screen height for the fullscreen display size.
    self.screen_height=screen_height       # Get screen width for the fullscreen display size.
    
    self.size=size                         # Get the given size: ["little"|"middle"|"big"].
    self.colors=colors                     # Get the given color(s) for the rollers to display and their count.
    self.background_color=background_color # Get the given display background color.
    self.speed=speed                       # Get the given rollers animation speed for the sleep() function argument.
    self.direction=direction               # Get the given rollers direction: ["Horizontal"|"Vertical"]. 
    
    self.password=password                 # Get the given password hash
    self.password_entry=""
    self.password_recursion=recursion
    self.password_check=Password()
    
    self.runner=True                       # Control animation keep-alive variable.  
    
    ''' 
        The rollers are driven in two times:
        -) from border to center (from color to white) : self.up 
        -) from center to border (from white to color) : self.down
        and the color is [de|in]crement with the steps : self.incr
        to form a roller.
    '''    
    if self.size == 'big' : 
      self.up=64
      self.down=64
      self.incr=4
    elif self.size == "middle" :
      self.up=32
      self.down=32
      self.incr=8
    elif self.size == "little" :
      self.up=16
      self.down=16
      self.incr=16  
    
    pygame.init()
    self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN,32)
    
    if music_filepath :
      self.play_backgroound_music(music_filepath)
    
    if direction == "Vertical" and len(colors) == 1 :
      # Rollers running vertical and only one is selected.
      self.run_vertical()
    elif direction == "Vertical" and len(colors) > 1 :
      # Rollers running vertical and more than one is selected.
      self.run_multi_vertical()
    elif direction == "Horizontal" and len(colors) == 1 :
      # Rollers running horizontal and only one is selected.
      self.run_horizontal()
    elif direction == "Horizontal" and len(colors) > 1 :
      # Rollers running horizontal and more than one is selected.
      self.run_multi_horizontal()
      
  def play_backgroound_music(self,filepath) :
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(-1)
  
  def run_vertical(self) :
    
    
    start_pos=0                   # Actual position y value in the display
    
    color_idx=0                   # Color index for compatiblity with multi rollers.  
    color=self.colors[color_idx]  # Color setting.
    while self.runner :
      # Mainloop for one roller animation.
      
      self.screen.fill(self.background_color) # Background color filling.
      
      if start_pos == self.screen_height-(self.up+self.down) :
	# The roller reach the display end and we set the y position value to begin.
	start_pos=0 
	
	
      i=0
      ii=0
      while i < self.up :
	# Iterating for roller (from border to center part) generating.
	# The variable i for the y value
	# The variable ii for the color value.
	if color == 'red' :
	  pygame.draw.line(self.screen,(255,ii,ii),(0,start_pos+i),(self.screen_width,start_pos+i),1)
	elif color == "green" :
	  pygame.draw.line(self.screen,(ii,255,ii),(0,start_pos+i),(self.screen_width,start_pos+i),1)
	elif color == "blue" :
	  pygame.draw.line(self.screen,(ii,ii,255),(0,start_pos+i),(self.screen_width,start_pos+i),1)  
	elif color == "yellow" :
	  pygame.draw.line(self.screen,(255,255,ii),(0,start_pos+i),(self.screen_width,start_pos+i),1)
	elif color == "pink" :
	  pygame.draw.line(self.screen,(255,ii,255),(0,start_pos+i),(self.screen_width,start_pos+i),1)  
	elif color == "turkish" :
	  pygame.draw.line(self.screen,(ii,255,255),(0,start_pos+i),(self.screen_width,start_pos+i),1)          
	i += 1
	ii += self.incr
      
      ii=255 
      i=0
      while i < self.down :
	# Iterating for roller (from center to border part) generating.
	# The variable i for the y value
	# The variable ii for the color value.
	if color == 'red' :
	  pygame.draw.line(self.screen,(255,ii,ii),(0,start_pos+i+self.down),(self.screen_width,start_pos+i+self.down),1)
	elif color == 'green' :
	  pygame.draw.line(self.screen,(ii,255,ii),(0,start_pos+i+self.down),(self.screen_width,start_pos+i+self.down),1) 
	elif color == "blue" :
	  pygame.draw.line(self.screen,(ii,ii,255),(0,start_pos+i+self.down),(self.screen_width,start_pos+i+self.down),1)  
	elif color == "yellow" :
	  pygame.draw.line(self.screen,(255,255,ii),(0,start_pos+i+self.down),(self.screen_width,start_pos+i+self.down),1)
	elif color == "pink" :
	  pygame.draw.line(self.screen,(255,ii,255),(0,start_pos+i+self.down),(self.screen_width,start_pos+i+self.down),1)  
	elif color == "turkish" :
	  pygame.draw.line(self.screen,(ii,255,255),(0,start_pos+i+self.down),(self.screen_width,start_pos+i+self.down),1)         
	i += 1
	ii -= self.incr
	
	
      for event in pygame.event.get() :
	
	if event.type == KEYDOWN :
	  
	  if event.key == K_RETURN :
	    if self.password :
	      if self.password_check.gen_password_hash(self.password_entry,self.password_recursion) == self.password :
	        self.runner=False
	        try :
		  pygame.mixer.music.stop()
		except :
		  pass
	      else :
	        self.password_entry=""
	    else :
	      try :
		pygame.mixer.music.stop()
              except :
		pass
	      self.runner=False
	      
	    
	  else :
	    if self.password :
	      char=get_char(event.key)
	      if not char :
		self.password_entry=""
	      else :
		if not type(char) == bool :
		  self.password_entry += char    
	    
      
      start_pos += 1
      sleep(self.speed)
      pygame.display.update()
      
     
    pygame.display.quit()

  
  def run_horizontal(self) :
    
    
    start_pos=0                   # Actual position x value in the display
    
    color_idx=0                   # Color index for compatiblity with multi rollers.  
    color=self.colors[color_idx]  # Color setting.
    while self.runner :
      # Mainloop for one roller animation.
      
      self.screen.fill(self.background_color) # Background color filling.
      
      if start_pos == self.screen_width :
	# The roller reach the display end and we set the x position value to begin.
	start_pos=0 
	
	
      i=0
      ii=0
      while i < self.up :
	# Iterating for roller (from border to center part) generating.
	# The variable i for the y value
	# The variable ii for the color value.
	if color == 'red' :
	  pygame.draw.line(self.screen,(255,ii,ii),(start_pos+i,0),(start_pos+i,self.screen_height),1)
	elif color == "green" :
	  pygame.draw.line(self.screen,(ii,255,ii),(start_pos+i,0),(start_pos+i,self.screen_height),1)
	elif color == "blue" :
	  pygame.draw.line(self.screen,(ii,ii,255),(start_pos+i,0),(start_pos+i,self.screen_height),1)  
	elif color == "yellow" :
	  pygame.draw.line(self.screen,(255,255,ii),(start_pos+i,0),(start_pos+i,self.screen_height),1)
	elif color == "pink" :
	  pygame.draw.line(self.screen,(255,ii,255),(start_pos+i,0),(start_pos+i,self.screen_height),1)  
	elif color == "turkish" :
	  pygame.draw.line(self.screen,(ii,255,255),(start_pos+i,0),(start_pos+i,self.screen_height),1)          
	i += 1
	ii += self.incr
      
      ii=255 
      i=0
      while i < self.down :
	# Iterating for roller (from center to border part) generating.
	# The variable i for the y value
	# The variable ii for the color value.
	if color == 'red' :
	  pygame.draw.line(self.screen,(255,ii,ii),(start_pos+i+self.down,0),(start_pos+i+self.down,self.screen_height),1)
	elif color == 'green' :
	  pygame.draw.line(self.screen,(ii,255,ii),(start_pos+i+self.down,0),(start_pos+i+self.down,self.screen_height),1) 
	elif color == "blue" :
	  pygame.draw.line(self.screen,(ii,ii,255),(start_pos+i+self.down,0),(start_pos+i+self.down,self.screen_height),1)  
	elif color == "yellow" :
	  pygame.draw.line(self.screen,(255,255,ii),(start_pos+i+self.down,0),(start_pos+i+self.down,self.screen_height),1)
	elif color == "pink" :
	  pygame.draw.line(self.screen,(255,ii,255),(start_pos+i+self.down,0),(start_pos+i+self.down,self.screen_height),1)  
	elif color == "turkish" :
	  pygame.draw.line(self.screen,(ii,255,255),(start_pos+i+self.down,0),(start_pos+i+self.down,self.screen_height),1)         
	i += 1
	ii -= self.incr
	
	
      for event in pygame.event.get() :
	
	if event.type == KEYDOWN :
	  
	  if event.key == K_RETURN :
	    if self.password :
	      if self.password_check.gen_password_hash(self.password_entry,self.password_recursion) == self.password :
	        self.runner=False
	        try :
		  pygame.mixer.music.stop()
		except :
		  pass
	      else :
	        self.password_entry=""
	    else :
	      try :
		pygame.mixer.music.stop()
              except :
		pass
	      self.runner=False
	      
	  else :
	    if self.password :
	      char=get_char(event.key)
	      if not char :
		self.password_entry=""
	      else :
		if not type(char) == bool :
		  self.password_entry += char    
      
      start_pos += 1
      sleep(self.speed)
      pygame.display.update()    
    
    pygame.display.quit()
    
  def run_multi_horizontal(self) :
    
    start_pos=0                                   # Actual position x value in the display.
    
    increment=self.screen_width/len(self.colors)  # Compute the offset betweeen 2 rollers in relationship of the number of roller selected.
    
    for v in self.colors :
      # Set the start position in relationship of the number of roller selected,
      # and the offset between 2 rollers.
      if v == 'red' :
        pos_red=start_pos*increment 
      elif v == 'green' :
	pos_green=start_pos*increment    
      elif v == 'blue' :	
        pos_blue=start_pos*increment
      elif v == 'yellow' :  
        pos_yellow=start_pos*increment
      elif v == 'pink' :
        pos_pink=start_pos*increment
      elif v == 'turkish' :  
        pos_turkish=start_pos*increment
      start_pos += 1
      
    while self.runner :
      # Mainloop for multi rollers animation.
      
      self.screen.fill(self.background_color)  # Background color filling.
      
      # In case a roller reach the display end and we set the x position value to begin.
      if 'red' in self.colors :
        if pos_red == self.screen_width :
	  pos_red=0
      if 'green' in self.colors :	
	if pos_green == self.screen_width :
	  pos_green=0
      if 'blue' in self.colors :
        if pos_blue == self.screen_width :
	  pos_blue=0
      if 'yellow' in self.colors :
        if pos_yellow == self.screen_width :
	  pos_yellow=0
      if 'pink' in self.colors :
        if pos_pink == self.screen_width :
	  pos_pink=0
      if 'turkish' in self.colors :
	if pos_turkish == self.screen_width :
	  pos_turkish=0	
	  
	


      for v in self.colors :
	'''
	Big iteration over the selected colors to generate them iterativ in the two steps:
	-) first from border to center part,
	-) and then from center to borter part.
	
	# The variable i for the x value
	# The variable ii for the color value.
	'''
        if v == 'red' :	
	  i=0
	  ii=0
	  while i < self.up :
	    pygame.draw.line(self.screen,(255,ii,ii),(pos_red+i,0),(pos_red+i,self.screen_height),1)
	    i += 1
	    ii += self.incr
	  
	  ii=255 
	  i=0
	  while i < self.down :
	    pygame.draw.line(self.screen,(255,ii,ii),(pos_red+i+self.down,0),(pos_red+i+self.down,self.screen_height),1)
	    i += 1
	    ii -= self.incr
	  
	  pos_red += 1
	elif v == "green" :	
	  i=0
	  ii=0
	  while i < self.up :
	    pygame.draw.line(self.screen,(ii,255,ii),(pos_green+i,0),(pos_green+i,self.screen_height),1)
	    i += 1
	    ii += self.incr
	  
	  ii=255 
	  i=0
	  while i < self.down :
	    pygame.draw.line(self.screen,(ii,255,ii),(pos_green+i+self.down,0),(pos_green+i+self.down,self.screen_height),1) 
	    i += 1
	    ii -= self.incr   
	    
	  pos_green += 1
	
	elif v == 'blue' :	
	  i=0
	  ii=0
	  while i < self.up :
	    pygame.draw.line(self.screen,(ii,ii,255),(pos_blue+i,0),(pos_blue+i,self.screen_height),1)  
	    i += 1
	    ii += self.incr
	  
	  ii=255 
	  i=0
	  while i < self.down :
	    pygame.draw.line(self.screen,(ii,ii,255),(pos_blue+i+self.down,0),(pos_blue+i+self.down,self.screen_height),1) 
	    i += 1
	    ii -= self.incr
	  
	  pos_blue += 1
	  
	elif v == "yellow" :	
	  i=0
	  ii=0
	  while i < self.up :
	    pygame.draw.line(self.screen,(255,255,ii),(pos_yellow+i,0),(pos_yellow+i,self.screen_height),1)
	    i += 1
	    ii += self.incr
	  
	  ii=255 
	  i=0
	  while i < self.down :
	    pygame.draw.line(self.screen,(255,255,ii),(pos_yellow+i+self.down,0),(pos_yellow+i+self.down,self.screen_height),1)
	    i += 1
	    ii -= self.incr   
	    
	  pos_yellow += 1
	  
	elif v == 'pink' :	
	  i=0
	  ii=0
	  while i < self.up :
	    pygame.draw.line(self.screen,(255,ii,255),(pos_pink+i,0),(pos_pink+i,self.screen_height),1) 
	    i += 1
	    ii += self.incr
	  
	  ii=255 
	  i=0
	  while i < self.down :
	    pygame.draw.line(self.screen,(255,ii,255),(pos_pink+i+self.down,0),(pos_pink+i+self.down,self.screen_height),1)
	    i += 1
	    ii -= self.incr
	  
	  pos_pink += 1
	  
	elif v == "turkish" :	
	  i=0
	  ii=0
	  while i < self.up :
	    pygame.draw.line(self.screen,(ii,255,255),(pos_turkish+i,0),(pos_turkish+i,self.screen_height),1)   
	    i += 1
	    ii += self.incr
	  
	  ii=255 
	  i=0
	  while i < self.down :
	    pygame.draw.line(self.screen,(ii,255,255),(pos_turkish+i+self.down,0),(pos_turkish+i+self.down,self.screen_height),1)
	    i += 1
	    ii -= self.incr   
	    
	  pos_turkish += 1  
	
	
	
      for event in pygame.event.get() :
	
	if event.type == KEYDOWN :
	  
	  if event.key == K_RETURN :
	    if self.password :
	      if self.password_check.gen_password_hash(self.password_entry,self.password_recursion) == self.password :
	        self.runner=False
	        try :
		  pygame.mixer.music.stop()
		except :
		  pass
	      else :
	        self.password_entry=""
	    else :
	      try :
		pygame.mixer.music.stop()
              except :
		pass
	      self.runner=False
	      
	  else :
	    if self.password :
	      char=get_char(event.key)
	      if not char :
		self.password_entry=""
	      else :
		if not type(char) == bool :
		  self.password_entry += char    
      
      
      
      pygame.display.update() 
      sleep(self.speed)       
    
    pygame.display.quit()
    
  def run_multi_vertical(self) :
    
    
    start_pos=0                                   # Actual position y value in the display.
    
    increment=self.screen_height/len(self.colors) # Compute the offset betweeen 2 rollers in relationship of the number of roller selected.
    
    for v in self.colors :
      # Set the start position in relationship of the number of roller selected,
      # and the offset between 2 rollers.
      if v == 'red' :
        pos_red=start_pos*increment 
      elif v == 'green' :
	pos_green=start_pos*increment    
      elif v == 'blue' :	
        pos_blue=start_pos*increment
      elif v == 'yellow' :  
        pos_yellow=start_pos*increment
      elif v == 'pink' :
        pos_pink=start_pos*increment
      elif v == 'turkish' :  
        pos_turkish=start_pos*increment
      start_pos += 1
      
    while self.runner :
      # Mainloop for multi rollers animation.
      
      self.screen.fill(self.background_color)  # Background color filling.
      
      # In case a roller reach the display end and we set the y position value to begin.
      if 'red' in self.colors :
	if pos_red == self.screen_height:
	  pos_red=0
      if 'green' in self.colors :
        if pos_green == self.screen_height :
	  pos_green=0
      if 'blue' in self.colors :
        if pos_blue == self.screen_height:
	  pos_blue=0
      if 'yellow' in self.colors :
        if pos_yellow == self.screen_height :
	  pos_yellow=0
      if 'pink' in self.colors :
        if pos_pink == self.screen_height :
	  pos_pink=0
      if 'turkish' in self.colors :
        if pos_turkish == self.screen_height :
	  pos_turkish=0	
	
	


      for v in self.colors :
	'''
	Big iteration over the selected colors to generate them iterativ in the two steps:
	-) first from border to center part,
	-) and then from center to borter part.
	
	# The variable i for the y value
	# The variable ii for the color value.
	'''
        if v == 'red' :	
	  i=0
	  ii=0
	  while i < self.up :
	    pygame.draw.line(self.screen,(255,ii,ii),(0,pos_red+i),(self.screen_width,pos_red+i),1)
	    i += 1
	    ii += self.incr
	  
	  ii=255 
	  i=0
	  while i < self.down :
	    pygame.draw.line(self.screen,(255,ii,ii),(0,pos_red+i+self.down),(self.screen_width,pos_red+i+self.down),1)
	    i += 1
	    ii -= self.incr
	  
	  pos_red += 1
	elif v == "green" :	
	  i=0
	  ii=0
	  while i < self.up :
	    pygame.draw.line(self.screen,(ii,255,ii),(0,pos_green+i),(self.screen_width,pos_green+i),1)
	    i += 1
	    ii += self.incr
	  
	  ii=255 
	  i=0
	  while i < self.down :
	    pygame.draw.line(self.screen,(ii,255,ii),(0,pos_green+i+self.down),(self.screen_width,pos_green+i+self.down),1) 
	    i += 1
	    ii -= self.incr   
	    
	  pos_green += 1
	
	elif v == 'blue' :	
	  i=0
	  ii=0
	  while i < self.up :
	    pygame.draw.line(self.screen,(ii,ii,255),(0,pos_blue+i),(self.screen_width,pos_blue+i),1)  
	    i += 1
	    ii += self.incr
	  
	  ii=255 
	  i=0
	  while i < self.down :
	    pygame.draw.line(self.screen,(ii,ii,255),(0,pos_blue+i+self.down),(self.screen_width,pos_blue+i+self.down),1) 
	    i += 1
	    ii -= self.incr
	  
	  pos_blue += 1
	  
	elif v == "yellow" :	
	  i=0
	  ii=0
	  while i < self.up :
	    pygame.draw.line(self.screen,(255,255,ii),(0,pos_yellow+i),(self.screen_width,pos_yellow+i),1)
	    i += 1
	    ii += self.incr
	  
	  ii=255 
	  i=0
	  while i < self.down :
	    pygame.draw.line(self.screen,(255,255,ii),(0,pos_yellow+i+self.down),(self.screen_width,pos_yellow+i+self.down),1)
	    i += 1
	    ii -= self.incr   
	    
	  pos_yellow += 1
	  
	elif v == 'pink' :	
	  i=0
	  ii=0
	  while i < self.up :
	    pygame.draw.line(self.screen,(255,ii,255),(0,pos_pink+i),(self.screen_width,pos_pink+i),1) 
	    i += 1
	    ii += self.incr
	  
	  ii=255 
	  i=0
	  while i < self.down :
	    pygame.draw.line(self.screen,(255,ii,255),(0,pos_pink+i+self.down),(self.screen_width,pos_pink+i+self.down),1)
	    i += 1
	    ii -= self.incr
	  
	  pos_pink += 1
	  
	elif v == "turkish" :	
	  i=0
	  ii=0
	  while i < self.up :
	    pygame.draw.line(self.screen,(ii,255,255),(0,pos_turkish+i),(self.screen_width,pos_turkish+i),1)   
	    i += 1
	    ii += self.incr
	  
	  ii=255 
	  i=0
	  while i < self.down :
	    pygame.draw.line(self.screen,(ii,255,255),(0,pos_turkish+i+self.down),(self.screen_width,pos_turkish+i+self.down),1)
	    i += 1
	    ii -= self.incr   
	    
	  pos_turkish += 1  
	
	
	
      for event in pygame.event.get() :
	
	if event.type == KEYDOWN :
	  
	  if event.key == K_RETURN :
	    if self.password :
	      if self.password_check.gen_password_hash(self.password_entry,self.password_recursion) == self.password :
	        self.runner=False
	        try :
		  pygame.mixer.music.stop()
		except :
		  pass
	      else :
	        self.password_entry=""
	    else :
	      try :
		pygame.mixer.music.stop()
              except :
		pass
	      self.runner=False
	      
	  else :
	    if self.password :
	      char=get_char(event.key)
	      if not char :
		self.password_entry=""
	      else :
		if not type(char) == bool :
		  self.password_entry += char    
      
      
      
      pygame.display.update() 
      sleep(self.speed)  
    
    pygame.display.quit()
   
#For single use uncomment following line.
#rollers=Rollers(screen_width,screen_height)


