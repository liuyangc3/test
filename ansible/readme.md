```
# get Python source
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tar.xz
chomd 755 inventory.py
# run playbook
sudo ansible-playbook python.yml -i inventory.py --extra-vars '{"host":["192.168.0.1"]}'
```
