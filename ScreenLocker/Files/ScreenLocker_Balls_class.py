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

from random import randint, randrange, choice

from os.path import expanduser
path.append(expanduser('~')+"/Bureau/ScreenLocker/Files")
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

class Balls() :
  def __init__(self,screen_width,screen_height,mode=1,size="big",color_balls=['red','blue','yellow'],background_color=(0,0,0),speed=0.05,music_filepath="",password="",recursion=0) :
    ''' Run the balls animation with the given settings. '''
    
    self.screen_width=screen_width   # Get screen width  for the fullscreen display size.
    self.screen_height=screen_height # Get screen height for the fullscreen display size.
    
    self.mode=mode                   # Get the mode [ Circle == 0 | Halo == 1 ]
    
    ''' 
       Computing the ball size in relationship with the given size ["little"|"middle"|"big"].
    '''   
    if size == "big" :
      self.ball_size=16*8 
      if mode :
        self.inter_spacing=32 # A quarter of the balls size for the Halo mode.
      else :
	self.inter_spacing=0
      
    elif size == "middle" :
      self.ball_size=16*4 
      if mode :
        self.inter_spacing=16  # A quarter of the balls size for the Halo mode.
      else :
	self.inter_spacing=0
	
    elif size == "little" :
      self.ball_size=16*2 
      if mode :
        self.inter_spacing=8   # A quarter of the balls size for the Halo mode.
      else :
	self.inter_spacing=0
    
    
    ''' 
       Compute the balls colors in relation ship of the selected colors. 
    '''   
    colors_dict={"red":((255,0,0),(255,127,127)),
		 "green":((0,255,0),(127,255,127)),
		 "blue":((0,0,255),(127,127,255)),
		 "yellow":((255,255,0),(255,255,127)),
		 "pink":((255,0,255),(255,127,255)),
		 "turkish":((0,255,255),(127,255,255))}
  
    self.color_balls=[]
    for v in color_balls :
      self.color_balls.append(colors_dict.get(v)[0])
      self.color_balls.append(colors_dict.get(v)[1])
    
    
    
    self.background_color=background_color  # Get the given display background color.
    self.speed=speed                        # Get the given balls animation speed for the sleep() function argument.
    self.direction="Vertical"               # Set the direction arbitraly. Because the algorithm can draw the balls Horizontal but not implemented in the programm.
    
    self.password=password                  # Get the given password hash
    self.password_entry=""
    self.password_recursion=recursion
    self.password_check=Password()
    
    self.runner=True                        # Control animation keep-alive variable.  
    
    pygame.init()
    self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN,32)
    
    self.init_balls(self.direction)
    
    if music_filepath :
      self.play_backgroound_music(music_filepath)
    
    self.run()
  
  def play_backgroound_music(self,filepath) :
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(-1)
  
  def init_balls(self,direction) :
    self.balls=[]            # Container for the balls coordinates because they change.
    self.balls_colors=[]     # Container for the balls colors because they change. 
    self.balls_control=[]    # Container for the balls bouncing control. 
    self.balls_overvalue=[]  # Container for the balls bouncing highest value who can change. 
    self.balls_as_bounce=[]  # Container for the balls bouncing timer. 
    
    
    if direction == "Vertical" :
      counter=0
      while counter < self.screen_width-self.ball_size :
	# Compute a count of how many balls we display.
	counter += self.ball_size
      
      offset=self.screen_width-counter # Offset value compute from the border the the first ball ( must be divided by 2 for centering the balls).
      
      i=int(round(offset / 2.))        # Iterator start at the 1/2 from the screen border.
      while i < self.screen_width-int(round(offset / 2.)):
	'''loop for settings the balls coordinates,colors,start bouncing settings.'''
	ii=randrange(self.ball_size,self.screen_height-self.ball_size,self.ball_size) # Random highest y value for bouncing.
	self.balls.append([[i,ii],[self.ball_size,self.ball_size]])                   # Setting ball coordinates.
	
	self.balls_colors.append(choice(self.color_balls))                            # Random ball color.
	
	self.balls_control.append("down")                                             # Setting bouncing direction.
	
	self.balls_overvalue.append(ii)                                               # Setting highest y value for bouncing.
	
	self.balls_as_bounce.append(0)                                                # Bouncing control value.
	
	i += self.ball_size                                                           # Go to next ball.
	
    elif direction == "Horizontal" :
      
      counter=0
      while counter < self.screen_height-self.ball_size :
	# Compute a count of how many balls we display.
	counter += self.ball_size
      
      offset=self.screen_height-counter # Offset value compute from the border the the first ball ( must be divided by 2 for centering the balls).
      
      ii=int(round(offset / 2.))  # Iterator start at the 1/2 from the screen border.
      while ii < self.screen_height-int(round(offset / 2.))  : # self.screen_height-(self.spaces*4) to compute for compatibility
	
	i=randrange(self.ball_size,self.screen_width-self.ball_size,self.ball_size) # Random highest x value for bouncing.
	self.balls.append([[i,ii],[self.ball_size,self.ball_size]])                 # Setting ball coordinates.
	
	self.balls_colors.append(choice(self.color_balls))                          # Random ball color.
	
	self.balls_control.append("down")                                           # Setting bouncing direction.
	
	self.balls_overvalue.append(i)                                              # Setting highest x value for bouncing.
	
	self.balls_as_bounce.append(0)                                              # Bouncing timer control value.
	
	ii += self.ball_size                                                        # Go to next ball.
    
  def change_color(self,color) :
    ''' Color changing function '''
    ret=[]
    for v in color :
       if ( v == 0) :
	 ret.append(127) 
       elif (v  == 127) :
	 ret.append(0) 
       else :
	 ret.append(255)
    return (ret[0],ret[1],ret[2])	 
  
  def run(self) :
    
    while self.runner :
      
      # Balls animation mainloop.
      self.screen.fill(self.background_color) # Background color filling.
      
      i=0 # Iterator over all balls. 
      while i < len(self.balls) :
	# Big loop do for all balls configurating.
	  
	if self.balls_control[i] == "down" :
	  # Ball bouncing getting down.
          if self.direction == "Vertical" :
            self.balls[i][0][1] += self.ball_size # Increment y value from ball.
          elif self.direction == "Horizontal" :
            self.balls[i][0][0] += self.ball_size # Increment x value from ball.
        
        elif self.balls_control[i] == "up" :
	  # Ball bouncing getting up.
	  if self.direction == "Vertical" :
	    self.balls[i][0][1] -= self.ball_size # Decrement y value from ball.
	  elif self.direction == "Horizontal" :
	    self.balls[i][0][0] -= self.ball_size # Decrement x value from ball.
	
	
	if self.direction == "Vertical" :
	  ii=self.screen_height-self.ball_size    # Offset from down.
	  while ii >= self.balls[i][0][1] :
	    # Draw balls loop.
	    rect=((self.balls[i][0][0],ii),(self.ball_size,self.ball_size))
	    pygame.draw.ellipse(self.screen,self.balls_colors[i],rect,0)
	    
	    if self.inter_spacing :
	      # In case of halo mode draw the halo.
	      pygame.draw.ellipse(self.screen,self.background_color,rect,self.inter_spacing)
	    
	    ii -= self.ball_size # Go to next ball in the same column.
	  
	  if self.balls[i][0][1] >= self.screen_height-self.ball_size :
	    # Ball at the ground.
	    self.balls_colors[i]=self.change_color(self.balls_colors[i]) # Change the ball color because the ball reach the ground.  
	    self.balls_control[i]="up"                                   # Change bouncing direction because the ball reach the ground.       
	    self.balls_as_bounce[i] += 1                                 # Change ball bouncing timer.
	    if self.balls_as_bounce[i] > 3 :
	      # The ball as bounce 3 times.
	      self.balls_as_bounce[i] = 0                                # Reset ball bouncing timer.
	      self.balls_overvalue[i]=randrange(self.ball_size,self.screen_height-self.ball_size,self.ball_size) # Change highest y value for bouncing.
	      self.balls_colors[i]=choice((self.color_balls))            # Change the ball color because as bounce 3 times.
	      
	    
	  elif self.balls[i][0][1] == self.balls_overvalue[i] :
	    # Ball at the top.
	    self.balls_colors[i]=self.change_color(self.balls_colors[i]) # Change the ball color because the ball reach the top.  
	    self.balls_control[i]="down"                                 # Change bouncing direction because the ball reach the top. 
	    
	
	elif self.direction == "Horizontal" :
	  ii=self.screen_width-self.ball_size     # Offset from the left.
	  while ii >= self.balls[i][0][0] :
	     # Draw balls loop.
	    rect=((ii,self.balls[i][0][1]),(self.ball_size,self.ball_size))
	    pygame.draw.ellipse(self.screen,self.balls_colors[i],rect,0)
	    
	    if self.inter_spacing :
	      # In case of halo mode draw the halo.
	      pygame.draw.ellipse(self.screen,self.background_color,rect,self.inter_spacing)
	    
	    ii -= self.ball_size # Go to next ball in the same line.
	
	  if self.balls[i][0][0] >= self.screen_width-self.ball_size :
	    # Ball at the right border.
	    self.balls_colors[i]=self.change_color(self.balls_colors[i]) # Change the ball color because the ball reach the ground. 
	    self.balls_control[i]="up"                                   # Change bouncing direction because the ball reach the ground.
	    self.balls_as_bounce[i] += 1                                 # Change ball bouncing timer.
	    if self.balls_as_bounce[i] > 3 :
	      # The ball as bounce 3 times.
	      self.balls_as_bounce[i] = 0                                # Reset ball bouncing timer.     
	      self.balls_overvalue[i]=randrange(self.ball_size,self.screen_width-self.ball_size,self.ball_size) # Change highest x value for bouncing.
	      self.balls_colors[i]=choice((self.color_balls))            # Change the ball color because as bounce 3 times.
	      
	    
	  elif self.balls[i][0][0] == self.balls_overvalue[i] :
	    # Ball at the max left value.
	    self.balls_colors[i]=self.change_color(self.balls_colors[i]) # Change the ball color because the ball reach the left limit. 
	    self.balls_control[i]="down"                                 # Change bouncing direction because the ball reach the left limit.
	    
	
        i += 1 # Go to next ball.
	
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
#balls=Balls(screen_width,screen_height)






