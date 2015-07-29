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

from random import randint

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

class Bars() :
  def __init__(self,screen_width,screen_height,square=1,size="little",color_rect=(0,0,255),color_fill=(255,255,0),background_color=(0,0,0),rand_color=False,speed=0.05,music_filepath="",password="",recursion=0) :
    ''' '''
    self.screen_width=screen_width         # Get screen height for the fullscreen display size.
    self.screen_height=screen_height       # Get screen width for the fullscreen display size.
    
    self.square=square                     # Get the mode [ rectangles == 0 | squares == 1 ]
    
    
    ''' 
       Compute the [rectangle|squares] in relation ship of the selected size ["little"|"middle"|"big"]. 
    '''  
    if size == "big" :
      if square :
        factor=8 # Factor for squares size computing.
      else :  
        factor=4 # Factor for rectangle (bars) size computing.
    elif size == "middle" :
      if square :
	factor=4 # Factor for squares size computing.
      else :
	factor=2 # Factor for rectangle (bars) size computing.
    elif size == "little" :
      if square :
	factor=2 # Factor for squares size computing.
      else :
	factor=1 # Factor for rectangle (bars) size computing.
    
    square_list=[] # Temporary container for squares size computing.
    
    for v in [16,8,4,2] :
     # Finding the right size of the rectangles (bars) and spaces between them, in relationship to the screen resolution width. 
     try :
       assert(self.screen_width % v == 0)
       self.spaces=v
       self.rect_width=v*factor
       square_list.append(v)
       break
     except :
       pass
    
    for v in [16,8,4,2] :
      # Finding the right size of the rectangles (bars) and spaces between them, in relationship to the screen resolution height. 
     try :
       assert(self.screen_height % v == 0)
       self.rect_heigth=v*factor
       square_list.append(v)
       break
     except :
       pass
    
    if not square_list :
      # The resolution not match with the algorithm we can't define the sizes.
      return 
    
    if square :
      # Finding the right size of the squares and spaces between them, in relationship to the screen resolution height.
      self.spaces,self.rect_width,self.rect_heigth=min(square_list),min(square_list)*factor,min(square_list)*factor
    
    
    self.color_rect=color_rect              # Get the given background [rectangles (bars) | squares] color.
    self.color_fill=color_fill              # Get the given foreground [rectangles (bars) | squares] color.
    
    self.background_color=background_color  # Get the given display background color.
    self.speed=speed                        # Get the given bars animation speed for the sleep() function argument.
    
    self.password=password                  # Get the given password hash
    self.password_entry=""
    self.password_recursion=recursion
    self.password_check=Password()
    
    self.rand_color=rand_color              # Get the given random color mode argument as boolean value.
    
    
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
  
  def compute_width_counter(self) :
    ''' Method to count the number of [rectangles (bars) | squares] we can display in the width.
        self.spaces is the offset from the border so we must divided it by 2 to center our animation.
    '''
    
    i=((self.screen_width % self.rect_width+self.spaces) / 2)+((self.rect_width+self.spaces) ) # Offset from the border. We sacrify an [ rectangle (bar) | square ] for bugfix an value overflow 
                                                                                               # what result to draw an piece of [ rectangle (bar) | square ] if we unlucky.  
    counter=0
    while i < self.screen_width - (((self.screen_width % self.rect_width+self.spaces) / 2)+((self.rect_width+self.spaces))) :
      i += self.rect_width+self.spaces
      counter += 1
    
    self.width_start_offset= ((self.screen_width % self.rect_width+self.spaces) / 2)+((self.rect_width+self.spaces)) # Offset from the border.
    
    return counter  
    
  def compute_heigth_counter(self) :
    ''' Method to count the number of [rectangles (bars) | squares] we can display in the height.
        self.spaces is the offset from the border so we must divided it by 2 to center our animation.
    '''
    
    i=((self.screen_height % (self.rect_heigth+self.spaces)) / 2) + ((self.rect_heigth + self.spaces) ) # Offset from the border. We sacrify an [ rectangle (bar) | square ] for bugfix an value overflow 
                                                                                                        # what result to draw an piece of [ rectangle (bar) | square ] if we unlucky.  
    counter=0
    while i < self.screen_height - (((self.screen_height % (self.rect_heigth+self.spaces)) / 2) + ((self.rect_heigth + self.spaces))) :
      i += self.rect_heigth + self.spaces
      counter += 1
    
    self.heigth_start_offset= ((self.screen_height % (self.rect_heigth+self.spaces)) / 2) + ((self.rect_heigth + self.spaces)) # Offset from the border.
    
    return counter
  
    
  def run(self) :
    
    self.width_rect_counter=self.compute_width_counter()
    self.height_rect_counter=self.compute_heigth_counter()
    
    while self.runner :
      # Mainloop for one [ rectangle (bar) | square ] animation.
      
      self.screen.fill(self.background_color) # Background color filling.
      
   
      i=0
      x_coords=self.width_start_offset
      
      while i < self.width_rect_counter :
	# We run from left to the right.
	ii=0
	y_coords=self.heigth_start_offset
	
	while ii < self.height_rect_counter  :
	  # We run from top to bottom.
	  
	  if self.rand_color :
	    self.color_rect=(randint(0,255),randint(0,255),randint(0,255))
	  
	  pygame.draw.rect(self.screen,self.color_rect,((x_coords,y_coords),(self.rect_width,self.rect_heigth)),0)
	  
	  y_coords += (self.rect_heigth + self.spaces)
	  ii += 1
	
	i += 1   
        x_coords += self.rect_width+self.spaces 
        
      if not self.rand_color :
	# In the random color mode we don't need the foreground [ rectangle (bar) | square ] what do this loop.
        i=0
        x_coords=self.width_start_offset
        while i < self.width_rect_counter :
	  # We run from left to the right.
	  y_coords=self.heigth_start_offset
	  ii=0
	  y_coords=self.screen_height-self.heigth_start_offset-(self.rect_heigth + self.spaces)
	  
	  while ii < randint(0,self.height_rect_counter)  :
	    # We run from top to bottom.
	    
	    pygame.draw.rect(self.screen,self.color_fill,((x_coords,y_coords),(self.rect_width,self.rect_heigth)),0)
	    
	    y_coords -= (self.rect_heigth + self.spaces)
	    ii += 1
	    
	  i += 1	 
	  x_coords += self.rect_width+self.spaces
    
	
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
#bars=Bars(screen_width,screen_height)






