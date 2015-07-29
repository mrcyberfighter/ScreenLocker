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

from hashlib import md5,sha1,sha224,sha256,sha384,sha512

class Password() :
  def gen_password_hash(self,password,recursion) :
    hash_algorithm=[md5(),sha1(),sha224(),sha256(),sha384(),sha512()]
    
    i=0
    ii=0
    while i < recursion :
      if ii == len(hash_algorithm) :
	ii=0
      hash_algorithm[ii].update(password)
      password=hash_algorithm[ii].hexdigest()
      i += 1
      ii += 1
      
    return password
