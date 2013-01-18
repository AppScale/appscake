AppsCake - Web Frontend for AppScale Tools
==========================================

"AppsCake makes deploying AppScale a piece of cake"

AppsCake is a simple and lightweight web application that allows users to
interact with AppScale tools over the web. This way even those users who
are not familiar with general cloud principles or those who are not
comfortable working with a traditional command line interface can get
started with deploying AppScale clouds and AppScale cloud applications.

AppsCake has been developed using the Ruby programming language and is 
based on Sinatra. So far it has been tested in Xen and EC2 cloud
environments.

Prerequisites
=============

Following software is required to install and run AppsCake:

1. Ruby interpreter
2. Sinatra gem
3. AppScale tools gem (or alternatively you can install AppScale tools
   binary distribution on your machine/VM and put it in the PATH)

Installation
============

There are 2 ways to install AppsCake:

1. Pull the latest source from the Github
	git clone https://github.com/AppScale/appscake

If you are on a Debian based system such as Ubuntu or Mint, you can run
the 'debian_setup.sh' script in the 'bin' directory to install all the
required dependencies and setup AppsCake.

2. Install the AppsCake gem
	sudo gem install appscake

Gem installation will take care of installing the necessary dependencies
too.

Next, install the AppScale Tools:

cd ~
git clone git://github.com/AppScale/appscale-tools
cd appscale-tools/debian
bash appscale_build.sh


Running AppsCake
================

If you installed AppsCake from source, simply go into the 'bin' directory
of the installation and run the 'appscake' script.

./appscake -td ~/appscale-tools

If you installed the AppsCake gem, simply execute the 'appscake' command
(which should be in your PATH).

Once the server has started up, fire up your web browser and navigate
to https://<appscake-host>:28443

If you're installing AppsCake on an EC2 image make sure to modify your
security group so that it allows inbound traffic on the port 28443.

Optional Parameters
===================

You may pass in following optional parameters to AppsCake to customize
its behavior.

* -p, --port        Specify a port other than 28443 to start AppsCake on
* -td, --tools-dir  Directory where AppScale-Tools are installed
* -h                Display a help message


======================================================================
AppsCake is a project by the UCSB RACELab
http://appscale.cs.ucsb.edu

