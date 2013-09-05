echo "Installing setuptools if needed."
set +e
hash easy_install > /dev/null 2>&1
if [ $? -ne 0 ]; then
  set -e
  echo "setuptools not found - installing."
  mkdir -pv downloads
  cd downloads
  wget https://s3.amazonaws.com/appscale-build/setuptools-0.6c11.tar.gz
  tar zxvf setuptools-0.6c11.tar.gz
  pushd setuptools-0.6c11
  python setup.py install
  popd
  rm -fr setuptools-0.6c11*
fi
set -e

easy_install termcolor
easy_install SOAPpy
easy_install pyyaml
easy_install boto==2.6
easy_install argparse
easy_install django 
easy_install google-api-python-client
apt-get -y install expect

