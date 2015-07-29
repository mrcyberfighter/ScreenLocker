#!/bin/bash -e

sudo echo 'Start desinstallation from the programm ScreenLocker...'

if [[ $? != 0 ]] ;
then
 
  echo "You must run this installation script as root"
  return 1
  
fi

if [[ -d /usr/share/ScreenLocker ]]
then

  sudo rm -R "/usr/share/ScreenLocker"
 
fi

if [[ -f "/usr/local/bin/ScreenLocker.py" ]]
then 

  sudo rm "/usr/local/bin/ScreenLocker.py"

fi

if [[ -d /usr/share/applications && -f /usr/share/applications/ScreenLocker.desktop ]]
then

  sudo rm "/usr/share/applications/ScreenLocker.desktop"
 
fi 

echo 'ScreenLocker desinstallation successfull'