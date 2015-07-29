#!/bin/bash -e

sudo echo 'Start installation from the program ScreenLocker...'

if [[ $? != 0 ]] ;
then
  echo "You must run this installation script as root"
  return 1
fi

python -c 'import pygame'
if [[ $? != 0 ]] ; then
  sudo echo "ScreenLocker require pygame python module"
  sudo echo "Install the package python-pygame and retry installation."
  return 1
fi

python -c 'import Pmw'
if [[ $? != 0 ]] ; then

  sudo echo "ScreenLocker require Pmw python module"
  sudo echo "Install the package python-pmw and retry installation."
  return 1

fi


way_prg="$PWD/Sources/ScreenLocker.py"

way_prg="$PWD/Sources/ScreenLocker.py"


if [[ ! -d /usr/share/ScreenLocker ]]
then

  sudo mkdir /usr/share/ScreenLocker
  sudo cp -R * /usr/share/ScreenLocker
  sudo chmod -R a+w /usr/share/ScreenLocker/Settings
  sudo chmod go-x /usr/share/ScreenLocker/Settings/*
  sudo chmod -R a+w /usr/share/ScreenLocker/Images


fi

if [[ ! -f /usr/local/bin/ScreenLocker.py ]]
then

  sudo cp "${way_prg}" "/usr/local/bin/"
  sudo chmod a+x "/usr/local/bin/ScreenLocker.py"

fi




way_prg="python2 /usr/local/bin/ScreenLocker.py"
way_icon="/usr/share/ScreenLocker/ScreenLocker_icon.png"

if [[ -d /usr/share/applications && ! -f /usr/share/applications/ScreenLocker.desktop ]]
then

  sudo cp "$PWD/Desktop/ScreenLocker.desktop" /usr/share/applications/ScreenLocker.desktop

else

  sudo echo "Cannot create dekstop shortcut:"
  sudo echo "No folder: /usr/share/applications"
  sudo echo

fi


sudo echo 'ScreenLocker installation successfull'


