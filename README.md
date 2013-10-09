![AppScale Logo](http://www.appscale.com/img/logos/appscale-logo-349x83.jpg)

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

## Install Process ##
Run ```bash get_tools.sh```, which downloads the AppScale Tools and puts them in the
appscake directory.

Next, install the tools dependencies by going into the appscake/debian directory
and running
```bash appscake_dependencies_install.sh```

# Running AppsCake #
```python2.7 manage.py runserver localhost:8000```

Go to http://localhost:8000 with a browser. 

If you are running AppsCake on the image that you will be starting AppScale, start AppsCake by running:
```/usr/local/Python-2.7.3/python manage.py runserver <ip>:8090```

Go to `http://<ip>:8090` with a browser.

### Issues ###
Contact us if you have problems at support@appscale.com or visit our IRC channel, #appscale on freenode.net.

***

# AppsCake w/ virtualenv #
Prerequisites: Python 2.6+, pip/easy_install

1. Installing virtualenv/virtualenvwrapper via the terminal:
```
sudo pip install virtualenvwrapper
```

2. Create the AppsCake virtualenv working directory:
```
virtualenv appscake-env
```

3. Open newly created virtualenv working directory:
```
cd appscake
```

4. Activate the AppsCake virtualenv:
```
source bin/activate
```

5. Installing dependencies for debian systems -- for Mac OSX ensure git and expect are installed in your path (if not use <a href="http://mxcl.github.io/homebrew/">Homebrew</a> to install):
```
sudo apt-get install git-core
sudo apt-get install expect
```

6. Cloning the AppsCake repository:
```
git clone https://github.com/AppScale/appscake.git
```

7. Installing the AppScale Tools and requirements:
```
cd appscake
bash get_tools.sh
sudo pip install -r requirements.txt
```

8. Running AppsCake:
```
python manage.py runserver
```

9. Navigate to the URL returned from the command above to use AppsCake.



License
-------
This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://opensource.org/licenses/BSD-3-Clause


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/DrOctogon/appscake/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

