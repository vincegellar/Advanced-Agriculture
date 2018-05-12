#!/bin/bash

sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'

sudo apt update
sudo apt upgrade -y
sudo apt install -y git mysql-server python3 python3-pip libatlas-base-dev nginx-light
sudo pip3 install --upgrade pip flask peewee pymysql numpy

git clone https://github.com/vincegellar/Advanced-Agriculture.git ~/app
cd ~/app
mysql -u root -proot -e "UPDATE mysql.user SET Grant_priv='Y' WHERE user = 'root';"
mysql -u root -proot < Database/create_mysql.sql
sudo cp nginx.conf /etc/nginx/sites-available/advanced-agriculture
sudo ln -s /etc/nginx/sites-available/advanced-agriculture /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo service nginx restart
