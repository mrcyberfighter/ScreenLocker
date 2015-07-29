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

from Tkinter import *
import Pmw
from PIL import Image,ImageTk
import tkColorChooser

import shelve

from os.path import expanduser,basename

from sys import exit, path


path.append("/usr/share/ScreenLocker/Files")

from ScreenLocker_tkFileSelector import tkFileSelector
from ScreenLocker_password import Password

from ScreenLocker_Rollers_class import Rollers
from ScreenLocker_Bars_class import Bars
from ScreenLocker_Colors_class import Colors
from ScreenLocker_Balls_class import Balls

class GUI() :
  def __init__(self,bg_color=None,fg_color=None) :
  
    self.bg_color=bg_color
    self.fg_color=fg_color
  
    self.rollers_settings_saving_filepath="/usr/share/ScreenLocker/Settings/rollers_settings"
    self.bars_settings_saving_filepath="/usr/share/ScreenLocker/Settings/bars_settings"
    self.colors_settings_saving_filepath="/usr/share/ScreenLocker/Settings/colors_settings"
    self.balls_settings_saving_filepath="/usr/share/ScreenLocker/Settings/balls_settings"
    self.gui_settings_saving_filepath="/usr/share/ScreenLocker/Settings/gui_settings"
    self.password_settings_saving_filepath="/usr/share/ScreenLocker/Settings/passwd_settings"
    self.music_settings_saving_filepath="/usr/share/ScreenLocker/Settings/music_settings"
  
    self.password_set_hash=""
    self.password_set_recursion=0
  
    self.main_font_12="Courrier 12 normal"
    self.main_font_11="Courrier 11 normal"
    self.main_font_10="Courrier 10 normal"
    self.main_font_09="Courrier 9 normal"
  
  
    self.main_window_instance=Tk()
    self.screen_width=self.main_window_instance.winfo_screenwidth()
    self.screen_height=self.main_window_instance.winfo_screenheight()
  
    self.main_window_instance.title("ScreenLocker: Main configuration")
    self.main_window_instance.resizable(False,False)
    
    if bg_color or fg_color :
      if not bg_color :
	self.bg_color=self.main_window_instance.cget("bg")
      self.main_window_instance.tk_setPalette(background=self.bg_color,foreground=self.fg_color)
  
    self._init_images()
  
    self._init_menu()
  
  
    Pmw.initialise(self.main_window_instance)
  
    self._init_main_window()
  
    self._init_rollers_animation_window()
  
    self._init_bars_animation_window()
  
    self._init_colors_animation_window()
  
    self._init_balls_animation_window()
  
    self._init_about_and_gui_settings()
  
    self.main_notebook_page_reference="Main configuration"
  
    self.main_notebook_instance.setnaturalsize()
    self.main_notebook_instance.pack()
  
    self.main_window_instance.mainloop()

  def _init_menu(self) :
    self.main_menubutton=Menubutton(self.main_window_instance,text="      Main menu      ",borderwidth=2,relief='flat')
    self.main_menu=Menu(self.main_menubutton,borderwidth=2,relief="sunken")
    self.main_menu.add_command(label="Main window      ",command=self.display_main_configuration_notebook_page)
    self.main_menu.add_command(label="Configure Rollers",command=self.display_rollers_configuration_notebook_page)
    self.main_menu.add_command(label="Configure Bars   ",command=self.display_bars_configuration_notebook_page)
    self.main_menu.add_command(label="Configure Colors ",command=self.display_colors_configuration_notebook_page)
    self.main_menu.add_command(label="Configure Balls  ",command=self.display_balls_configuration_notebook_page)
    self.main_menu.add_command(label="Configure GUI    ",command=self.display_about_configuration_notebook_page)
    self.main_menubutton.config(menu=self.main_menu)

    self.main_menubutton.pack(anchor="nw")
  
  def _init_main_window(self) :
  
    self.gui_settings_getting()
  
    self.main_notebook_instance=Pmw.NoteBook(self.main_window_instance,tabpos=None)
  
    self.main_notebook_instance_page =self.main_notebook_instance.add("Main configuration")

    self.group_main_window_1 = Pmw.Group(self.main_notebook_instance_page,tag_text="Use a password")   # section 1 main window: password to quit setting.

    self.group_main_window_2 = Pmw.Group(self.main_notebook_instance_page,tag_text="Use a music file") # section 2 main window: set background music setting.

    self.group_main_window_3 = Pmw.Group(self.main_notebook_instance_page,tag_text="Action")
  
  
  
    self.group_main_window_1.component("tag").config(font=self.main_font_12)
    self.group_main_window_2.component("tag").config(font=self.main_font_12)
    self.group_main_window_3.component("tag").config(font=self.main_font_12)
  
    # Construct section 1 main window: password to quit setting.
  
    self.password_settings_getting()
    self.music_settings_getting()
  
    self.use_password_control_var=BooleanVar(value=self.password_use)
    self.use_password_checkbox=Checkbutton(self.group_main_window_1.interior(),font=self.main_font_10,variable=self.use_password_control_var,text="Use a password to quit")
  
    self.use_password_balloon_checkbox = Pmw.Balloon(self.group_main_window_1.interior())
    self.use_password_balloon_checkbox.component('label').config(bg=self.bg_color)
    self.use_password_balloon_checkbox.bind(self.use_password_checkbox, 'Password protection activate')
  
    self.password_label=Label(self.group_main_window_1.interior(),font=self.main_font_10,text="Password")
    self.password_entry=Entry(self.group_main_window_1.interior(),font=self.main_font_10,show="*",width=40,justify="center")
    if self.password_set_recursion :
      self.password_entry.insert(0,self.password_set_recursion*'a')
    
      self.use_password_checkbox.select()
    
    self.password_entry.bind("<KeyRelease>",self.password_entry_check)
  
    self.confirm_label=Label(self.group_main_window_1.interior(),font=self.main_font_10, text="Confirm")
    self.confirm_entry=Entry(self.group_main_window_1.interior(),font=self.main_font_10,show="*",width=40,justify="center")
    if self.password_set_recursion :
      self.confirm_entry.insert(0,self.password_set_recursion*'a')
    
    self.confirm_entry.bind("<KeyRelease>",self.confirm_entry_check)
  
    self.set_as_password_button=Button(self.group_main_window_1.interior(),font=self.main_font_10,text="Set as password",command=self.set_password)
    self.reset_password_button=Button(self.group_main_window_1.interior(),font=self.main_font_10,text="Reset",command=self.reset_password)

    self.use_password_checkbox.grid(row=0,column=0,columnspan=22)
    self.password_label.grid(row=1,column=2,columnspan=8,padx=10)
    self.password_entry.grid(row=1,column=10,columnspan=15)
    self.confirm_label.grid(row=2,column=2,columnspan=8,padx=10)
    self.confirm_entry.grid(row=2,column=10,columnspan=15)
    self.set_as_password_button.grid(row=3,column=10,columnspan=5,pady=5)
    self.reset_password_button.grid(row=3,column=22,columnspan=3,pady=5)

    # Contruct section 2 main window: set background music setting.
  
    self.use_music_control_var=BooleanVar(value=self.music_set_on)
    self.use_music_checkbox=Checkbutton(self.group_main_window_2.interior(),font=self.main_font_10,variable=self.use_music_control_var,text="Use a background music")
    self.use_music_balloon_checkbox = Pmw.Balloon(self.group_main_window_1.interior())
    self.use_music_balloon_checkbox.component('label').config(bg=self.bg_color)
    self.use_music_balloon_checkbox.bind(self.use_music_checkbox, 'Enable background music in fullscreen mode.')
  
    self.select_music_file_button=Button(self.group_main_window_2.interior(),font=self.main_font_10,text="Select file",command=self.set_music_file)
    self.select_music_file_balloon_button = Pmw.Balloon(self.group_main_window_2.interior())
    self.select_music_file_balloon_button.component('label').config(bg=self.bg_color)
    self.select_music_file_balloon_button.bind(self.select_music_file_button, 'Select a background music file to play in fullscreen mode.\nSimply quit the file selector to reset the music file.\nOr disable the checkbox to not playing music.')
    self.music_filename_entry=Entry(self.group_main_window_2.interior(),font=self.main_font_10,width=36,state="readonly",readonlybackground=self.bg_color,justify="center")
    if self.music_filepath :
      self.music_filename_entry.config(state="normal")
      self.music_filename_entry.delete(0,END)
      self.music_filename_entry.insert(0,basename(self.music_filepath))
      self.music_filename_entry.config(state="readonly")
    
    self.use_music_checkbox.grid(row=0,column=0,columnspan=25)
    self.select_music_file_button.grid(row=1,column=2,columnspan=8,padx=10)
    self.music_filename_entry.grid(row=1,column=10,columnspan=15,stick="NS")
  
  
    # Contruct section 3 main window: choosing the animation to launch and launching button.
  
    # Animation choosing section
    self.selection_animation_frame=LabelFrame(self.group_main_window_3.interior(),font=self.main_font_10,text="Select animation")
  
    self.control_selection_variable=StringVar(value="Rolls")
    self.rolls_animation_radiobutton=Radiobutton(self.selection_animation_frame, text=" Rolls   animation     ",font=self.main_font_10,variable=self.control_selection_variable,value="Rolls")
    self.bars_animation_radiobutton=Radiobutton(self.selection_animation_frame,  text=" Bars    animation     ",font=self.main_font_10,variable=self.control_selection_variable,value="Bars")
    self.colors_animation_radiobutton=Radiobutton(self.selection_animation_frame,text=" Colors animation     ",font=self.main_font_10,variable=self.control_selection_variable,value="Colors")
    self.balls_animation_radiobutton=Radiobutton(self.selection_animation_frame, text=" Balls   animation     ",font=self.main_font_10,variable=self.control_selection_variable,value="Balls")

    self.rolls_animation_radiobutton.grid(row=0,column=0,padx=5,sticky="NSEW")
    self.bars_animation_radiobutton.grid(row=1,column=0,padx=5,sticky="NSEW")
    self.colors_animation_radiobutton.grid(row=2,column=0,padx=5,sticky="NSEW")
    self.balls_animation_radiobutton.grid(row=3,column=0,padx=5,sticky="NSEW")
  
    self.selection_animation_frame.grid(row=0,column=0,padx=15,pady=15,sticky="NSEW")
  
    # Launch button
    self.launcher_button_frame=LabelFrame(self.group_main_window_3.interior(),font=self.main_font_10,text="Action")
  
    self.launcher_button=Button(self.launcher_button_frame,image=self.launch_image_instance,borderwidth=5,relief="raised",command=self.launch_animation)
  
    self.launcher_balloon_button = Pmw.Balloon(self.group_main_window_1.interior())
    self.launcher_balloon_button.component('label').config(bg=self.bg_color)
    self.launcher_balloon_button.bind(self.launcher_button, 'Launch the selected animation in fullscreen mode.\nWith the current settings.')
  
    self.launcher_button.grid(padx=15,pady=15)
    self.launcher_button_frame.grid(row=0,column=1,padx=15,pady=15,sticky="NSEW")
  
  
    # pack GUI composant and entry mainloop.
    self.group_main_window_1.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)
    self.group_main_window_2.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)
    self.group_main_window_3.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)

  def launch_animation(self) :
    tk_objt=self.main_window_instance
    screen_width=tk_objt.winfo_screenwidth()
    screen_height=tk_objt.winfo_screenheight()

    if self.use_password_control_var.get() :
      self.password_settings_getting()
      passwd=self.password_set_hash
      recursions=self.password_set_recursion
    else :
      passwd=""
      recursions=0
  
    if self.use_music_control_var.get() and self.music_filepath :
      background_music_filepath=self.music_filepath
    else :
      background_music_filepath=""
    
  
    if self.control_selection_variable.get() == "Rolls" :
      self.get_rollers_configuration()
      Rollers(screen_width,screen_height,size=self.rollers_size,colors=self.rollers_colors,background_color=self.rollers_display_background,speed=float(self.rollers_speed),direction=self.rollers_direction,music_filepath=background_music_filepath,password=passwd,recursion=recursions)

    elif self.control_selection_variable.get() == "Bars" :
      self.get_bars_configuration()
      Bars(screen_width,screen_height,square=self.bars_square,size=self.bars_size,color_rect=self.bars_color_rect_background,color_fill=self.bars_color_rect_foreground,background_color=self.bars_display_background,rand_color=self.bars_rand_color,speed=float(self.bars_speed),music_filepath=background_music_filepath,password=passwd,recursion=recursions)
     
    elif self.control_selection_variable.get() == "Colors" :
      self.get_colors_configuration()
      Colors(screen_width,screen_height,square=self.colors_square,size=self.colors_size,fullscreen=self.colors_fullscreen,color=self.colors_colors,rand_color=self.colors_rand_color,rand_size=self.colors_rand_size,background_color=self.colors_display_background,speed=float(self.colors_speed),music_filepath=background_music_filepath,password=passwd,recursion=recursions)
  
    elif self.control_selection_variable.get() == "Balls" :
      self.get_balls_configuration()
      Balls(screen_width,screen_height,mode=self.balls_square,size=self.balls_size,color_balls=self.balls_colors,background_color=self.balls_display_background,speed=float(self.balls_speed),music_filepath=background_music_filepath,password=passwd,recursion=recursions)
    
  def password_entry_check(self,event) :

    for char in self.password_entry.get() :
      if not char.isalnum() :
	self.password_entry.delete(0,END)
        self.password_inform_error_toplevel(title="Password error",msg="The password must only contains\nalphanumeric characters:\n-) Lowercase letters.\n-) Uppercase letters.\n-) Digits.                  \n...",button_label=" Understand ")
        break

  def confirm_entry_check(self,event) :
    for char in self.confirm_entry.get() :
      if not char.isalnum() :
	self.confirm_entry.delete(0,END)
	self.password_inform_error_toplevel(title="Password error",msg="The password must only contains\nalphanumeric characters:\n-) Lowercase letters.\n-) Uppercase letters.\n-) Digits.                  \n...",button_label=" Understand ")
	break

  def set_password(self) :
    for char in self.password_entry.get() :
      if not char.isalnum() :
	self.password_entry.delete(0,END)
        self.password_inform_error_toplevel(title="Password error",msg="The password must only contains\nalphanumeric characters:\n-) Lowercase letters.\n-) Uppercase letters.\n-) Digits.                  \n...",button_label=" Understand ")
        return
    
    for char in self.confirm_entry.get() :
      if not char.isalnum() :
	self.confirm_entry.delete(0,END)
	self.password_inform_error_toplevel(title="Password error",msg="The password must only contains\nalphanumeric characters:\n-) Lowercase letters.\n-) Uppercase letters.\n-) Digits.                  \n...",button_label=" Understand ")
	return
    
    if self.password_entry.get() != self.confirm_entry.get() :
      self.password_entry.delete(0,END)
      self.confirm_entry.delete(0,END)
      self.password_inform_error_toplevel(title="Password error",msg="The passwords don't match !!!",button_label="    Ok    ")
      return
  
    if not self.password_entry.get() or not self.confirm_entry.get() :
      self.password_entry.delete(0,END)
      self.confirm_entry.delete(0,END)
      self.password_inform_error_toplevel(title="Password error",msg="Password field empty !!!",button_label="    Ok    ")
      return
  
    else :
      self.password_set_hash=passwd.gen_password_hash(self.password_entry.get(),len(self.password_entry.get()))
      self.password_set_recursion=len(self.password_entry.get())
      self.password_use=True
      self.use_password_control_var.set(True)
      self.use_password_checkbox.select()
      self.password_settings_saving()
      self.password_inform_error_toplevel(title="Password stored",msg="Password sucessfull set and stored !!!",button_label="    Ok    ")
    
  def reset_password(self) :
    self.password_set_hash=""
    self.password_set_recursion=0
    self.password_use=False
    self.password_settings_saving()
    self.confirm_entry.delete(0,END)
    self.password_entry.delete(0,END)
    self.use_password_checkbox.deselect()

  def set_music_file(self) :
  
    self.music_file_selection=tkFileSelector(self.main_window_instance,start_dir=expanduser("~"),filetypes=["*.mp3","*.wav"],title="Select a music file.",color_1=self.fg_color,color_2=self.bg_color,highlight_color_items="#c9c9c9")
    if self.music_file_selection.select_filepath :
      self.music_filepath=self.music_file_selection.select_filepath
      self.music_set_on=True
      self.music_filename_entry.config(state="normal")
      self.music_filename_entry.delete(0,END)
      self.music_filename_entry.insert(0,basename(self.music_file_selection.select_filepath))
      self.music_filename_entry.config(state="readonly")
      self.use_music_checkbox.select()
      del(self.music_file_selection)
      self.music_settings_saving()
    else :
      self.music_filepath=""
      self.music_set_on=False
      self.music_filename_entry.config(state="normal")
      self.music_filename_entry.delete(0,END)
      self.music_filename_entry.config(state="readonly")
      self.use_music_checkbox.deselect()
      self.music_settings_saving()

  def _init_rollers_animation_window(self) :
  
    self.get_saved_rollers_configuration()
  
    self.main_notebook_instance_page =self.main_notebook_instance.add("Rollers configuration")

    self.group_rollers_window_1 = Pmw.Group(self.main_notebook_instance_page,tag_text="Description")

    self.group_rollers_window_2 = Pmw.Group(self.main_notebook_instance_page,tag_text="Settings")

    self.group_rollers_window_3 = Pmw.Group(self.main_notebook_instance_page,tag_text="Actions")

    self.group_rollers_window_1.component("tag").config(font=self.main_font_12)
    self.group_rollers_window_2.component("tag").config(font=self.main_font_12)
    self.group_rollers_window_3.component("tag").config(font=self.main_font_12)
  
    # Contruct rollers window section 1: description and screenshot.
  
    self.rollers_description_message=Message(self.group_rollers_window_1.interior(),text="Rollers rolls overs the screen\nhorizontal or vertical\nwith seven colors available\nin the wanted speed.",font=self.main_font_09,width=256)
    self.rollers_screenshot_button=Button(self.group_rollers_window_1.interior(),image=self.rollers_image_screenshot_instance)
    self.rollers_description_message.pack(side=LEFT,padx=15,pady=0)
    self.rollers_screenshot_button.pack(side=RIGHT,padx=15,pady=5)
  
  
    # Contruct rollers window section 2: rollers animation settings.
  

    self.rollers_size_label=Label(self.group_rollers_window_2.interior(),text="Size",font=self.main_font_10)
    self.rollers_size_control_variable=StringVar(value=self.rollers_size)
    self.rollers_size_little_radiobutton=Radiobutton(self.group_rollers_window_2.interior(),   text="Little    ",variable=self.rollers_size_control_variable,value="little",font=self.main_font_10)
    self.rollers_size_middle_radiobutton=Radiobutton(self.group_rollers_window_2.interior(),   text="Middle    ",variable=self.rollers_size_control_variable,value="middle",font=self.main_font_10)
    self.rollers_size_big_radiobutton=Radiobutton(self.group_rollers_window_2.interior(),      text="Big       ",variable=self.rollers_size_control_variable,value="big",font=self.main_font_10)
  
    self.rollers_size_label.grid(row=0,column=0,columnspan=5,sticky="EW")
    self.rollers_size_little_radiobutton.grid(row=0,column=5,columnspan=5,sticky="EW")
    self.rollers_size_middle_radiobutton.grid(row=0,column=10,columnspan=5,sticky="EW")
    self.rollers_size_big_radiobutton.grid(row=0,column=15,columnspan=5,sticky="EW")

    self.rollers_direction_label=Label(self.group_rollers_window_2.interior(),text="Direction",font=self.main_font_10)
    self.rollers_direction_control_variable=StringVar(value=self.rollers_direction)
    self.rollers_direction_vertical_radiobutton=Radiobutton(self.group_rollers_window_2.interior(),   text="Vertical",variable=self.rollers_direction_control_variable,value="Vertical",font=self.main_font_10)
    self.rollers_direction_horizontal_radiobutton=Radiobutton(self.group_rollers_window_2.interior(),   text="Horizontal",variable=self.rollers_direction_control_variable,value="Horizontal",font=self.main_font_10)
  
    self.rollers_direction_label.grid(row=1,column=0,columnspan=5,sticky="EW")
    self.rollers_direction_vertical_radiobutton.grid(row=1,column=5,columnspan=5,sticky="EW")
    self.rollers_direction_horizontal_radiobutton.grid(row=1,column=10,columnspan=5,sticky="EW")

    self.rollers_set_colors_and_numbers=Button(self.group_rollers_window_2.interior(),text="    Rollers to set on:    ",font=self.main_font_10,justify="center")
    self.rollers_set_colors_and_numbers.grid(row=2,column=3,columnspan=16,sticky="EW")
  
    if self.rollers_colors.__contains__("red") :
      color="red"
    else :
      color=""
    
    self.rollers_set_red_control_var=StringVar(value=color)
    self.rollers_set_red=Checkbutton(self.group_rollers_window_2.interior(),    text="red      ",font=self.main_font_10,variable=self.rollers_set_red_control_var,onvalue="red",offvalue="",command=self.rollers_colors_check)
  
    if self.rollers_colors.__contains__("pink") :
      color="pink"
    else :
      color=""
    self.rollers_set_pink_control_var=StringVar(value=color)
    self.rollers_set_pink=Checkbutton(self.group_rollers_window_2.interior(),   text="pink   ",font=self.main_font_10,variable=self.rollers_set_pink_control_var,onvalue="pink",offvalue="",command=self.rollers_colors_check)
  
    if self.rollers_colors.__contains__("turkish") :
      color="turkish"
    else :
      color=""
    self.rollers_set_turkish_control_var=StringVar(value=color)
    self.rollers_set_turkish=Checkbutton(self.group_rollers_window_2.interior(),text="turkish",font=self.main_font_10,variable=self.rollers_set_turkish_control_var,onvalue="turkish",offvalue="",command=self.rollers_colors_check)
  
    if self.rollers_colors.__contains__("green") :
      color="green"
    else :
      color=""
    self.rollers_set_green_control_var=StringVar(value=color)
    self.rollers_set_green=Checkbutton(self.group_rollers_window_2.interior(),  text="green  ",font=self.main_font_10,variable=self.rollers_set_green_control_var,onvalue="green",offvalue="",command=self.rollers_colors_check)
  
    if self.rollers_colors.__contains__("blue") :
      color="blue"
    else :
      color=""
    self.rollers_set_blue_control_var=StringVar(value=color)
    self.rollers_set_blue=Checkbutton(self.group_rollers_window_2.interior(),   text="blue   ",font=self.main_font_10,variable=self.rollers_set_blue_control_var,onvalue="blue",offvalue="",command=self.rollers_colors_check)
  
    if self.rollers_colors.__contains__("yellow") :
      color="yellow"
    else :
      color=""
    self.rollers_set_yellow_control_var=StringVar(value=color)
    self.rollers_set_yellow=Checkbutton(self.group_rollers_window_2.interior(), text="yellow ",font=self.main_font_10,variable=self.rollers_set_yellow_control_var,onvalue="yellow",offvalue="",command=self.rollers_colors_check)
  
    self.rollers_set_red.grid(row=3,column=4)
    self.rollers_set_pink.grid(row=3,column=8)
    self.rollers_set_turkish.grid(row=3,column=12)
  
    self.rollers_set_green.grid(row=4,column=4)
    self.rollers_set_blue.grid(row=4,column=8)
    self.rollers_set_yellow.grid(row=4,column=12)
  
    self.rollers_users_display_background=self.rollers_display_background
    self._generate_colors_images(self.rollers_image_set_display_background_file,"/usr/share/ScreenLocker/Images/color_selection/rollers_display_background.png",self.rollers_users_display_background)
    self.rollers_image_set_display_background_instance=ImageTk.PhotoImage(image=self.rollers_image_set_display_background_file)
    self.rollers_display_background_button=Button(self.group_rollers_window_2.interior(),text="Window background color",font=self.main_font_10,compound="left",image=self.rollers_image_set_display_background_instance,command=self.get_users_rollers_display_background)
  
    self.rollers_display_background_button.grid(row=5,column=0,padx=15,pady=3,columnspan=25)

    self.rollers_speed_label=Label(self.group_rollers_window_2.interior(),text="Speed animation",font=self.main_font_10)
  
    self.rollers_speed_control_variable=StringVar(value=str(self.rollers_speed).zfill(3))
  
    self.rollers_speed_spinbox=Spinbox(self.group_rollers_window_2.interior(),from_="0.001",to_="0.100",increment="0.001",textvariable=self.rollers_speed_control_variable,takefocus=FALSE,state="readonly",justify=CENTER,readonlybackground=self.bg_color,buttonbackground=self.bg_color)

    self.rollers_speed_label.grid(row=6,column=0,padx=15,pady=3,columnspan=5)
    self.rollers_speed_spinbox.grid(row=6,column=5,padx=15,pady=3,columnspan=20)

 
    # Contruct rollers window section 3: rollers animation settings saving | reset.
    self.rollers_save_configuration_button=Button(self.group_rollers_window_3.interior(), text="   Save configuration    ",font=self.main_font_10,command=self.get_users_rollers_configuration)
    self.rollers_reset_configuration=Button(self.group_rollers_window_3.interior(),text="     Reset to default     ",font=self.main_font_10,command=self.set_default_rollers_configuration)
    self.rollers_save_configuration_button.grid(row=0,column=0,columnspan=10,padx=15,pady=3,sticky="EW")
    self.rollers_reset_configuration.grid(row=0,column=10,columnspan=10,padx=15,pady=3,sticky="EW")
  
    self.group_rollers_window_1.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)
    self.group_rollers_window_2.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)
    self.group_rollers_window_3.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)

  def rollers_colors_check(self) :
    self.colors_choosing_callback(colors=[self.rollers_set_red_control_var,self.rollers_set_pink_control_var,self.rollers_set_turkish_control_var,self.rollers_set_green_control_var,self.rollers_set_blue_control_var,self.rollers_set_yellow_control_var],default=self.rollers_set_red_control_var,switch=False)

  def set_default_rollers_configuration(self) :
  
    self.rollers_size="big"
    self.rollers_direction="Vertical"
    self.rollers_colors=["red"]
    self.rollers_speed=0.005
    self.rollers_display_background=(0,0,0)

    self.rollers_settings_saving()
  
    self.main_notebook_instance.delete("Rollers configuration")
    self._init_rollers_animation_window()
    self.display_rollers_configuration_notebook_page()
  
  def get_users_rollers_configuration(self) :
    self.confirm_asking_toplevel(msg="Save current rollers configuration")
    if self.confirm_toplevel_answers :
      self.set_saved_rollers_configuration()

  def get_rollers_configuration(self) :
    self.rollers_size=self.rollers_size_control_variable.get()
    self.rollers_direction=self.rollers_direction_control_variable.get()
    self.rollers_colors=[ x.get() for x in [self.rollers_set_red_control_var,self.rollers_set_pink_control_var,self.rollers_set_turkish_control_var,self.rollers_set_green_control_var,self.rollers_set_blue_control_var,self.rollers_set_yellow_control_var] if x.get() ]
  
    self.rollers_speed=float(self.rollers_speed_control_variable.get())
    self.rollers_display_background=self.rollers_users_display_background
  
  

  def set_saved_rollers_configuration(self) :
    self.rollers_size=self.rollers_size_control_variable.get()
    self.rollers_direction=self.rollers_direction_control_variable.get()
    self.rollers_colors=[ x.get() for x in [self.rollers_set_red_control_var,self.rollers_set_pink_control_var,self.rollers_set_turkish_control_var,self.rollers_set_green_control_var,self.rollers_set_blue_control_var,self.rollers_set_yellow_control_var] if x.get() ]
  
    self.rollers_speed=float(self.rollers_speed_control_variable.get())
    self.rollers_display_background=self.rollers_users_display_background
  
    self.rollers_settings_saving()

  def get_saved_rollers_configuration(self) :
     self.rollers_settings_getting()

  def get_users_rollers_display_background(self) :
    color=tkColorChooser.askcolor(color=self.rollers_display_background)
  
    if color[0] and color[1] :
      self.rollers_users_display_background=color[0]
      self._generate_colors_images(self.rollers_image_set_display_background_file,"/usr/share/ScreenLocker/Images/color_selection/rollers_display_background.png",self.rollers_users_display_background)
      self.rollers_image_set_display_background_instance=ImageTk.PhotoImage(image=self.rollers_image_set_display_background_file)
      self.rollers_display_background_button.config(image=self.rollers_image_set_display_background_instance)
    
    else :
      pass

  def _init_bars_animation_window(self) :
  
    self.get_saved_bars_configuration()
  
    self.main_notebook_instance_page =self.main_notebook_instance.add("Bars configuration")

    self.group_bars_window_1 = Pmw.Group(self.main_notebook_instance_page,tag_text="Description")

    self.group_bars_window_2 = Pmw.Group(self.main_notebook_instance_page,tag_text="Settings")

    self.group_bars_window_3 = Pmw.Group(self.main_notebook_instance_page,tag_text="Actions")

    self.group_bars_window_1.component("tag").config(font=self.main_font_12)
    self.group_bars_window_2.component("tag").config(font=self.main_font_12)
    self.group_bars_window_3.component("tag").config(font=self.main_font_12)
  
    # Contruct bars window section 1: description and screenshot.
  
    self.bars_description_message=Message(self.group_bars_window_1.interior(),text="Animated bars or squares\nbouncing, on an background\nmesh,available in 3 sizes,\nin the colors and speed you like.",font=self.main_font_09,width=256)
    self.bars_screenshot_button=Button(self.group_bars_window_1.interior(),image=self.bars_image_screenshot_instance)
    self.bars_description_message.pack(side=LEFT,padx=15,pady=0)
    self.bars_screenshot_button.pack(side=RIGHT,padx=15,pady=5)
  
    # Contruct bars window section 2: bars animation settings.
    self.bars_size_label=Label(self.group_bars_window_2.interior(),text="Size",font=self.main_font_10)
    self.bars_size_control_variable=StringVar(value=self.bars_size)
    self.bars_size_little_radiobutton=Radiobutton(self.group_bars_window_2.interior(),   text="Little",variable=self.bars_size_control_variable,value="little",font=self.main_font_10)
    self.bars_size_middle_radiobutton=Radiobutton(self.group_bars_window_2.interior(),   text="Middle",variable=self.bars_size_control_variable,value="middle",font=self.main_font_10)
    self.bars_size_big_radiobutton=Radiobutton(self.group_bars_window_2.interior(),      text="Big      ",variable=self.bars_size_control_variable,value="big",font=self.main_font_10)

    self.bars_size_label.grid(row=0,column=0,columnspan=5,sticky="EW")
    self.bars_size_little_radiobutton.grid(row=0,column=5,columnspan=5,sticky="EW")
    self.bars_size_middle_radiobutton.grid(row=0,column=10,columnspan=5,sticky="EW")
    self.bars_size_big_radiobutton.grid(row=0,column=15,columnspan=5,sticky="EW")

  
    self.bars_mode_label=Label(self.group_bars_window_2.interior(),text="Mode",font=self.main_font_10)
    self.bars_mode_control_variable=IntVar(value=self.bars_square)
    self.bars_mode_rectangle_radiobutton=Radiobutton(self.group_bars_window_2.interior(),text="Rectangles                   ",variable=self.bars_mode_control_variable,value=0,font=self.main_font_10)
    self.bars_mode_square_radiobutton=Radiobutton(self.group_bars_window_2.interior(),   text="Square",variable=self.bars_mode_control_variable,value=1,font=self.main_font_10)

    self.bars_mode_label.grid(row=1,column=0,columnspan=5,sticky="EW")
    self.bars_mode_rectangle_radiobutton.grid(row=1,column=5,columnspan=10,sticky="EW")
    self.bars_mode_square_radiobutton.grid(row=1,column=15,columnspan=10,sticky="EW")
   
    self.bars_users_background_color=self.bars_color_rect_background
    self._generate_colors_images(self.bars_image_set_bars_background_file,"/usr/share/ScreenLocker/Images/color_selection/bars_background.png",self.bars_users_background_color)
    self.bars_image_set_bars_background_instance=ImageTk.PhotoImage(image=self.bars_image_set_bars_background_file)
    self.bars_background_button=Button(self.group_bars_window_2.interior(),text=" Background bars ",font=self.main_font_10,compound="left",image=self.bars_image_set_bars_background_instance,command=self.get_users_bars_background_color)
     
    self.bars_users_foreground_color=self.bars_color_rect_foreground
    self._generate_colors_images(self.bars_image_set_bars_foreground_file,"/usr/share/ScreenLocker/Images/color_selection/bars_foreground.png",self.bars_users_foreground_color)
    self.bars_image_set_bars_foreground_instance=ImageTk.PhotoImage(image=self.bars_image_set_bars_foreground_file)
    self.bars_foreground_button=Button(self.group_bars_window_2.interior(),text=" Foreground bars ",font=self.main_font_10,compound="left",image=self.bars_image_set_bars_foreground_instance,command=self.get_users_bars_foreground_color)

    self.bars_background_button.grid(row=2,column=0,columnspan=10,padx=15,pady=3,sticky="EW")
    self.bars_foreground_button.grid(row=2,column=10,columnspan=10,padx=15,pady=3,sticky="EW")
   
    self.bars_random_colors_using=self.bars_rand_color
    if self.bars_random_colors_using :
      button_text=" Random bars colors = On  "
    else :
      button_text=" Random bars colors = Off "
    
    self.bars_random_colors_button=Button(self.group_bars_window_2.interior(),text=button_text,font=self.main_font_10,command=self.set_bars_random_color)
    self.bars_random_colors_button.grid(row=3,column=0,columnspan=25,padx=15,pady=3,sticky="EW")
  
    self.bars_users_display_background=self.bars_display_background
    self._generate_colors_images(self.bars_image_set_display_background_file,"/usr/share/ScreenLocker/Images/color_selection/bars_display_background.png",self.bars_users_display_background)
    self.bars_image_set_display_background_instance=ImageTk.PhotoImage(image=self.bars_image_set_display_background_file)
    self.bars_display_background_button=Button(self.group_bars_window_2.interior(),text="Window background color",font=self.main_font_10,compound="left",image=self.bars_image_set_display_background_instance,command=self.get_users_bars_display_background)
    self.bars_display_background_button.grid(row=5,column=0,padx=15,pady=3,columnspan=25)
  
    self.bars_speed_control_variable=StringVar(value=str(self.bars_speed))
    self.bars_speed_label=Label(self.group_bars_window_2.interior(),text="Speed animation",font=self.main_font_10)

    self.bars_speed_spinbox=Spinbox(self.group_bars_window_2.interior(),from_="0.01",to="1.00",increment="0.01",textvariable=self.bars_speed_control_variable,takefocus=FALSE,state="readonly",justify=CENTER,readonlybackground=self.bg_color,buttonbackground=self.bg_color)

    self.bars_speed_label.grid(row=6,column=0,padx=15,pady=3,columnspan=5)
    self.bars_speed_spinbox.grid(row=6,column=5,padx=15,pady=3,columnspan=20)

 
    # Contruct bars window section 3: bars animation settings saving | reset.
    self.bars_save_configuration_button=Button(self.group_bars_window_3.interior(), text="   Save configuration    ",font=self.main_font_10,command=self.get_users_bars_configuration)
    self.bars_reset_configuration=Button(self.group_bars_window_3.interior(),text="     Reset to default     ",font=self.main_font_10,command=self.set_default_bars_configuration)
    self.bars_save_configuration_button.grid(row=0,column=0,columnspan=10,padx=15,pady=3,sticky="EW")
    self.bars_reset_configuration.grid(row=0,column=10,columnspan=10,padx=15,pady=3,sticky="EW")
  
    self.group_bars_window_1.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)
    self.group_bars_window_2.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)
    self.group_bars_window_3.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)



  def set_default_bars_configuration(self) :
  
    self.bars_size="middle"
    self.bars_square=0
    self.bars_color_rect_background=(0,0,255)
    self.bars_color_rect_foreground=(255,255,0)
    self.bars_rand_color=False
    self.bars_speed=  0.05
    self.bars_display_background=(0,0,0)
   
    self.bars_settings_saving()
  
    self.main_notebook_instance.delete("Bars configuration")
    self._init_bars_animation_window()
    self.display_bars_configuration_notebook_page()
  
  def get_users_bars_configuration(self) :
    self.confirm_asking_toplevel(msg="Save current bars configuration")
    if self.confirm_toplevel_answers :
      self.set_saved_bars_configuration()

  def get_bars_configuration(self) :
    self.bars_size=self.bars_size_control_variable.get()
    self.bars_square=self.bars_mode_control_variable.get()
 
    self.bars_color_rect_background=self.bars_users_background_color
    self.bars_color_rect_foreground=self.bars_users_foreground_color
    self.bars_rand_color=self.bars_random_colors_using
    self.bars_speed=  float(self.bars_speed_control_variable.get())
  
  
    self.bars_display_background=self.bars_users_display_background

 

  def set_saved_bars_configuration(self) :
    self.bars_size=self.bars_size_control_variable.get()
    self.bars_square=self.bars_mode_control_variable.get()
 
    self.bars_color_rect_background=self.bars_users_background_color
    self.bars_color_rect_foreground=self.bars_users_foreground_color
    self.bars_rand_color=self.bars_random_colors_using
    self.bars_speed=  float(self.bars_speed_control_variable.get())
  
  
    self.bars_display_background=self.bars_users_display_background

    self.bars_settings_saving()

  def get_saved_bars_configuration(self) :
     self.bars_settings_getting()


  def set_bars_random_color(self) :
    if not self.bars_random_colors_using :
      self.bars_random_colors_using=True
      self.bars_random_colors_button.config(text=" Random bars colors = On  ")
    else :
      self.bars_random_colors_using=False
      self.bars_random_colors_button.config(text=" Random bars colors = Off ")
    
  def get_users_bars_display_background(self) :
    color=tkColorChooser.askcolor(color=self.bars_users_display_background)
 
    if color[0] and color[1] :
      self.bars_users_display_background=color[0]
      self._generate_colors_images(self.bars_image_set_display_background_file,"/usr/share/ScreenLocker/Images/color_selection/bars_display_background.png",self.bars_users_display_background)
      self.bars_image_set_display_background_instance=ImageTk.PhotoImage(image=self.bars_image_set_display_background_file)
      self.bars_display_background_button.config(image=self.bars_image_set_display_background_instance)
  
    else :
      pass

  def get_users_bars_background_color(self) :
    color=tkColorChooser.askcolor(color=self.bars_users_background_color)
    if color[0] and color[1] :
      self.bars_users_background_color=color[0]
      self._generate_colors_images(self.bars_image_set_bars_background_file,"/usr/share/ScreenLocker/Images/color_selection/bars_background.png",self.bars_users_background_color)
      self.bars_image_set_bars_background_instance=ImageTk.PhotoImage(image=self.bars_image_set_bars_background_file)
      self.bars_background_button.config(image=self.bars_image_set_bars_background_instance)
    else :
      pass
  
  def get_users_bars_foreground_color(self) :
    color=tkColorChooser.askcolor(color=self.bars_users_foreground_color)
    if color[0] and color[1] :
      self.bars_users_foreground_color=color[0]
      self._generate_colors_images(self.bars_image_set_bars_foreground_file,"/usr/share/ScreenLocker/Images/color_selection/bars_foreground.png",self.bars_users_foreground_color)
      self.bars_image_set_bars_foreground_instance=ImageTk.PhotoImage(image=self.bars_image_set_bars_foreground_file)
      self.bars_foreground_button.config(image=self.bars_image_set_bars_foreground_instance)
    
    else :
      pass


  

  def _init_colors_animation_window(self) :
  
    self.colors_settings_getting()

    self.main_notebook_instance_page =self.main_notebook_instance.add("Colors configuration")

    self.group_colors_window_1 = Pmw.Group(self.main_notebook_instance_page,tag_text="Description")

    self.group_colors_window_2 = Pmw.Group(self.main_notebook_instance_page,tag_text="Settings")

    self.group_colors_window_3 = Pmw.Group(self.main_notebook_instance_page,tag_text="Actions")

    self.group_colors_window_1.component("tag").config(font=self.main_font_12)
    self.group_colors_window_2.component("tag").config(font=self.main_font_12)
    self.group_colors_window_3.component("tag").config(font=self.main_font_12)
  
    # Contruct colors window section 1: description and screenshot.
  
    self.colors_description_message=Message(self.group_colors_window_1.interior(),text="An colors gradient animation\navailable in an circle or square,\nFullscreen or not.\nWith random size and colors\npossiblities.",font=self.main_font_09,width=256)
    self.colors_screenshot_button=Button(self.group_colors_window_1.interior(),image=self.colors_image_screenshot_instance)
    self.colors_description_message.pack(side=LEFT,padx=15,pady=0)
    self.colors_screenshot_button.pack(side=RIGHT,padx=15,pady=5)
  
    # Contruct colors window section 2: colors animation settings.
    self.colors_size_label=Label(self.group_colors_window_2.interior(),text="Size",font=self.main_font_10)
    self.colors_size_control_variable=StringVar(value=self.colors_size) #
    self.colors_size_little_radiobutton=Radiobutton(self.group_colors_window_2.interior(),   text="Little ",variable=self.colors_size_control_variable,value="little",font=self.main_font_10)
    self.colors_size_middle_radiobutton=Radiobutton(self.group_colors_window_2.interior(),   text="Middle",variable=self.colors_size_control_variable,value="middle",font=self.main_font_10)
    self.colors_size_big_radiobutton=Radiobutton(self.group_colors_window_2.interior(),      text="Big            ",variable=self.colors_size_control_variable,value="big",font=self.main_font_10)

    self.colors_size_label.grid(row=0,column=0,columnspan=5,sticky="EW")
    self.colors_size_little_radiobutton.grid(row=0,column=5,columnspan=5,sticky="EW")
    self.colors_size_middle_radiobutton.grid(row=0,column=10,columnspan=5,sticky="EW")
    self.colors_size_big_radiobutton.grid(row=0,column=15,columnspan=5,sticky="EW")
  
  
    self.colors_mode_label=Label(self.group_colors_window_2.interior(),text="Mode",font=self.main_font_10)
    self.colors_mode_control_variable=IntVar(value=self.colors_square)
    self.colors_mode_circle_radiobutton=Radiobutton(self.group_colors_window_2.interior(),text="Circle",variable=self.colors_mode_control_variable,value=0,font=self.main_font_10)
    self.colors_mode_square_radiobutton=Radiobutton(self.group_colors_window_2.interior(),   text="Square",variable=self.colors_mode_control_variable,value=1,font=self.main_font_10)
  
    self.colors_mode_fullscreen_control_variable=BooleanVar(value=self.colors_fullscreen)
    self.colors_mode_fullscreen_checkbutton=Checkbutton(self.group_colors_window_2.interior(),   text="Fullscreen",variable=self.colors_mode_fullscreen_control_variable,font=self.main_font_10,command=self.set_fullscreen_mode)

  
    self.colors_mode_label.grid(row=1,column=0,columnspan=5,sticky="EW")
    self.colors_mode_circle_radiobutton.grid(row=1,column=5,columnspan=5,sticky="EW")
    self.colors_mode_square_radiobutton.grid(row=1,column=10,columnspan=5,sticky="EW")
    self.colors_mode_fullscreen_checkbutton.grid(row=1,column=15,columnspan=5,stick="EW")
  
    self.colors_random_size_control_variable=BooleanVar(value=self.colors_rand_size)
    self.colors_random_size_checkbutton=Checkbutton(self.group_colors_window_2.interior(),     text="Random size animation  ",font=self.main_font_10,variable=self.colors_random_size_control_variable,command=self.set_size_random)
    self.colors_random_size_checkbutton.grid(row=2,column=0,columnspan=25,padx=15,pady=3,sticky="EW")

  
    self.colors_set_colors=Label(self.group_colors_window_2.interior(),text="Colors animation:",font=self.main_font_10,justify="center")
    self.colors_set_colors.grid(row=3,column=0,sticky="EW")
  
    if self.colors_colors.__contains__("red") :
      color="red"
    else :
      color=""
    self.colors_set_red_control_var=StringVar(value=color)
    self.colors_set_red=Checkbutton(self.group_colors_window_2.interior(),    text="red    ",variable=self.colors_set_red_control_var,onvalue='red',offvalue="",font=self.main_font_10,command=self.colors_colors_check_red)
  
    if self.colors_colors.__contains__("green") :
      color="green"
    else :
      color=""
    self.colors_set_green_control_var=StringVar(value=color)
    self.colors_set_green=Checkbutton(self.group_colors_window_2.interior(),   text="green  ",variable=self.colors_set_green_control_var,onvalue="green",offvalue="",font=self.main_font_10,command=self.colors_colors_check_green)
  
    if self.colors_colors.__contains__("blue") :
      color="blue"
    else :
      color=""
    self.colors_set_blue_control_var=StringVar(value=color)
    self.colors_set_blue=Checkbutton(self.group_colors_window_2.interior(),text="blue   ",variable=self.colors_set_blue_control_var,onvalue="blue",offvalue="",font=self.main_font_10,command=self.colors_colors_check_blue)
  
    self.colors_set_red.grid(row=3,column=4)
    self.colors_set_green.grid(row=3,column=8)
    self.colors_set_blue.grid(row=3,column=12)
  
    self.colors_random_colors_control_variable=BooleanVar(value=self.colors_rand_color)
    self.colors_random_colors_checkbutton=Checkbutton(self.group_colors_window_2.interior(),   text="Random color animation",font=self.main_font_10,variable=self.colors_random_colors_control_variable,command=self.set_colors_random)
    self.colors_random_colors_checkbutton.grid(row=4,column=0,columnspan=25,padx=15,pady=3,sticky="EW")
  
    self.colors_users_display_background=self.colors_display_background
    self._generate_colors_images(self.colors_image_set_display_background_file,"/usr/share/ScreenLocker/Images/color_selection/colors_display_background.png",self.colors_users_display_background)
    self.colors_image_set_display_background_instance=ImageTk.PhotoImage(image=self.colors_image_set_display_background_file)
    self.colors_display_background_button=Button(self.group_colors_window_2.interior(),text="Window background color",compound="left",image=self.colors_image_set_display_background_instance,font=self.main_font_10,command=self.get_users_colors_display_background)
    self.colors_display_background_button.grid(row=5,column=0,padx=15,pady=3,columnspan=25)

    self.colors_speed_label=Label(self.group_colors_window_2.interior(),text="Speed animation",font=self.main_font_10)
  
    self.colors_speed_control_variable=StringVar(value=str(self.colors_speed))

    self.colors_speed_spinbox=Spinbox(self.group_colors_window_2.interior(),from_="0.001",to="0.100",increment="0.001",textvariable=self.colors_speed_control_variable,takefocus=FALSE,state="readonly",justify=CENTER,readonlybackground=self.bg_color,buttonbackground=self.bg_color)

    self.colors_speed_label.grid(row=6,column=0,padx=15,pady=3,columnspan=5)
    self.colors_speed_spinbox.grid(row=6,column=5,padx=15,pady=3,columnspan=20)

 
    # Contruct colors window section 3: colors animation settings saving | reset.
    self.colors_save_configuration_button=Button(self.group_colors_window_3.interior(), text="   Save configuration    ",font=self.main_font_10,command=self.get_users_colors_configuration)
    self.colors_reset_configuration=Button(self.group_colors_window_3.interior(),text="     Reset to default     ",font=self.main_font_10,command=self.set_default_colors_configuration)
    self.colors_save_configuration_button.grid(row=0,column=0,columnspan=10,padx=15,pady=3,sticky="EW")
    self.colors_reset_configuration.grid(row=0,column=10,columnspan=10,padx=15,pady=3,sticky="EW")
  
    self.group_colors_window_1.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)
    self.group_colors_window_2.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)
    self.group_colors_window_3.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)

  def set_default_colors_configuration(self) :
    self.colors_size="little"
    self.colors_square=0
    self.colors_fullscreen=False
    self.colors_rand_size=False
    self.colors_rand_color=False
    self.colors_colors=["red"]
    self.colors_speed= 0.05
    self.colors_display_background=(0,0,0)
  
    self.colors_settings_saving()
  
    self.main_notebook_instance.delete("Colors configuration")
    self._init_colors_animation_window()
    self.display_colors_configuration_notebook_page()

  def get_users_colors_configuration(self) :
    self.confirm_asking_toplevel(msg="Save current colors configuration")
    if self.confirm_toplevel_answers :
      self.set_saved_colors_configuration()

  def get_colors_configuration(self) :
  
    self.colors_size=self.colors_size_control_variable.get()
    self.colors_square=self.colors_mode_control_variable.get()
  
    self.colors_fullscreen=self.colors_mode_fullscreen_control_variable.get()
  
    self.colors_rand_size=self.colors_random_size_control_variable.get()
    self.colors_rand_color=self.colors_random_colors_control_variable.get()
  
    self.colors_colors=[ x.get() for x in [self.colors_set_red_control_var,self.colors_set_green_control_var,self.colors_set_blue_control_var] if x.get() ]
  
    if self.colors_rand_size :
      self.colors_speed= round(float(self.colors_speed_control_variable.get())*10,2)
    else :
      self.colors_speed= float(self.colors_speed_control_variable.get())
    
    self.colors_display_background=self.colors_users_display_background

  def set_saved_colors_configuration(self) :
  
    self.colors_size=self.colors_size_control_variable.get()
    self.colors_square=self.colors_mode_control_variable.get()
  
    self.colors_fullscreen=self.colors_mode_fullscreen_control_variable.get()
  
    self.colors_rand_size=self.colors_random_size_control_variable.get()
    self.colors_rand_color=self.colors_random_colors_control_variable.get()
  
    self.colors_colors=[ x.get() for x in [self.colors_set_red_control_var,self.colors_set_green_control_var,self.colors_set_blue_control_var] if x.get() ]
  
    if self.colors_rand_size :
      self.colors_speed= round(float(self.colors_speed_control_variable.get())*10,2)
    else :
      self.colors_speed= float(self.colors_speed_control_variable.get())
    
    self.colors_display_background=self.colors_users_display_background
  
    self.colors_settings_saving()

  def get_saved_colors_configuration(self) :
     self.colors_settings_getting()

  def set_fullscreen_mode(self) :
    if not self.colors_mode_fullscreen_control_variable.get() :
      pass
    else :
      self.colors_random_size_control_variable.set(False)

  def set_size_random(self) :
    if not self.colors_random_size_control_variable.get() :
      pass
    else :
      self.colors_mode_fullscreen_control_variable.set(False)

  def set_colors_random(self) :
    if not self.colors_random_colors_control_variable.get() :
      if not [ x.get() for x in [self.colors_set_red_control_var,self.colors_set_green_control_var,self.colors_set_blue_control_var] if x.get() ]  :
        self.colors_set_red_control_var.set('red')
    else :
      for v in [self.colors_set_red_control_var,self.colors_set_green_control_var,self.colors_set_blue_control_var] :
	v.set('')


    
  def colors_colors_check_red(self) :
    if not [x.get() for x in [self.colors_set_red_control_var,self.colors_set_green_control_var,self.colors_set_blue_control_var] if x.get() ] and not self.colors_random_colors_control_variable.get() :
      self.colors_set_red_control_var.set('red')
    elif not [x.get() for x in [self.colors_set_red_control_var,self.colors_set_green_control_var,self.colors_set_blue_control_var] if x.get() ] and self.colors_random_colors_control_variable.get() :
	self.colors_random_colors_control_variable.set(False)
    elif [x.get() for x in [self.colors_set_red_control_var,self.colors_set_green_control_var,self.colors_set_blue_control_var] if x.get() ] :
      self.colors_set_red_control_var.set('red')
      self.colors_set_green_control_var.set('')
      self.colors_set_blue_control_var.set('')
      if self.colors_random_colors_control_variable.get() :
	self.colors_random_colors_control_variable.set(False)
    
  def colors_colors_check_green(self) :
    if not [x.get() for x in [self.colors_set_red_control_var,self.colors_set_green_control_var,self.colors_set_blue_control_var] if x.get() ] and not self.colors_random_colors_control_variable :
      self.colors_set_green_control_var.set('green')
    elif not [x.get() for x in [self.colors_set_red_control_var,self.colors_set_green_control_var,self.colors_set_blue_control_var] if x.get() ] and self.colors_random_colors_control_variable :
	self.colors_random_colors_control_variable.set(False)
    elif [x.get() for x in [self.colors_set_red_control_var,self.colors_set_green_control_var,self.colors_set_blue_control_var] if x.get() ] :
      self.colors_set_red_control_var.set('')
      self.colors_set_green_control_var.set('green')
      self.colors_set_blue_control_var.set('')
      if self.colors_random_colors_control_variable.get() :
	self.colors_random_colors_control_variable.set(False)
    
    
  def colors_colors_check_blue(self) :
    if not [x.get() for x in [self.colors_set_red_control_var,self.colors_set_green_control_var,self.colors_set_blue_control_var] if x.get() ] and not self.colors_random_colors_control_variable :
      self.colors_set_blue_control_var.set('blue')
    elif not [x.get() for x in [self.colors_set_red_control_var,self.colors_set_green_control_var,self.colors_set_blue_control_var] if x.get() ] and self.colors_random_colors_control_variable :
	self.colors_random_colors_control_variable.set(False)
    elif [x.get() for x in [self.colors_set_red_control_var,self.colors_set_green_control_var,self.colors_set_blue_control_var] if x.get() ] :
      self.colors_set_red_control_var.set('')
      self.colors_set_green_control_var.set('')
      self.colors_set_blue_control_var.set('blue')
      if self.colors_random_colors_control_variable.get() :
	self.colors_random_colors_control_variable.set(False)



  def get_users_colors_display_background(self) :
    color=tkColorChooser.askcolor(color=self.colors_users_display_background)
 
    if color[0] and color[1] :
      self.colors_users_display_background=color[0]
      self._generate_colors_images(self.colors_image_set_display_background_file,"/usr/share/ScreenLocker/Images/color_selection/colors_display_background.png",self.colors_users_display_background)
      self.colors_image_set_display_background_instance=ImageTk.PhotoImage(image=self.colors_image_set_display_background_file)
      self.colors_display_background_button.config(image=self.colors_image_set_display_background_instance)
  
    else :
      pass

  def _init_balls_animation_window(self) :
  
    self.balls_settings_getting()
  
    self.main_notebook_instance_page =self.main_notebook_instance.add("Balls configuration")

    self.group_balls_window_1 = Pmw.Group(self.main_notebook_instance_page,tag_text="Description")

    self.group_balls_window_2 = Pmw.Group(self.main_notebook_instance_page,tag_text="Settings")

    self.group_balls_window_3 = Pmw.Group(self.main_notebook_instance_page,tag_text="Actions")
  
  
  
  
    self.group_balls_window_1.component("tag").config(font=self.main_font_12)
    self.group_balls_window_2.component("tag").config(font=self.main_font_12)
    self.group_balls_window_3.component("tag").config(font=self.main_font_12)
  
    # Contruct balls window section 1: description and screenshot.
  
    self.balls_description_message=Message(self.group_balls_window_1.interior(),text="Animated balls rebounding in\nseverals colors, available in 3 size.\nWith or without an halo.\nbouncing in the speed you like.",font=self.main_font_09,width=256)
    self.balls_screenshot_button=Button(self.group_balls_window_1.interior(),image=self.balls_image_screenshot_instance)
    self.balls_description_message.pack(side=LEFT,padx=15,pady=0)
    self.balls_screenshot_button.pack(side=RIGHT,padx=15,pady=5)
  
  
    # Contruct balls window section 2: balls animation settings.
  

    self.balls_size_label=Label(self.group_balls_window_2.interior(),text="Size",font=self.main_font_10)
    self.balls_size_control_variable=StringVar(value=self.balls_size)
    self.balls_size_little_radiobutton=Radiobutton(self.group_balls_window_2.interior(),   text="Little    ",variable=self.balls_size_control_variable,value="little",font=self.main_font_10)
    self.balls_size_middle_radiobutton=Radiobutton(self.group_balls_window_2.interior(),   text="Middle     ",variable=self.balls_size_control_variable,value="middle",font=self.main_font_10)
    self.balls_size_big_radiobutton=Radiobutton(self.group_balls_window_2.interior(),      text="Big       ",variable=self.balls_size_control_variable,value="big",font=self.main_font_10)
  
    self.balls_size_label.grid(row=0,column=0,columnspan=5,sticky="EW")
    self.balls_size_little_radiobutton.grid(row=0,column=5,columnspan=5,sticky="EW")
    self.balls_size_middle_radiobutton.grid(row=0,column=10,columnspan=5,sticky="EW")
    self.balls_size_big_radiobutton.grid(row=0,column=15,columnspan=5,sticky="EW")

    self.balls_mode_label=Label(self.group_balls_window_2.interior(),text="Mode",font=self.main_font_10)
    self.balls_mode_control_variable=IntVar(value=self.balls_square)
    self.balls_mode_circle_radiobutton=Radiobutton(self.group_balls_window_2.interior(),    text="Circle   ",variable=self.balls_mode_control_variable,value=0,font=self.main_font_10)
    self.balls_mode_rounded_radiobutton=Radiobutton(self.group_balls_window_2.interior(),   text="Halo        ",variable=self.balls_mode_control_variable,value=1,font=self.main_font_10)
  
    self.balls_mode_label.grid(row=1,column=0,columnspan=5,sticky="EW")
    self.balls_mode_circle_radiobutton.grid(row=1,column=5,columnspan=5,sticky="EW")
    self.balls_mode_rounded_radiobutton.grid(row=1,column=10,columnspan=5,sticky="EW")

    self.balls_set_colors_and_numbers=Button(self.group_balls_window_2.interior(),text="    Colors to set on:    ",font=self.main_font_10,justify="center")
    self.balls_set_colors_and_numbers.grid(row=2,column=3,columnspan=16,sticky="EW")
  
    if self.balls_colors.__contains__('red') :
      color='red'
    else :
      color=''
    self.balls_set_red_control_var=StringVar(value=color)
    self.balls_set_red=Checkbutton(self.group_balls_window_2.interior(),    text="red      ",variable=self.balls_set_red_control_var,onvalue="red",offvalue="",font=self.main_font_10,command=self.balls_colors_check)
  
    if self.balls_colors.__contains__('green') :
      color='green'
    else :
      color=''
    self.balls_set_green_control_var=StringVar(value=color)
    self.balls_set_green=Checkbutton(self.group_balls_window_2.interior(),   text="green  ",variable=self.balls_set_green_control_var,onvalue="green",offvalue="",font=self.main_font_10,command=self.balls_colors_check)
  
    if self.balls_colors.__contains__('blue') :
      color='blue'
    else :
      color=''
    self.balls_set_blue_control_var=StringVar(value=color)
    self.balls_set_blue=Checkbutton(self.group_balls_window_2.interior(),text="blue   " ,variable=self.balls_set_blue_control_var,onvalue="blue",offvalue="",font=self.main_font_10,command=self.balls_colors_check)
  
    if self.balls_colors.__contains__('yellow') :
      color='yellow'
    else :
      color=''
    self.balls_set_yellow_control_var=StringVar(value=color)
    self.balls_set_yellow=Checkbutton(self.group_balls_window_2.interior(),  text="yellow ",variable=self.balls_set_yellow_control_var,onvalue="yellow",offvalue="",font=self.main_font_10,command=self.balls_colors_check)
  
    if self.balls_colors.__contains__('pink') :
      color='pink'
    else :
      color=''
    self.balls_set_pink_control_var=StringVar(value=color)
    self.balls_set_pink=Checkbutton(self.group_balls_window_2.interior(),   text="pink   ",variable=self.balls_set_pink_control_var,onvalue="pink",offvalue="",font=self.main_font_10,command=self.balls_colors_check)
  
    if self.balls_colors.__contains__('turkish') :
      color='turkish'
    else :
      color=''
    self.balls_set_turkish_control_var=StringVar(value=color)
    self.balls_set_turkish=Checkbutton(self.group_balls_window_2.interior(), text="turkish",variable=self.balls_set_turkish_control_var,onvalue="turkish",offvalue="",font=self.main_font_10,command=self.balls_colors_check)
  
    self.balls_set_red.grid(row=3,column=4)
    self.balls_set_green.grid(row=3,column=8)
    self.balls_set_blue.grid(row=3,column=12)
  
    self.balls_set_yellow.grid(row=4,column=4)
    self.balls_set_pink.grid(row=4,column=8)
    self.balls_set_turkish.grid(row=4,column=12)
  
  
    self.balls_users_display_background=self.balls_display_background
    self._generate_colors_images(self.balls_image_set_display_background_file,"/usr/share/ScreenLocker/Images/color_selection/balls_display_background.png",self.balls_users_display_background)
    self.balls_image_set_display_background_instance=ImageTk.PhotoImage(image=self.balls_image_set_display_background_file)
    self.balls_display_background_button=Button(self.group_balls_window_2.interior(),text="Window background color",compound='left',image=self.balls_image_set_display_background_instance,font=self.main_font_10,command=self.get_users_balls_display_background)
    self.balls_display_background_button.grid(row=5,column=0,padx=15,pady=3,columnspan=25)

    self.balls_speed_label=Label(self.group_balls_window_2.interior(),text="Speed animation",font=self.main_font_10)
  
    self.balls_speed_control_variable = StringVar(value=str(self.balls_speed))

    self.balls_speed_spinbox=Spinbox(self.group_balls_window_2.interior(),from_="0.01",to="1.0",increment="0.01",takefocus=FALSE,state="readonly",justify=CENTER,textvariable=self.balls_speed_control_variable,readonlybackground=self.bg_color,buttonbackground=self.bg_color)

    self.balls_speed_label.grid(row=6,column=0,padx=15,pady=3,columnspan=5)
    self.balls_speed_spinbox.grid(row=6,column=5,padx=15,pady=3,columnspan=20)

 
    # Contruct balls window section 3: balls animation settings saving | reset.
    self.balls_save_configuration_button=Button(self.group_balls_window_3.interior(), text="   Save configuration    ",font=self.main_font_10,command=self.get_users_balls_configuration)
    self.balls_reset_configuration=Button(self.group_balls_window_3.interior(),text="     Reset to default     ",font=self.main_font_10,command=self.set_default_balls_configuration)
    self.balls_save_configuration_button.grid(row=0,column=0,columnspan=10,padx=15,pady=3,sticky="EW")
    self.balls_reset_configuration.grid(row=0,column=10,columnspan=10,padx=15,pady=3,sticky="EW")
  
    self.group_balls_window_1.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)
    self.group_balls_window_2.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)
    self.group_balls_window_3.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)

  def balls_colors_check(self) :
    self.colors_choosing_callback(colors=[self.balls_set_red_control_var,self.balls_set_pink_control_var,self.balls_set_turkish_control_var,self.balls_set_green_control_var,self.balls_set_blue_control_var,self.balls_set_yellow_control_var],default=self.balls_set_red_control_var,switch=False)

  def get_users_balls_configuration(self) :
    self.confirm_asking_toplevel(msg="Save current balls configuration")
    if self.confirm_toplevel_answers :
      self.set_saved_balls_configuration()

  def set_default_balls_configuration(self) :
  
    self.balls_size="middle"
    self.balls_square=0
    self.balls_colors=["red"]
    self.balls_speed=0.05
    self.balls_display_background=(0,0,0)
  
    self.balls_settings_saving()
  
    self.main_notebook_instance.delete("Balls configuration")
    self._init_balls_animation_window()
    self.display_balls_configuration_notebook_page()
  
  def get_balls_configuration(self) :
  
    self.balls_size=self.balls_size_control_variable.get()
    self.balls_square=self.balls_mode_control_variable.get()
  
    self.balls_colors=[ x.get() for x in [self.balls_set_red_control_var,self.balls_set_green_control_var,self.balls_set_blue_control_var,self.balls_set_yellow_control_var,self.balls_set_pink_control_var,self.balls_set_turkish_control_var] if x.get() ]
  
    self.balls_speed=float(self.balls_speed_control_variable.get())
    
    self.balls_display_background=self.balls_users_display_background

  def set_saved_balls_configuration(self) :
  
    self.balls_size=self.balls_size_control_variable.get()
    self.balls_square=self.balls_mode_control_variable.get()
  
    self.balls_colors=[ x.get() for x in [self.balls_set_red_control_var,self.balls_set_green_control_var,self.balls_set_blue_control_var,self.balls_set_yellow_control_var,self.balls_set_pink_control_var,self.balls_set_turkish_control_var] if x.get() ]
  
    self.balls_speed=float(self.balls_speed_control_variable.get())
    
    self.balls_display_background=self.balls_users_display_background
    self.balls_settings_saving()

  def get_saved_balls_configuration(self) :
     self.balls_settings_getting()

  def get_users_balls_display_background(self) :
    color=tkColorChooser.askcolor(color=self.balls_users_display_background)
 
    if color[0] and color[1] :
      self.balls_users_display_background=color[0]
      self._generate_colors_images(self.balls_image_set_display_background_file,"/usr/share/ScreenLocker/Images/color_selection/colors_display_background.png",self.balls_users_display_background)
      self.balls_image_set_display_background_instance=ImageTk.PhotoImage(image=self.balls_image_set_display_background_file)
      self.balls_display_background_button.config(image=self.balls_image_set_display_background_instance)
  
    else :
      pass

  def _init_about_and_gui_settings(self) :
  
    self.gui_settings_getting()
    self.update_gui_colors()
  
    self.about_and_gui_settings_notebook_instance_page =self.main_notebook_instance.add("About and GUI settings")

    self.group_about_and_gui_settings_window_1 = Pmw.Group(self.about_and_gui_settings_notebook_instance_page,tag_text="About")

    self.group_about_and_gui_settings_window_2 = Pmw.Group(self.about_and_gui_settings_notebook_instance_page,tag_text="GUI settings")
  
    self.group_about_and_gui_settings_window_3 = Pmw.Group(self.about_and_gui_settings_notebook_instance_page,tag_text="Actions")
  
    self.group_about_and_gui_settings_window_1.component("tag").config(font=self.main_font_12)
    self.group_about_and_gui_settings_window_2.component("tag").config(font=self.main_font_12)
    self.group_about_and_gui_settings_window_3.component("tag").config(font=self.main_font_12)
      
    highlight_mask_color=self.main_window_instance.cget("bg")
    self.about_and_gui_settings_image_label=Label(self.group_about_and_gui_settings_window_1.interior(),image=self.about_and_gui_settings_image_file_instance,relief="flat",activebackground=highlight_mask_color)
    self.about_and_gui_settings_about_text_message=Message(self.group_about_and_gui_settings_window_1.interior(),text="Author: Eddie Bruggemann.\nContact: mrcyberfighter@gmail.com\nCopyright: License GPLv3.\nHit Enter to leave the fullscreen mode !!!",font=self.main_font_09,width=256)
  
    self.about_and_gui_settings_image_label.pack(side=TOP,padx=15,pady=0)
    self.about_and_gui_settings_about_text_message.pack(side=BOTTOM,padx=15,pady=0)
     
    self.compute_bg_fg_colors_as_tuple()
  
    self._generate_colors_images(self.about_and_gui_settings_background_file,"/usr/share/ScreenLocker/Images/color_selection/gui_background.png",self.about_and_gui_users_gui_background)
    self.about_and_gui_settings_background_instance=ImageTk.PhotoImage(image=self.about_and_gui_settings_background_file)
     
    self.about_and_gui_settings_background_button=Button(self.group_about_and_gui_settings_window_2.interior(),text=" Background GUI   ",font=self.main_font_10,compound="left",image=self.about_and_gui_settings_background_instance,command=self.get_users_gui_background)
  
    self._generate_colors_images(self.about_and_gui_settings_foreground_file,"/usr/share/ScreenLocker/Images/color_selection/gui_foreground.png",self.about_and_gui_users_gui_foreground)
    self.about_and_gui_settings_foreground_instance=ImageTk.PhotoImage(image=self.about_and_gui_settings_foreground_file)

    self.about_and_gui_settings_foreground_button=Button(self.group_about_and_gui_settings_window_2.interior(),text=" Foreground GUI   ",font=self.main_font_10,compound="left",image=self.about_and_gui_settings_foreground_instance,command=self.get_users_gui_foreground)

    self.about_and_gui_settings_background_button.grid(row=2,column=0,columnspan=10,padx=15,pady=3,sticky="EW")
    self.about_and_gui_settings_foreground_button.grid(row=2,column=10,columnspan=10,padx=15,pady=3,sticky="EW")
  
    self.about_and_gui_settings_save_configuration_button=Button(self.group_about_and_gui_settings_window_3.interior(), text="   Save configuration    ",font=self.main_font_10,command=self.get_users_gui_settings_configuration)
    self.about_and_gui_settings_reset_configuration=Button(self.group_about_and_gui_settings_window_3.interior(),text="     Reset to default     ",font=self.main_font_10,command=self.set_default_gui_settings_configuration)
    self.about_and_gui_settings_save_configuration_button.grid(row=0,column=0,columnspan=10,padx=15,pady=3,sticky="EW")
    self.about_and_gui_settings_reset_configuration.grid(row=0,column=10,columnspan=10,padx=15,pady=3,sticky="EW")
  
    self.group_about_and_gui_settings_window_1.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)
    self.group_about_and_gui_settings_window_2.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)
    self.group_about_and_gui_settings_window_3.pack(ipadx=5,ipady=5,padx=15,pady=15,fill=X)

  def compute_bg_fg_colors_as_tuple(self) :
    self.about_and_gui_users_gui_background=(int(str(self.bg_color[1:3]),16),int(str(self.bg_color[3:5]),16),int(str(self.bg_color[5::]),16))
    self.about_and_gui_users_gui_foreground=(int(str(self.fg_color[1:3]),16),int(str(self.fg_color[3:5]),16),int(str(self.fg_color[5::]),16))
  
  def update_gui_colors(self) :
    self.main_window_instance.tk_setPalette(background=self.bg_color,foreground=self.fg_color)
  

  def set_default_gui_settings_configuration(self) :
    self.bg_color="#00c0c0"
    self.fg_color="#000000"
  
    self.music_filename_entry.config(readonlybackground=self.bg_color)
  
    self.rollers_speed_spinbox.config(readonlybackground=self.bg_color,buttonbackground=self.bg_color)
    self.bars_speed_spinbox.config(readonlybackground=self.bg_color,buttonbackground=self.bg_color)
    self.colors_speed_spinbox.config(readonlybackground=self.bg_color,buttonbackground=self.bg_color)
    self.balls_speed_spinbox.config(readonlybackground=self.bg_color,buttonbackground=self.bg_color)
  
    self._generate_colors_images(self.about_and_gui_settings_background_file,"/usr/share/ScreenLocker/Images/color_selection/gui_background.png",(0,192,192))
    self.about_and_gui_settings_background_instance=ImageTk.PhotoImage(image=self.about_and_gui_settings_background_file)
  
    self._generate_colors_images(self.about_and_gui_settings_foreground_file,"/usr/share/ScreenLocker/Images/color_selection/gui_foreground.png",(0,0,0))
    self.about_and_gui_settings_foreground_instance=ImageTk.PhotoImage(image=self.about_and_gui_settings_foreground_file)
    self.gui_settings_saving()
  
    self.main_notebook_instance.delete("About and GUI settings")
    self._init_about_and_gui_settings()
    self.display_about_configuration_notebook_page()
  
  def get_users_gui_settings_configuration(self) :
    self.confirm_asking_toplevel(msg="Save current GUI configuration")
    if self.confirm_toplevel_answers :
      self.set_saved_gui_settings_configuration()

  def set_saved_gui_settings_configuration(self) :
    self.gui_settings_saving()

  def get_saved_gui_settings_configuration(self) :
     self.gui_settings_getting()


  def get_users_gui_background(self) :
    color=tkColorChooser.askcolor(color=self.bg_color)
 
    if color[0] and color[1] :
      self.about_and_gui_users_gui_background=color[0]
      self.bg_color=color[1]
      self._generate_colors_images(self.about_and_gui_settings_background_file,"/usr/share/ScreenLocker/Images/color_selection/gui_background.png",self.about_and_gui_users_gui_background)
      self.about_and_gui_settings_background_instance=ImageTk.PhotoImage(image=self.about_and_gui_settings_background_file)
      self.about_and_gui_settings_background_button.config(image=self.about_and_gui_settings_background_instance)
    
      self.rollers_speed_spinbox.config(readonlybackground=self.bg_color,buttonbackground=self.bg_color)
      self.bars_speed_spinbox.config(readonlybackground=self.bg_color,buttonbackground=self.bg_color)
      self.colors_speed_spinbox.config(readonlybackground=self.bg_color,buttonbackground=self.bg_color)
      self.balls_speed_spinbox.config(readonlybackground=self.bg_color,buttonbackground=self.bg_color)
    
      self.update_gui_colors()
    else :
      pass

  def get_users_gui_foreground(self) :
    color=tkColorChooser.askcolor(color=self.fg_color)
 
    if color[0] and color[1] :
      self.about_and_gui_users_gui_foreground=color[0]
      self.fg_color=color[1]
    
      self._generate_colors_images(self.about_and_gui_settings_foreground_file,"/usr/share/ScreenLocker/Images/color_selection/gui_foreground.png",self.about_and_gui_users_gui_foreground)
      self.about_and_gui_settings_foreground_instance=ImageTk.PhotoImage(image=self.about_and_gui_settings_foreground_file)
      self.about_and_gui_settings_foreground_button.config(image=self.about_and_gui_settings_foreground_instance)
      self.update_gui_colors()
    else :
      pass



  def confirm_asking_toplevel(self,title="Confirm ?",msg=False) :
    self.confirm_toplevel=Toplevel(self.main_window_instance)
    self.confirm_toplevel.title(title)
    self.confirm_toplevel.resizable(False,False)
    self.confirm_toplevel_answers=False
    self.confirm_toplevel_label=Label(self.confirm_toplevel,text=msg)
    self.confirm_toplevel_button_cancel=Button(self.confirm_toplevel,text=" Cancel ",command=self.confirm_toplevel.destroy)
    self.confirm_toplevel_button_ok=Button(self.confirm_toplevel,text=" Confirm ",command=self.confirm_toplevel_callback)
    self.confirm_toplevel_label.grid(row=1,column=5,columnspan=25,padx=15,pady=15)
    self.confirm_toplevel_button_cancel.grid(row=2,column=5,columnspan=10,padx=15,pady=15)
    self.confirm_toplevel_button_ok.grid(row=2,column=20,columnspan=10,padx=15,pady=15)
    self.confirm_toplevel.mainloop()

  def confirm_toplevel_callback(self) :
    self.confirm_toplevel.destroy()
    self.confirm_toplevel_answers=True
  
  def password_inform_error_toplevel(self,title=False,msg=False,button_label=False) :
    self.password_inform_toplevel=Toplevel(self.main_window_instance)
    self.password_inform_toplevel.title(title)
    self.password_inform_toplevel.resizable(False,False)
    self.password_inform_toplevel_label=Label(self.password_inform_toplevel,text=msg)
    self.password_inform_toplevel_ok=Button(self.password_inform_toplevel,text=button_label,command=self.password_inform_toplevel.destroy)
    self.password_inform_toplevel_label.grid(row=1,column=5,columnspan=25,padx=15,pady=15)
    self.password_inform_toplevel_ok.grid(row=2,column=5,columnspan=25,padx=15,pady=15)
    self.password_inform_toplevel.mainloop()
  
  def _init_images(self) :
    self.launch_image_file=Image.open("/usr/share/ScreenLocker/Images/launching/Launch_button_image.png")
    self.launch_image_instance=ImageTk.PhotoImage(image=self.launch_image_file)
  
    self.rollers_image_set_display_background_file=Image.open("/usr/share/ScreenLocker/Images/color_selection/rollers_display_background.png")
    self.rollers_image_set_display_background_instance=ImageTk.PhotoImage(image=self.rollers_image_set_display_background_file)
  
    self.rollers_image_screenshot_file=Image.open("/usr/share/ScreenLocker/Images/screenshots/rollers_screenshot.png")
    self.rollers_image_screenshot_instance=ImageTk.PhotoImage(image=self.rollers_image_screenshot_file)
  
    self.bars_image_set_bars_background_file=Image.open("/usr/share/ScreenLocker/Images/color_selection/bars_background.png")
    self.bars_image_set_bars_background_instance=ImageTk.PhotoImage(image=self.bars_image_set_bars_background_file)
  
    self.bars_image_set_bars_foreground_file=Image.open("/usr/share/ScreenLocker/Images/color_selection/bars_foreground.png")
    self.bars_image_set_bars_foreground_instance=ImageTk.PhotoImage(image=self.bars_image_set_bars_foreground_file)

    self.bars_image_set_display_background_file=Image.open("/usr/share/ScreenLocker/Images/color_selection/bars_display_background.png")
    self.bars_image_set_display_background_instance=ImageTk.PhotoImage(image=self.bars_image_set_display_background_file)
  
    self.bars_image_screenshot_file=Image.open("/usr/share/ScreenLocker/Images/screenshots/bars_screenshot.png")
    self.bars_image_screenshot_instance=ImageTk.PhotoImage(image=self.bars_image_screenshot_file)
  
    self.colors_image_set_display_background_file=Image.open("/usr/share/ScreenLocker/Images/color_selection/colors_display_background.png")
    self.colors_image_set_display_background_instance=ImageTk.PhotoImage(image=self.colors_image_set_display_background_file)
  
    self.colors_image_screenshot_file=Image.open("/usr/share/ScreenLocker/Images/screenshots/colors_screenshot.png")
    self.colors_image_screenshot_instance=ImageTk.PhotoImage(image=self.colors_image_screenshot_file)
  
    self.balls_image_set_display_background_file=Image.open("/usr/share/ScreenLocker/Images/color_selection/balls_display_background.png")
    self.balls_image_set_display_background_instance=ImageTk.PhotoImage(image=self.balls_image_set_display_background_file)
  
    self.balls_image_screenshot_file=Image.open("/usr/share/ScreenLocker/Images/screenshots/balls_screenshot.png")
    self.balls_image_screenshot_instance=ImageTk.PhotoImage(image=self.balls_image_screenshot_file)
  
    self.about_and_gui_settings_image_file=Image.open("/usr/share/ScreenLocker/Images/about/screen_icon.png")
    self.about_and_gui_settings_image_file_instance=ImageTk.PhotoImage(image=self.about_and_gui_settings_image_file)
  
    self.about_and_gui_settings_background_file=Image.open("/usr/share/ScreenLocker/Images/color_selection/gui_background.png")
    self.about_and_gui_settings_background_instance=ImageTk.PhotoImage(image=self.about_and_gui_settings_background_file)
  
    self.about_and_gui_settings_foreground_file=Image.open("/usr/share/ScreenLocker/Images/color_selection/gui_foreground.png")
    self.about_and_gui_settings_foreground_instance=ImageTk.PhotoImage(image=self.about_and_gui_settings_foreground_file)
  
  def _generate_colors_images(self,instance=False,filename=False,color=False) :
    i=0
    while i < 16 :
      ii=0
      while ii < 16 :
	instance.putpixel((i,ii),color)
	ii += 1
      i += 1

    instance.save(filename)



  def colors_choosing_callback(self,colors=False,default=False,switch=False) :
    if not [ x.get() for x in colors if x.get() ] and not switch :
      default.set("red")
    elif switch :
      if switch.get() :
	switch.set(False)
      if not [ x.get() for x in colors if x.get() ] :
	default.set("red")

  def change_page(self) :
    self.main_notebook_instance.selectpage(self.main_notebook_page_reference)
  
  def display_main_configuration_notebook_page(self) :
    self.main_notebook_page_reference="Main configuration"
    self.main_window_instance.title("ScreenLocker: Main configuration")
    self.change_page()

  def display_rollers_configuration_notebook_page(self) :
    self.main_notebook_page_reference="Rollers configuration"
    self.main_window_instance.title("ScreenLocker: Rollers configuration")
    self.change_page()
  
  def display_bars_configuration_notebook_page(self) :
    self.main_notebook_page_reference="Bars configuration"
    self.main_window_instance.title("ScreenLocker: Bars configuration")
    self.change_page()

  def display_colors_configuration_notebook_page(self) :
    self.main_notebook_page_reference="Colors configuration"
    self.main_window_instance.title("ScreenLocker: Colors configuration")
    self.change_page()  

  def display_balls_configuration_notebook_page(self) :
    self.main_notebook_page_reference="Balls configuration"
    self.main_window_instance.title("ScreenLocker: Balls configuration")
    self.change_page()  

  def display_about_configuration_notebook_page(self) :
    self.main_notebook_page_reference="About and GUI settings"
    self.main_window_instance.title("ScreenLocker: About and GUI settings")
    self.change_page() 

  def rollers_settings_saving(self) :
    rollers_settings_saving_dict=shelve.open(self.rollers_settings_saving_filepath, flag='c')
  
    rollers_settings_saving_dict["size"]=self.rollers_size
    rollers_settings_saving_dict["colors"]=self.rollers_colors
    rollers_settings_saving_dict["direction"]=self.rollers_direction
    rollers_settings_saving_dict["speed"]=self.rollers_speed
    rollers_settings_saving_dict["display_bg"]=self.rollers_display_background
  
    rollers_settings_saving_dict.close()
  
  def rollers_settings_getting(self) :
    rollers_settings_saving_dict=shelve.open(self.rollers_settings_saving_filepath, flag='r')
  
    self.rollers_size=rollers_settings_saving_dict.get('size')
    self.rollers_colors=rollers_settings_saving_dict.get('colors')
    self.rollers_direction=rollers_settings_saving_dict.get('direction')
    self.rollers_speed=rollers_settings_saving_dict.get('speed')
    self.rollers_display_background=rollers_settings_saving_dict.get('display_bg')
  
    rollers_settings_saving_dict.close()
  
  def bars_settings_saving(self) :
    bars_settings_saving_dict=shelve.open(self.bars_settings_saving_filepath, flag='c')
  
    bars_settings_saving_dict["size"]=self.bars_size
    bars_settings_saving_dict["square"]=self.bars_square
    bars_settings_saving_dict["rand_color"]=self.bars_rand_color
    bars_settings_saving_dict["bars_bg_color"]=self.bars_color_rect_background
    bars_settings_saving_dict["bars_fg_color"]=self.bars_color_rect_foreground
    bars_settings_saving_dict["speed"]=self.bars_speed
    bars_settings_saving_dict["display_bg"]=self.bars_display_background
  
    bars_settings_saving_dict.close()
  
  def bars_settings_getting(self) :
    bars_settings_saving_dict=shelve.open(self.bars_settings_saving_filepath, flag='r')
  
    self.bars_size=bars_settings_saving_dict.get('size')
    self.bars_square=bars_settings_saving_dict.get('square')
    self.bars_rand_color=bars_settings_saving_dict.get('rand_color')
    self.bars_color_rect_background=bars_settings_saving_dict.get('bars_bg_color')
    self.bars_color_rect_foreground=bars_settings_saving_dict.get('bars_fg_color')
    self.bars_speed=bars_settings_saving_dict.get('speed')
    self.bars_display_background=bars_settings_saving_dict.get('display_bg')
    bars_settings_saving_dict.close()
  
  def colors_settings_saving(self) :
    colors_settings_saving_dict=shelve.open(self.colors_settings_saving_filepath, flag='c')
  
    colors_settings_saving_dict["size"]=self.colors_size
    colors_settings_saving_dict["square"]=self.colors_square
    colors_settings_saving_dict["fullscreen"]=self.colors_fullscreen
    colors_settings_saving_dict["rand_size"]=self.colors_rand_size
    colors_settings_saving_dict["colors"]=self.colors_colors
    colors_settings_saving_dict["rand_colors"]=self.colors_rand_color
    colors_settings_saving_dict["speed"]=self.colors_speed
    colors_settings_saving_dict["display_bg"]=self.colors_display_background
  
    colors_settings_saving_dict.close()
  
  def colors_settings_getting(self) :
    colors_settings_saving_dict=shelve.open(self.colors_settings_saving_filepath, flag='r')
  
    self.colors_size=colors_settings_saving_dict.get('size')
  
    self.colors_square=colors_settings_saving_dict.get('square')
    self.colors_fullscreen=colors_settings_saving_dict.get("fullscreen")
    self.colors_rand_size=colors_settings_saving_dict.get('rand_size')
    self.colors_colors=colors_settings_saving_dict.get('colors')
    self.colors_rand_color=colors_settings_saving_dict.get('rand_colors')
    self.colors_speed=colors_settings_saving_dict.get('speed')
    if self.colors_rand_size :
    
      self.colors_speed=self.colors_speed/10.0
    self.colors_display_background=colors_settings_saving_dict.get('display_bg')
    colors_settings_saving_dict.close()
  
  def balls_settings_saving(self) :
    balls_settings_saving_dict=shelve.open(self.balls_settings_saving_filepath, flag='c')
  
    balls_settings_saving_dict["size"]=self.balls_size
    balls_settings_saving_dict["square"]=self.balls_square
    balls_settings_saving_dict["colors"]=self.balls_colors
    balls_settings_saving_dict["speed"]=self.balls_speed
    balls_settings_saving_dict["display_bg"]=self.balls_display_background
  
    balls_settings_saving_dict.close()
  
  def balls_settings_getting(self) :
    balls_settings_saving_dict=shelve.open(self.balls_settings_saving_filepath, flag='r')
  
    self.balls_size=balls_settings_saving_dict.get('size')
    self.balls_square=balls_settings_saving_dict.get('square')
    self.balls_colors=balls_settings_saving_dict.get('colors')
    self.balls_speed=balls_settings_saving_dict.get('speed')
    self.balls_display_background=balls_settings_saving_dict.get('display_bg')
  
    balls_settings_saving_dict.close()  
  
  def gui_settings_saving(self) :
    gui_settings_saving_dict=shelve.open(self.gui_settings_saving_filepath, flag='n')
    gui_settings_saving_dict["bg_color"]=self.bg_color
    gui_settings_saving_dict["fg_color"]=self.fg_color
    gui_settings_saving_dict.close()
  
  def gui_settings_getting(self) :
    gui_settings_saving_dict=shelve.open(self.gui_settings_saving_filepath, flag='r')
    self.bg_color=gui_settings_saving_dict.get("bg_color")
    self.fg_color=gui_settings_saving_dict.get("fg_color")
    gui_settings_saving_dict.close()
  
  def password_settings_saving(self) :
    password_settings_saving_dict=shelve.open(self.password_settings_saving_filepath, flag='n')
  
    password_settings_saving_dict["passwd_hash"]=self.password_set_hash
    password_settings_saving_dict["passwd_recursion"]=self.password_set_recursion
    password_settings_saving_dict["passwd_use"]=self.password_use
    password_settings_saving_dict.close()
  
  def password_settings_getting(self) :
    password_settings_saving_dict=shelve.open(self.password_settings_saving_filepath, flag='r')
    self.password_set_hash=password_settings_saving_dict.get("passwd_hash")
    self.password_set_recursion=password_settings_saving_dict.get("passwd_recursion")
    self.password_use=password_settings_saving_dict.get("passwd_use")
    password_settings_saving_dict.close()
  
  def music_settings_saving(self) :
    music_settings_saving_dict=shelve.open(self.music_settings_saving_filepath, flag='n')
  
    music_settings_saving_dict["music_filepath"]=self.music_filepath
    music_settings_saving_dict["music_on"]=self.music_set_on
  
    music_settings_saving_dict.close()
  
  def music_settings_getting(self) :
    music_settings_saving_dict=shelve.open(self.music_settings_saving_filepath, flag='r')
    self.music_filepath=music_settings_saving_dict.get("music_filepath")
    self.music_set_on=music_settings_saving_dict.get("music_on")
    music_settings_saving_dict.close()    
  
passwd=Password()
gui=GUI("#00c0c0","#000000")  


  
  