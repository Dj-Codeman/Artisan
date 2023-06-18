#!/bin/bash

cp -v /tmp/artisan_update/updater/*.sh /usr/local/bin/Artisan/Updater/
cp -v /tmp/artisan_update/updater/*.py /usr/local/bin/Artisan/Updater/
chmod -Rv +x /usr/local/bin/Artisan/*

python3 /usr/local/bin/Artisan/Updater/update.py

cp /tmp/artisan_update/update_kickstart.php /usr/local/bin/Artisan/Updater/update_kickstart.php
chmod +x /usr/local/bin/Artisan/Updater/update_kickstart.php

version="Artisan Manager version: ${artisan --version-cli} installed"
echo "$version"

systemctl daemon-reload
systemctl start ArtisanManager.timer
systemctl start ArtisanUpdater.timer