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


# Uncomment following import lines for single use of tkFileSelector.
#from Tkinter import Tk,Toplevel,Frame,Entry,Button,Canvas,Scrollbar,Menubutton,Menu,Label, StringVar, HORIZONTAL,BOTH,END
#from PIL import Image,ImageTk

#from os.path import expanduser,isdir,isfile,basename 
#from os import listdir


class File_selector() :
  def __init__(self,master,start_dir=expanduser("~"),filetypes=["*.mp3","*.wav"],title="Select a music file.",color_1="#000000",color_2="#00c0c0",highlight_color_items="#c9c9c9") :
    '''
    master == root_window == Tk()
    
    use color_1 and color_2 and bg_items and fg_items and highlight_color_items for colors personalisation.
    
    filetypes must "Strictly" be a list of extension beginning with an asterix followed by a point and the extension (in lowercase) or an empty list for no filtering.
    filetypes=["*.mp3","*.wav"] per example. Or insert an, item '*' for all filetype in combination with defined filetypes.
    
    for borderwidth and relief settings look at the code
    '''
    
    # Constrcut GUI for the file selection toplevel.
    
    self.toplevel=Toplevel(master,bg=color_1,borderwidth=1,relief="sunken")
    self.toplevel.resizable(width=False, height=False)
    self.toplevel.title(title)
    
    self.dir_selection_frame=Frame(self.toplevel,bg=color_1,borderwidth=8/2,relief="groove")                                         # Frame container for directory fields.
    self.dir_name_entry=Entry(self.toplevel,justify="center",width=50,bg=color_2,fg=color_1)                                         # This will contains the current directory relative dirname
    self.dir_name_separator=Button(self.toplevel,width=1,relief="sunken",bg=color_1,fg=color_2)                                      # An separator
    self.dir_back_button=Button(self.toplevel,width=6,relief="raised",bg=color_2,fg=color_1,text="Back",command=self.folder_go_back) # Change directory back button.
    
    
    self.canvas_frame=Frame(self.toplevel,borderwidth=8,relief="groove")     # Frame for the file selection window canvas and his scrollbar.
    self.canvas=Canvas(self.canvas_frame,height=20*9,width=18*28,bg=color_2) # File selection window.
    self.canvas_scrollbar=Scrollbar(self.canvas_frame,orient=HORIZONTAL, bg=color_2,troughcolor=color_1,command=self.canvas.xview) # File selection window scrollbar.
    self.canvas.configure(xscrollcommand=self.canvas_scrollbar.set)
    
    
    self.file_selection_frame=Frame(self.toplevel,bg=color_1,borderwidth=8/2,relief="groove")                                        # Frame container for filename fields.
    self.file_name_entry=Entry(self.toplevel,justify="center",width=50,bg=color_2,fg=color_1)                                        # This will contains the basename (relative) of the selected file.
    self.file_name_separator=Button(self.toplevel,width=1,relief="sunken",bg=color_1,fg=color_2)                                     # An separator.
    self.file_filter_menubutton = Menubutton(self.file_selection_frame, text='',relief="groove",width=8,bg=color_2,fg=color_1)       # Menubutton for filetype filter.
    
    self.file_filter_extension=""
    
    if filetypes :
      self.file_filter_menu= Menu(self.file_filter_menubutton,borderwidth=3,relief="groove") # We use a menu for the filetypes filtering.
      i=0
      self.file_filter_var=StringVar(master=None, value=filetypes[i], name=None)             # Control varaible for current filetype and initialize with the first filetype item.
      self.file_filter_menubutton.config(text=filetypes[i])                                  
      self.file_filter_extension=filetypes[i][1::]
      while i < len(filetypes) :
	# Creating radiobutton to change the filetype filter.
	self.file_filter_menu.add_radiobutton(label=filetypes[i], variable=self.file_filter_var,value=filetypes[i],background=color_2,command=self.set_filetype_filter )
        i += 1
      
      self.file_filter_menubutton.configure(menu= self.file_filter_menu)
    
    
    self.buttons_frame=Frame(self.toplevel,bg=color_2,borderwidth=8,relief="groove",height=50,width=18*3) # Frame container for the buttons.
    self.button_cancel=Button(self.buttons_frame,bg=color_2,fg=color_1,text="Quit",borderwidth=8/2,relief="groove",width=8,command=self.item_selection_quit)
    self.button_home=Button(self.buttons_frame,bg=color_2,fg=color_1,text="Home",borderwidth=8/2,relief="groove",width=8,command=self.item_selection_home)
    self.button_ok=Button(self.buttons_frame,bg=color_2,fg=color_1,text=" OK ",borderwidth=8/2,relief="groove",width=8,command=self.item_selection_ok)
    
     
    self.start_dir=start_dir        # Start folder.
    self.curdir=start_dir           # Current folder.
    
    self.last_dir=[]                # Container for the precedent folders we visit.
    self.last_dir.append(start_dir) # Append start folder.
    
    self.select_filepath=""         # Value to return by file selection.
    
    self.dir_name_entry.insert(0,"../"+basename(self.curdir))
    
    
    if not color_2 :
      self.items_bg="#D9D9D9"
    else :
      self.items_bg=color_2
    
    self.items_fg=color_1
    self.highlight_color_items=highlight_color_items
    
    
    self.init_icons()
    self.ls_dir()
    self.update_canvas()
    
    
    self.dir_selection_frame.grid(row=0,column=0,sticky="WE")
    self.dir_name_entry.grid(row=0,column=0,in_=self.dir_selection_frame,sticky="NSEW")
    self.dir_name_separator.grid(row=0,column=1,in_=self.dir_selection_frame,sticky="EW")
    self.dir_back_button.grid(row=0,column=2,in_=self.dir_selection_frame,sticky="EW")
    
    self.canvas_frame.grid(row=1,column=0,sticky="WE")
    self.canvas.grid(row=0,column=0,in_=self.canvas_frame)
    self.canvas_scrollbar.grid(row=1,column=0,in_=self.canvas_frame,sticky="WE")
    
    self.file_selection_frame.grid(row=2,column=0,sticky="WE")
    self.file_name_entry.grid(row=0,column=0,in_=self.file_selection_frame,sticky="NSEW")
    self.file_name_separator.grid(row=0,column=1,in_=self.file_selection_frame,sticky="EW")
    self.file_filter_menubutton.grid(row=0,column=2,in_=self.file_selection_frame,sticky="NS")
    
    self.buttons_frame.grid(row=3,column=0,sticky="NSEW")
    self.button_cancel.grid(row=0,column=2,padx=32+3,pady=4,in_=self.buttons_frame)
    self.button_home.grid(row=0,column=4,padx=32+3,pady=4,in_=self.buttons_frame)
    self.button_ok.grid(row=0,column=6,padx=34+3,pady=4,in_=self.buttons_frame)
    
    self.toplevel.mainloop()
    
    
    
  def init_icons(self) :
    # Folder and file icons, design by me.
    self.image_folder=Image.open(expanduser("~")+"/Bureau/ScreenLocker/Images/file_selector/file_selector/folder_icon.png")
    self.imagetk_folder=ImageTk.PhotoImage(image=self.image_folder)
    
    self.image_file=Image.open(expanduser("~")+"/Bureau/ScreenLocker/Images/file_selector/file_selector/file_icon.png")
    self.imagetk_file=ImageTk.PhotoImage(image=self.image_file)
    
  def ls_dir(self) : 
    ''' List an directory and split the result in folders and files containers.
        Finally sort the 2 containers.'''
    
    folder_content=listdir(self.curdir)
    self.cur_folder_entries=len(folder_content)
    
    self.cur_folder_list=[]
    self.cur_files_list=[]
    
    folder_content.sort()
    
    for v in folder_content :
      if isdir(self.curdir+"/"+v) :
	self.cur_folder_list.append(unicode(v,encoding='utf-8'))
      elif isfile(self.curdir+"/"+v) :
        self.cur_files_list.append(unicode(v,encoding='utf-8'))
    
    self.cur_folder_list.sort()
    self.cur_files_list.sort()  
      
  def update_canvas(self) :
    ''' Generating the content from the File selection window (an canvas)'''
    self.clear_canvas()
    
    i=0             # global folder and file iterator.
    pos_x=0         # Coordinates for the rows.
    pos_y=0         # Coordinates in the columns.
    max_len=0       # Column max folder|filename length.
    max_len_save=0  # Saved value for filling empty canvas scrollregion.
    
    while i < len(self.cur_folder_list) :
      # Generating the folder items of the current folder
      
      exec(u"folder_icon_{0}=Label(self.canvas,text='{1}',image=self.imagetk_folder,relief='flat',width=17,height=17,bg=self.items_bg)".format(str(i),self.cur_folder_list[i].replace("'","\\'")))
      exec(u"folder_name_{0}=Label(self.canvas,text='{1}',relief='flat',width={2},font='Monospace 9 bold',justify='left',bg=self.items_bg,fg=self.items_fg)".format(str(i),self.cur_folder_list[i].replace("'","\\'"),int(len(" "+self.cur_folder_list[i]))))
      
      if int(len(" "+self.cur_folder_list[i])) > max_len :
	# Update longest folder name in this column.
	max_len=int(len(" "+self.cur_folder_list[i])) # Storing the value for max length of the longest folder name in this column.
	max_len_save=max_len # Value to save for filling if the generating content take minus place as the canvas scrollregion.
	
      exec("folder_icon_{0}.bind('<Double-1>',self.select_folder)".format(str(i)))
      exec("folder_name_{0}.bind('<Double-1>',self.select_folder)".format(str(i)))	
      
     
      exec("folder_name_{0}.bind('<Enter>',self.highlight_item_enter)".format(str(i)))	
      exec("folder_name_{0}.bind('<Leave>',self.highlight_item_leave)".format(str(i)))
      
      exec("folder_icon_{0}.pack(side='left',fill=BOTH)".format(str(i)))
      exec("folder_name_{0}.pack(side='right',fill=BOTH)".format(str(i)))
      
      exec("self.canvas.create_window(({1},{2}),anchor='nw',window=folder_icon_{0})".format(str(i),pos_x,pos_y))
      exec("self.canvas.create_window(({1}+17+1,{2}),anchor='nw',window=folder_name_{0})".format(str(i),pos_x,pos_y))
      
      pos_y += 20  # column increment 17 height of an items + 3 pixels padding.
      
      
      if ( i % 9 == 0) and not  i == 0 :
	# An column can contains 9 items and we change column.
	pos_y=0                   # Column position updating.
	pos_x += 17 + (max_len*9) # Update the x coordinates according the maximal length of foldername in this column ( (9 pixels == font size) (17 pixels for the folder item icon) ) . 
	
	max_len=0
	
      i += 1 # Go to the next item.
      
    ii=0            # Files iterator.
    
    while ii < len(self.cur_files_list) :
      # Generating the files items of the current folder.
      if (self.file_filter_extension and self.cur_files_list[ii].lower().endswith(self.file_filter_extension)) or not self.file_filter_extension :
        # applying filter of no filetype filering.
        
	exec(u"file_icon_{0}=Label(self.canvas,text='{1}',image=self.imagetk_file,relief='flat',width=17,height=17,bg=self.items_bg)".format(str(i),self.cur_files_list[ii].replace("'","\\'")))
	exec(u"file_name_{0}=Label(self.canvas,text='{1}',relief='flat',width={2},font='Monospace 9 normal',justify='left',bg=self.items_bg,fg=self.items_fg)".format(str(i),self.cur_files_list[ii].replace("'","\\'"),int(len(" "+self.cur_files_list[ii]))))
	
	if int(len(" "+self.cur_files_list[ii])) > max_len :
	  # Update longest filename in this column.
	  max_len=int(len(" "+self.cur_files_list[ii])) # Storing the value for max length of the longest filename in this column.
	  max_len_save=max_len                          # Value to save for filling if the generating content take minus place as the canvas scrollregion.
	  
	exec("file_icon_{0}.bind('<Double-1>',self.select_file)".format(str(i)))
	exec("file_name_{0}.bind('<Double-1>',self.select_file)".format(str(i)))	
	  
	exec("file_name_{0}.bind('<Enter>',self.highlight_item_enter)".format(str(i)))	
	exec("file_name_{0}.bind('<Leave>',self.highlight_item_leave)".format(str(i)))	
	
	exec("file_icon_{0}.pack(side='left',fill=BOTH)".format(str(i)))
	exec("file_name_{0}.pack(side='right',fill=BOTH)".format(str(i)))
	
	exec("self.canvas.create_window(({1},{2}),anchor='nw',window=file_icon_{0})".format(str(i),pos_x,pos_y))
	exec("self.canvas.create_window(({1}+17+1,{2}),anchor='nw',window=file_name_{0})".format(str(i),pos_x,pos_y))
	
	pos_y += 20 # column increment 17 height of an items + 3 pixels padding.
    
	if ( i % 9 == 0) and not  i == 0 :
	  # An column can contains 9 items and we change column.
	  # Note: we check the common file & folder iterator.
	  pos_y=0                   # Column position updating. 
	  pos_x += 17 + (max_len*9) # Update the x coordinates according the maximal length of filename in this column ( (9 pixels == font size) (17 pixels for the file item icon) ). 
	  max_len=0
	i += 1
      ii += 1
    
    if not pos_x+(max_len_save*9)+17 < 18*28 :
      # items collection greater than the canvas scrollregion.
      self.canvas.config(scrollregion=(0,0,pos_x+(max_len_save*9)+17,0))
    else :
      # items collection littler than the canvas scrollregion.
      self.canvas.config(scrollregion=(0,0,18*28,0))
  
  def clear_canvas(self) :
    for child in self.canvas.children.values() :
      child.destroy()
    
    
  def highlight_item_enter(self,event) :
    event.widget.config(bg=self.highlight_color_items)
  
  def highlight_item_leave(self,event) :
    event.widget.config(bg=self.items_bg)
  
  def select_folder(self,event) :
    
    if isdir(self.curdir+"/"+event.widget.cget("text").lstrip()) : # event.widget.cget("text") return the selected folder. sea the update_canvas() method. 
      self.select_filepath=""
      self.file_name_entry.delete(0,END)
      
      if self.curdir.startswith('//') :
	# Bug fix.
	self.curdir=self.curdir[1::]
        self.last_dir.append(self.curdir)
      else :
        self.last_dir.append(self.curdir)
        
      for v in self.last_dir :
	if self.last_dir.count(v) > 1 :
	  self.last_dir.remove(v)
      
      try :
	# in case of access right this will fail immediatelly
	listdir(self.curdir+"/"+event.widget.cget("text"))
        self.curdir=self.curdir+"/"+event.widget.cget("text")
      
	self.dir_name_entry.delete(0,END)
	self.dir_name_entry.insert(0,"../"+event.widget.cget("text"))
      
        self.ls_dir()
        self.update_canvas()
      except :
	pass
      
      print self.last_dir
      
  def select_file(self,event) :
    if isfile(self.curdir+"/"+event.widget.cget("text")) :
      # Set the value to return and fill the file selection field.
      self.select_filepath=self.curdir+"/"+event.widget.cget("text") 
      self.file_name_entry.delete(0,END)
      self.file_name_entry.insert(0,event.widget.cget("text"))
      
  def folder_go_back(self) :
    if len(self.last_dir) > 1 :
      print self.last_dir
      self.curdir=self.last_dir.pop(-1) # pop the last value from the visited folder folders
    else :
      # In case we have yet only 1 folder in the visited folder container.
      if self.last_dir[0].rfind("/") :
	# The value of the container is not the root folder ( / ) but not the /home/username folder who can be only visited folder. 
	self.last_dir[0]=self.last_dir[0][0:self.last_dir[0].rfind("/")]
	self.curdir=self.last_dir[0]
      elif self.last_dir[0].rfind("/") == 0 :
	# The value of the container is the root folder.
        self.last_dir[0]="/"
        self.curdir=self.last_dir[0]
      else :  
	# The value is the /home/username directory
        self.curdir=self.last_dir[0]
    
    self.file_name_entry.delete(0,END)
    self.select_filepath=""
    
    self.dir_name_entry.delete(0,END) 
    self.dir_name_entry.insert(0,"../"+basename(self.curdir)) 
    
    self.ls_dir()
    self.update_canvas()  
      
  def set_filetype_filter(self) :
    '''Change filetype filter.'''
    self.file_filter_menubutton.config(text=self.file_filter_var.get())
    self.file_filter_extension=self.file_filter_var.get()[1::]          # Contains the selected filetype ( in form '.'+filetype ).
    
    self.file_name_entry.delete(0,END)
    self.select_filepath=""
       
    self.ls_dir()
    self.update_canvas()  
    
  def item_selection_ok(self) :
    '''Return the selected filepath or empty string
       and destroy File_selector instance'''
       
    if self.select_filepath :
      self.toplevel.destroy()
      return self.select_filepath
  
  def item_selection_quit(self) :
    '''destroy File_selector instance''' 
    self.toplevel.destroy()
    
  def item_selection_home(self) :
    '''Change current directory to the /home/username folder'''
    self.curdir=expanduser("~")
    self.select_filepath=""
    self.file_name_entry.delete(0,END)
    
    self.last_dir=[]
    self.last_dir.append(expanduser("~"))
    
    self.dir_name_entry.delete(0,END) 
    self.dir_name_entry.insert(0,"../"+basename(self.curdir))    
    self.ls_dir()
    self.update_canvas()  
    
        
      
#a=Tk()
#b=File_selector(a)
#a.mainloop()
    
    
