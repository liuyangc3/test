# -*- coding:utf-8 -*-
import time
import logging
from stompest.sync import Stomp
from stompest.config import StompConfig
from stompest.protocol import StompSpec


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# use port 61613 for protocol Stomp
uri = 'failover:(tcp://10.201.20.21:61613,tcp://10.201.20.20:61613,tcp://10.201.10.204:61613)\
?randomize=false,startupMaxReconnectAttempts=3,initialReconnectDelay=7,maxReconnectDelay=8,maxReconnectAttempts=0'
config = StompConfig(uri)
client = Stomp(config)

queue_name = '/queue/liuyang-test'
try:
    client.connect()
    client.send(queue_name, 'test message 1')
    client.send(queue_name, 'test message 2')
    time.sleep(2)
    
    client.subscribe(queue_name, {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL})
    frame = client.receiveFrame()
    print('Got %s' % frame.info)
    frame = client.receiveFrame()
    print('Got %s' % frame.info)
except Exception as e:
    print(e)
finally:
    client.disconnect()
    
