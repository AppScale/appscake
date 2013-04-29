![AppScale Logo](http://www.appscale.com/img/appscale-logo.png)

# Appscake - Web Frontend for AppScale Tools #

## About ##

"AppsCake makes deploying AppScale a piece of cake"

AppsCake is a simple and lightweight web application that allows users to
interact with AppScale tools over the web. This way even those users who
are not familiar with general cloud principles or those who are not
comfortable working with a traditional command line interface can get
started with deploying AppScale clouds and AppScale cloud applications.

AppsCake has been developed using the python programming language and is
based on Django. 

## Prerequisites ##
- Python 2.7
- Django 1.5 (get the tar ball here: https://www.djangoproject.com/download/1.5.1/tarball/)
- Git
- Expect (http://downloads.sourceforge.net/project/expect/Expect/5.45/expect5.45.tar.gz or 
  ```apt-get install expect```)

# Tools Install Process ##
Run ```bash get_tools.sh```.

### On an AppScale Image ###
Install the tools for python2.7 by going into appscale/tools/src_install and running
```bash appscale_install.sh```

### For Mac OSX ###
Install the tools by going into appscale-tools/osx and running
```bash appscale_install.sh```

### For Debian based systems ###
Install the tools by going into appscale-tools/debian and running
```bash appscale_install.sh```

### Source Install ###
Install the tools for python2.7 by going into appscale/tools/src_install
```bash appscale_install.sh```

# Running AppsCake #
```python2.7 manage.py runserver localhost:8000```

Go to http://localhost:8000 with a browser. 

If you are running AppScake on the image that you will be starting AppScale:
```/usr/local/Python-2.7.3/python manage.py runserver <ip>:8090```

Go to http://<ip>:8090 with a browser.

### Issues ###
Contact us if you have problems at: support@appscale.com or visit our IRC channel #appscale on freenode.net.


License
-------
This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://opensource.org/licenses/BSD-3-Clause
