# -*- coding:utf-8 -*-
# author : liuyangc3

import socket

RECV_SIZE = 4096


class Client(object):
    def __init__(self,
                 server,
                 timeout=None):
        self.sock = None
        self.server = server
        self.timeout = timeout

    def _connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.server)
        sock.settimeout(self.timeout)
        self.sock = sock

    def _close(self):
        if self.sock:
            self.sock.close()
        self.sock = None

    def get(self, name):
        name += b''
        cmd = name + b'\r\n'
        if not self.sock:
            self._connect()
        self.sock.sendall(cmd)

        buf = b''
        result = []
        while True:
            buf, line = parseline(self.sock, buf)
            if line == b'END':
                self._close()
                return result
            result.append(line)


def parseline(sock, buf):
    chunks = []
    last_char = b''

    while True:
        if last_char == b'\r' and buf[0:1] == b'\n':
            # Strip the last character from the last chunk.
            chunks[-1] = chunks[-1][:-1]
            return buf[1:], b''.join(chunks)
        elif buf.find(b'\r\n') != -1:
            before, sep, after = buf.partition(b"\r\n")
            chunks.append(before)
            return after, b''.join(chunks)

        if buf:
            chunks.append(buf)
            last_char = buf[-1:]

        try:
            buf = sock.recv(RECV_SIZE)
        except IOError as e:
            raise e

if __name__ == "__main__":
    c = Client(("172.16.200.98", 11211), timeout=5)
    print c.get("stats slabs")
