#!/usr/bin/bash

set -e

pip install virtualenv --upgrade
pip install setuptools --upgrade
echo "virtualenv version ... $(virtualenv --version)"
echo "python version ... $(python -V)"
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb
pip install -r requirements.txt
pip install --pre vmprof

# download the chrome driver
wget https://chromedriver.storage.googleapis.com/2.27/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin
git clone --depth 1 git://github.com/vmprof/vmprof-server.git
pushd .
cd vmprof-server
pip install -r requirements/testing.txt
python manage.py migrate
python vmlog/test/data/loggen.py
python manage.py loaddata vmlog/test/fixtures.yaml
popd
