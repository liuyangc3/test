# -*- coding:utf-8 -*-
import json
import os_client_config

nova = os_client_config.make_client(
    'compute',
    auth_url='http://x.y.z:5000',
    username='liuyang',
    password='*******',
    # project_id='5eabd20c9803431cbb8e6f2c59df0683',
    project_name='XXXXX',
    region_name='RegionOne')


for server in nova.servers.list():
    print(json.dumps(server._info, sort_keys=True, indent=4, separators=(',', ': ')))
