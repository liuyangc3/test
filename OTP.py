#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'tadeck'
__url__ = 'https://github.com/tadeck/onetimepass'

import hmac
import base64
import struct
import hashlib
import time


def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(h[19]) & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time())//30)

if __name__ == '__main__':
    print(get_totp_token('ATFP7MBKXNV7AORX'))