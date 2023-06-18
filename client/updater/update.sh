#!/bin/bash

# * stoping all of the Artisan Services

systemctl stop ArtisanManager.timer
systemctl stop ArtisanUpdater.timer

# * Making dir to rollback 
cd /tmp/artisan_update/ || echo "Update ill formed quiting to minimize damage" && exit 1
mkdir /tmp/artisan_fallback/

mv -v /usr/local/bin/Artisan /tmp/artisan_fallback/Artisan.old/

mkdir -v /usr/local/bin/Artisan 

mkdir /usr/local/bin/Artisan/{Firstrun,Manager,Updater,Welcome}

# ! copy the files

# ! Manager 
# * Software
cp -v ./manager/*.py /usr/local/bin/Artisan/Manager/
cp -v ./manager/*.sh /usr/local/bin/Artisan/Manager/
cp -v ./manager/*.stub /usr/local/bin/Artisan/Manager/
chmod +x /usr/local/bin/Artisan/Manager/*
# * Service and timer files
cp -v ./manager/*.service /etc/systemd/system/
cp -v ./manager/*.timer /etc/systemd/system/

# ! Updater
# * Software
cp -v ./updater/*.sh /usr/local/bin/Artisan/Updater/
cp -v ./updater/*.py /usr/local/bin/Artisan/Updater/
chmod +x /usr/local/bin/Artisan/Updater/*
# * Service and timer files
cp -v ./updater/*.service /etc/systemd/system/
cp -v ./updater/*.timer /etc/systemd/system/

#! Welcome
# * Software
cp -v ./welcome/*.sh /usr/local/bin/Artisan/Welcome/
cp -v ./welcome/*.py /usr/local/bin/Artisan/Welcome/
chmod +x /usr/local/bin/Artisan/Welcome/*

#! remake soft links
rm /usr/local/bin/artisan
ln -sf /usr/local/bin/Artisan/Manager/artisan_manage.py /usr/local/bin/artisan

python3 /usr/local/bin/Artisan/Updater/update.py

cp /tmp/artisan_update/update_kickstart.php /usr/local/bin/Artisan/Updater/update_kickstart.php
chmod +x /usr/local/bin/Artisan/Updater/update_kickstart.php

version="Artisan Manager version: $(artisan --version-cli) installed"
echo "$version"

systemctl daemon-reload
systemctl start ArtisanManager.timer
systemctl start ArtisanUpdater.timer