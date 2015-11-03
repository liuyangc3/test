```
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tar.xz
wget https://pypi.python.org/packages/source/p/pip/pip-7.1.2.tar.gz#md5=3823d2343d9f3aaab21cf9c917710196
wget https://pypi.python.org/packages/source/s/setuptools/setuptools-18.5.tar.gz#md5=533c868f01169a3085177dffe5e768bb

chomd 755 inventory.py
sudo ansible-playbook python.yml -i inventory.py --extra-vars '{"host":["192.168.0.1"]}'
sudo ansible-playbook setuptools.yml -i inventory.py --extra-vars '{"host":["192.168.0.1"]}'
sudo ansible-playbook pip.yml -i inventory.py --extra-vars '{"host":["192.168.0.1"]}'
```
