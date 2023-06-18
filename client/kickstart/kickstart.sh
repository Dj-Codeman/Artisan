#!/bin/bash

# ! ssh needs to be re-initialized 
version="2.1"

rm /etc/ssh/ssh_host_*
rm /root/.bash_history
dpkg-reconfigure openssh-server

# adding trusted ssh ids 
cat /usr/local/bin/Artisan/Firstrun/artisan_trusted.stub > /root/.ssh/authorized_keys

# running system update
apt-get update -y

# generate random-ish hostname 
hostname_sub="client"
hostname_domain="$(echo $RANDOM | md5sum | head -c 20; echo;)"
new_hostname="$hostname_sub-$hostname_domain"

# setting the hostname 
hostnamectl set-hostname "$new_hostname"

# enabeling the Manager and Update Checker
systemctl enable ArtisanManager.timer --now
systemctl enable ArtisanUpdater.timer

# Disable the first run script
systemctl disable ArtisanFirstrun

reboot