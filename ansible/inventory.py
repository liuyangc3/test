#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import json
import sys

~                                                   
# dynamic_inventory
def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--host')
    return parser.parse_args()

hosts = {"tomcat": ["172.16.200.83","172.16.200.51"]}

def out(host):
    info = {"ansible_ssh_port": 22, "ansible_ssh_user": "root"}
    info["ansible_ssh_host"] = host
    return info



if __name__ == '__main__':
    args = parse_args()
    if args.list:
        json.dump(hosts, sys.stdout)
    if args.host:
        json.dump(out(args.host), sys.stdout)
