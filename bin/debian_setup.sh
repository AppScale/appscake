#!/bin/bash
sudo apt-get update

hash ruby > /dev/null 2>&1
if [ $? -ne 0 ]; then
  sudo apt-get install -y ruby
fi

hash rubygems > /dev/null 2>&1
if [ $? -ne 0 ]; then
  sudo apt-get install -y rubygems
fi

sudo apt-get install -y expect
sudo apt-get install -y git-core

rubydev=`dpkg -l | grep ruby1.8-dev | wc -l`
if [ $rubydev == "0" ]; then
  sudo apt-get install -y ruby1.8-dev
fi
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