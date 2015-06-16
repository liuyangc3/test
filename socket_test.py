#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'web'

import socket
import select

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
response += b'Hello, world!'

srvsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 地址重用
srvsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

srvsocket.bind(('0.0.0.0', 8000))
srvsocket.listen(1)

try:
    while True:
        client, address = srvsocket.accept()
        request = b''
        while EOL1 not in request and EOL2 not in request:
            request += client.recv(1024)
        # print('-' * 40 + '\n' + request.decode()[:-2])
        print('-'*40 + '\n' + request)
        client.send(response)
        client.close()
finally:
    srvsocket.close()
