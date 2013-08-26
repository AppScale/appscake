![AppScale Logo](http://www.appscale.com/img/appscale-logo.png)

# Appscake - Web Frontend for AppScale Tools #

## About ##

"AppsCake makes deploying AppScale a piece of cake"

AppsCake is a simple and lightweight web application that allows users to
interact with AppScale Tools over the web. This way, even those users who
are not familiar with general cloud principles or those who are not
comfortable working with a traditional command line interface can get
started with deploying AppScale clouds.

AppsCake has been developed using the Python programming language and uses Django.

## Prerequisites ##
- Python 2.7
- Django 1.5 (get the tar ball here: https://www.djangoproject.com/download/1.5.1/tarball/) or 
  run "easy_install django"
- Git
- Expect (http://downloads.sourceforge.net/project/expect/Expect/5.45/expect5.45.tar.gz or 
  ```apt-get install expect```)

## Tools Install Process ##
Run ```bash get_tools.sh```, which downloads the AppScale Tools and puts them in the
appscake directory. Next, install the AppScale Tools:

### On an AppScale Image ###
Install the tools for Python 2.7 by going into appscale-tools/src_install and running
```bash appscale_install.sh```

### For Mac OSX ###
Install the tools by going into appscale-tools/osx and running
```bash appscale_install.sh```

### For Debian based systems ###
Install the tools by going into appscale-tools/debian and running
```bash appscale_install.sh```

### Source Install ###
Install the tools by going into appscale-tools/src_install and running
```bash appscale_install.sh```

# Running AppsCake #
```python2.7 manage.py runserver localhost:8000```

Go to http://localhost:8000 with a browser. 

If you are running AppsCake on the image that you will be starting AppScale, start AppsCake by running:
```/usr/local/Python-2.7.3/python manage.py runserver <ip>:8090```

Go to `http://<ip>:8090` with a browser.

### Issues ###
Contact us if you have problems at support@appscale.com or visit our IRC channel, #appscale on freenode.net.


License
-------
This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://opensource.org/licenses/BSD-3-Clause


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/DrOctogon/appscake/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

