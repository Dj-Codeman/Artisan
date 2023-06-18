#!/bin/bash

# * stoping all of the Artisan Services

systemctl stop ArtisanManager.timer
systemctl stop ArtisanUpdater.timer

# * Making dir to rollback 
cd /tmp/artisan_update/
mkdir /tmp/artisan_fallback/

mv -v /usr/local/bin/Artisan /tmp/artisan_fallback/Artisan.old/

mkdir -v /usr/local/bin/Artisan 

mkdir /usr/local/bin/Artisan/{Firstrun,Manager,Updater,Welcome}

# ! copy the files

# ! Manager 
# * Software
cp -v ./Artisan_Manager/*.py /usr/local/bin/Artisan/Manager/
cp -v ./Artisan_Manager/*.sh /usr/local/bin/Artisan/Manager/
cp -v ./Artisan_Manager/*.stub /usr/local/bin/Artisan/Manager/
chmod +x /usr/local/bin/Artisan/Manager/*
# * Service and timer files
cp -v ./Artisan_Manager/*.service /etc/systemd/system/
cp -v ./Artisan_Manager/*.timer /etc/systemd/system/

# ! Updater
# * Software
cp -v ./Artisan_Updater/*.sh /usr/local/bin/Artisan/Updater/
cp -v ./Artisan_Updater/*.py /usr/local/bin/Artisan/Updater/
chmod +x /usr/local/bin/Artisan/Updater/*
# * Service and timer files
cp -v ./Artisan_Updater/*.service /etc/systemd/system/
cp -v ./Artisan_Updater/*.timer /etc/systemd/system/

#! Welcome
# * Software
cp -v ./Artisan_Welcome/*.sh /usr/local/bin/Artisan/Welcome/
cp -v ./Artisan_Welcome/*.py /usr/local/bin/Artisan/Welcome/
chmod +x /usr/local/bin/Artisan/Welcome/*

#! remake soft links
rm /usr/local/bin/artisan
ln -sf /usr/local/bin/Artisan/Manager/artisan_manage.py /usr/local/bin/artisan

systemctl daemon-reload
systemctl start ArtisanManager.timer
systemctl start ArtisanUpdater.timer
