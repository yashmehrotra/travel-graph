#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

echo "Updating"
apt-get update > /dev/null

echo "Installing Git"
apt-get install git git-core -y > /dev/null

echo "Installing Nginx"
apt-get install nginx -y > /dev/null

echo "Installing Dependencies"
apt-get install libpq-dev python-dev python-psycopg2 -y > /dev/null

echo "Installing Python-pip"
apt-get install python-pip -y > /dev/null

echo "Installing and setting up virtualenvwrapper"
pip install virtualenvwrapper > /dev/null
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc

echo "Installing nodejs and npm"
apt-get install g++ make python-software-properties -y > /dev/null
apt-add-repository ppa:chris-lea/node.js -y > /dev/null
echo "Updating"
apt-get update > /dev/null
echo "Installing now.."
apt-get install nodejs -y > /dev/null

echo "Setting up project specifics now...."
mkvirtualenv tg
echo "Installing requirements.txt"
pip install -r requirements.txt > /dev/null

echo "Installing npm dependencies"
npm install --no-bin-link

echo "Installing bower dependencies"
bower install
