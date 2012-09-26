AppsCake - Web Frontend for AppScale Tools
==========================================

"AppsCake makes deploying AppScale a piece of cake"

AppsCake is a simple and lightweight web application that allows users to
interact with AppScale tools over the web. This way even those users who
are not familiar with general cloud principles or those who are not
comfortable with working with a traditional command line interface can
get started with deploying AppScale clouds and AppScale cloud applications.

AppsCake has been developed using the Ruby programming language and is 
based on Sinatra. So far it has been tested in Xen and EC2 cloud
environments.

Prerequisites
=============

Following software is required to install and run AppsCake:

1. Ruby interpreter
2. Sinatra gem
3. AppScale tools gem (or alternatively you can install AppScale tools
   binary distribution on your machine/VM and put them in the PATH)

Installation
============

There are 2 ways to install AppsCake:

1. Pull the source from the Github
	- https://github.com/AppScale/appscake

2. Install the AppsCake gem
	sudo gem install appscake

Running AppsCake
================

To launch AppsCake, simply go into the bin directory and execute the
'appscake' script:

./appscake

Once the server has started up, fire up your web browser and navigate
to https://<appscake-host>:8443

If you're installing AppsCake on an EC2 image make sure to modify your
security group so that it allows inbound traffic on the port 8443.



======================================================================
AppsCake is a project by the UCSB RACELab
http://appscake.cs.ucsb.edu

