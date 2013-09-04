easy_install termcolor M2Crypto SOAPpy pyyaml boto==2.6 argparse django 
apt-get -y install expect

curl https://s3.amazonaws.com/appscale-build/setuptools-0.6c11.tar.gz > setuptools-0.6c11.tar.gz
tar zxvf setuptools-0.6c11.tar.gz
cd setuptools-0.6c11
python setup.py install

rm -fdr setuptools-0.6c11
