#!/bin/bash
sudo apt-get update
sudo apt-get install -y ruby
sudo apt-get install -y rubygems
sudo apt-get install -y expect
sudo apt-get install -y git-core

sudo apt-get install -y ruby1.8-dev
sudo apt-get install -y openssl
sudo apt-get install -y libopenssl-ruby

sudo gem install sinatra
sudo gem install net-ssh
sudo gem install json
sudo gem install webrick
sudo gem install optiflag

tools_path=`which appscale-run-instances`
if [ -z "$tools_path" ]; then
  echo "AppScale Tools not found. Installing..."
  sudo gem install appscale-tools
fi

git clone https://github.com/AppScale/sample-apps.git
cp -rv sample-apps/python/guestbook ../repository
rm -rf sample-apps

echo "AppsCake is ready to rock and roll..."