#!/usr/bin/python
# -*- coding: utf-8 -*-

# ansible dynamic inventory executable script

import argparse
import json
import sys


# add  class B/C network ip address
hosts = []
for i in xrange(1, 255):
    for j in xrange(1, 255): 
        hosts.append("192.168.{0}.{1}".format(i, j))
        hosts.append("172.16.{0}.{1}".format(i, j))
        
inventorys = {"groupname": hosts}

def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--host')
    return parser.parse_args()


def get_host_info(ip):
    host_info = {"ansible_ssh_port": 22, "ansible_ssh_user": "root"}
    host_info["ansible_ssh_host"] = ip
    return host_info

if __name__ == '__main__':
    args = parse_args()
    if args.list:
        json.dump(inventorys, sys.stdout)
    if args.host:
        json.dump(get_host_info(args.host), sys.stdout)
