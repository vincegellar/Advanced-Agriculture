#!/bin/bash

# Set MySQL root password
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'

# Add official Node.js source
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -

# Add Yarn source
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

# Install dependencies
sudo apt update
sudo apt upgrade -y
sudo apt install -y git libatlas-base-dev mysql-server nginx-light nodejs python3 python3-pip yarn
sudo pip3 install --upgrade flask numpy peewee pip pymysql

# Set up application
git clone https://github.com/vincegellar/Advanced-Agriculture.git ~/app
cd ~/app
mysql -u root -proot -e "UPDATE mysql.user SET Grant_priv='Y' WHERE user = 'root';"
mysql -u root -proot < Database/create_mysql.sql
sudo ln -s /home/pi/app/nginx.conf /etc/nginx/sites-enabled/advanced-agriculture
sudo rm /etc/nginx/sites-enabled/default
sudo service nginx restart
