#!/bin/bash

# * stoping all of the Artisan Services

systemctl stop Artisan_Manager.timer
systemctl stop Artisan_Updater.timer

# * Making dir to rollback 
cd /tmp/artisan_update/ || echo "Update ill formed"

# * Setting directories
mkdir /tmp/artisan_fallback/
mkdir -v /usr/local/bin/Artisan 
mkdir -v /usr/local/bin/Artisan/bin
cp -v /usr/local/bin/Artisan/ /tmp/artisan_fallback

# ! copy the files

# ! Client
cp -v ./bin/* /usr/local/bin/Artisan/bin/
cp -v ./static/* /usr/local/bin/Artisan/static/
cp -v /usr/local/bin/Artisan/static/Artisan_*.service /etc/systemd/system/
cp -v /usr/local/bin/Artisan/static/Artisan_*.timer /etc/systemd/system/

#! remake soft links
rm /usr/local/bin/artisan
ln -sf /usr/local/bin/Artisan/bin/manage_machine /usr/local/bin/artisan_update

python3 /usr/local/bin/Artisan/bin/update_message

chmod +x /usr/local/bin/Artisan/bin/*

version="Artisan has been updated"
echo "$version"

#! custom code needed on new runs 

systemctl daemon-reload
#systemctl start Artisan_Manager.timer
#systemctl start Artisan_Updater.timer