wget https://s3.amazonaws.com/appscale-build/setuptools-0.6c11.tar.gz
tar zxvf setuptools-0.6c11.tar.gz
cd setuptools-0.6c11
python setup.py install

cd ..
rm -r setuptools-0.6c11
rm setuptools-0.6c11.tar.gz

easy_install termcolor
easy_install M2Crypto 
easy_install SOAPpy
easy_install pyyaml
easy_install boto==2.6
easy_install argparse
easy_install django 
apt-get -y install expect

apt-get -y install mercurial
hg clone https://code.google.com/p/google-api-python-client/
cd google-api-python-client
python setup.py install
cd ..
rm -r google-api-python-client
