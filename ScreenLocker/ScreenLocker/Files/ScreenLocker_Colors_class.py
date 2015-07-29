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

from random import randint, choice

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



class Colors() :
  def __init__(self,screen_width,screen_height,square=0,size="little",fullscreen=False,color="red",rand_color=False,rand_size=False,background_color=(0,0,0),speed=0.005,music_filepath="",password="",recursion=0) :
    
    self.center=(screen_width/2,screen_height/2) # Get the center coordinates.
    
    self.mode=square                             # Get the given mode [ Circle == 0 | Square == 1] 
    
    self.colors_red=self.generate_red()          # Generate the red gradients.
    self.colors_green=self.generate_green()      # Generate the green gradients.
    self.colors_blue=self.generate_blue()        # Generate the blue gradients.
    
    self.rand_color=rand_color                   # Get the random color mode as an boolean value.  
    
    if not rand_color :
      # Only one color will be used.
      colors=['red','green','blue']
      self.colors_indexer=colors.index(color[0])    # Color is given as an string ["red"|"green"|"blue"]
      self.colors=[self.generate_red(),self.generate_green(),self.generate_blue()][self.colors_indexer] # Set the wanted color.
    else :
      # Random color mode.
      self.colors_indexer=0
      self.colors=choice([self.generate_red(),self.generate_green(),self.generate_blue()])
    
    
    
    
    sizer={"little":512,"middle":1024,"big":768*2} # Predefine sizes for the size arguùment values ["little"|"middle"|"big"]
    
    if not fullscreen and not rand_size :
      # Predefine sizes.
      self.rand_size=False                       # Set the random size mode as an boolean value.
      self.size=sizer.get(size)/2                # Contains the size of the radius of the greatest circle or the half-size from the square in relationship to the mode.             
    else :
      # Fullscreen mode.
      self.rand_size=False 
      if screen_width >= screen_height :   
        self.size=screen_width                   # Contains the size of the radius of the greatest circle or the half-size from the square in relationship to the mode.
      else :
	self.size=screen_height                  # Contains the size of the radius of the greatest circle or the half-size from the square in relationship to the mode.
	
    if rand_size and not fullscreen:
      # Random size mode.
      if screen_width >= screen_height :
        size_up=screen_height-1                  # Contains the size of the radius of the greatest circle or the half-size from the square in relationship to the mode.
      else :
	size_up=screen_width-1                   # Contains the size of the radius of the greatest circle or the half-size from the square in relationship to the mode.
	
      self.rand_size=True
      
      self.min_size=1                            # Lowest  value  for the random size
      self.max_size=size_up/2                    # Highest value  for the random size.
      self.size=size_up/2
      
    self.background_color=background_color       # Get the given display background color.
    self.speed=speed                             # Get the given bars animation speed for the sleep() function argument.
    
    self.password=password                  # Get the given password hash
    self.password_entry=""
    self.password_recursion=recursion
    self.password_check=Password()
    
    self.runner=True                        # Control animation keep-alive variable.
    
    pygame.init()
    self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN,32)
    
    if music_filepath :
      self.play_backgroound_music(music_filepath)
      
    self.run()
  
  def play_backgroound_music(self,filepath) :
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(-1)
  
  def change_palette(self) :
    ''' Change the color.'''
    if self.colors_indexer == 0 :
      self.colors=self.generate_green()  
    elif self.colors_indexer == 1 :
      self.colors=self.generate_blue()  
    elif self.colors_indexer == 2 :
      self.colors=self.generate_red()  
  
  def generate_red(self) :
    ''' Generate red gradients. '''

    colors_red=[]
    red_tmp_1=[]
    red_tmp_2=[]
    red_tmp_3=[]
    
    for v in range(0,256) :
      red_tmp_1.append((255,0,v))

    for v in range(0,256) :
      red_tmp_2.append((255,v,0))
      
    for v in range(0,256) :
      red_tmp_3.append((255,v,v))  
    
    i=2
    red_tmp=[red_tmp_1,red_tmp_2,red_tmp_3]
    while i >= 0 :
      if i == 0 :
	colors_red += red_tmp.pop(0)
      else : 	
        colors_red += red_tmp.pop(randint(0,i))
      i -= 1
    return colors_red

  
  def generate_green(self) :
    ''' Generate green gradients. '''

    colors_green=[]
    green_tmp_1=[]
    green_tmp_2=[]
    green_tmp_3=[] 
    for v in range(0,256) :
      green_tmp_1.append((0,255,v))

    for v in range(0,256) :
      green_tmp_2.append((v,255,0))  
      
    for v in range(0,256) :
      green_tmp_3.append((v,255,v))
    
    i=2
    green_tmp=[green_tmp_1,green_tmp_2,green_tmp_3]
    while i >= 0 :
      if i == 0 :
	colors_green += green_tmp.pop(0)
      else : 	
        colors_green += green_tmp.pop(randint(0,i))
      i -= 1
      
    return colors_green

  
  def generate_blue(self) :
    ''' Generate blue gradients list. '''
    
    colors_blue=[]
    blue_tmp_1=[]
    blue_tmp_2=[]
    blue_tmp_3=[] 
    for v in range(0,256) :
      blue_tmp_1.append((0,v,255))

    for v in range(0,256) :
      blue_tmp_2.append((v,0,255))
      
    for v in range(0,256) :
      blue_tmp_3.append((v,v,255))    
    
    i=2
    blue_tmp=[blue_tmp_1,blue_tmp_2,blue_tmp_3]
    while i >= 0 :
      if i == 0 :
	colors_blue += blue_tmp.pop(0)
      else : 	
        colors_blue += blue_tmp.pop(randint(0,i))
      i -= 1
      
    return colors_blue
      
  
  def run(self) :
    control=0  # Control variable for colors the gradients direction (order).
    ii=0       # Loop counter controlling the colors gradients change in addition to the variable control.
	
    while self.runner :
      
      self.screen.fill(self.background_color) # Background color filling.
      
      if ii == 256 and control :
	# Reset the loop counter and switch the gradients direction (order) variable control.
	ii=0
	control=0
	self.colors=[self.generate_red(),self.generate_green(),self.generate_blue()][self.colors_indexer] # Change the current color list
	if self.rand_color :
	  # Set a new random color for the next time.
	  self.change_palette()
	  self.colors_indexer = randint(0,2)
	  
      elif ii == 256 and not control :
	# Reset the loop counter and switch the gradients direction (order) variable control.
	ii=0
	control=1
	self.colors=[self.generate_red(),self.generate_green(),self.generate_blue()][self.colors_indexer] # Change the current color list
	if self.rand_color :
	  # Set a new random color for the next time.
	  self.change_palette()
	  self.colors_indexer = randint(0,2)
      

      
      
      
      
      
      if self.rand_size :
	# Set the maximal value of the radius for the circle mode or the value of an half square side for the square mode.
        threshold=randint(self.min_size,self.max_size)
      else :
	# Set the maximal value of the radius for the circle mode or the value of an half square side for the square mode.
	threshold=self.size
      
      i=0
      color_index=0
      while i < threshold :
	
	if color_index == 768 :
	  color_index=0
	
	if not self.mode :
	  # Circle mode.
	  pygame.draw.circle(self.screen,self.colors[color_index],(self.center[0],self.center[1]),i+1,1)
	else :
	  # Square mode.
	  pygame.draw.rect(self.screen,self.colors[color_index],((int(self.center[0])-(i+1),int(self.center[1])-(i+1)),((i+1)*2,(i+1)*2)),1)
	
	i += 1
	color_index += 1
	
      if control == 0 :
	# We set the first color of the actual color list to the last, every loop turn in relationship to the value of the variable control.
	color_to_change=self.colors.pop(0)
	self.colors.append(color_to_change)
	
      elif control == 1 :
	# We set the last color of the actual color list to the first, every loop turn in relationship to the value of the variable control.
	color_to_change=self.colors.pop(-1)
	self.colors.insert(0,color_to_change)
	
      ii += 1
      
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
#colors=Colors(screen_width,screen_height)