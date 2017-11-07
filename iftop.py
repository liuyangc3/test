import re
import time
import shlex
from datetime import datetime
import subprocess32 as subprocess

# iftop command stdout format
"""
iftop -PBbNnt -i eth0

   # Host name (port/service if enabled)            last 2s   last 10s   last 40s cumulative
--------------------------------------------------------------------------------------------
   1 10.212.25.13:80                          =>      120KB      120KB      120KB      241KB
     171.104.61.0:38676                       <=     2.04KB     2.04KB     2.04KB     4.09KB
   2 10.212.25.13:80                          =>     23.7KB     23.7KB     23.7KB     47.4KB
     107.164.194.250:37842                    <=       590B       590B       590B     1.15KB
   3 10.212.25.13:718                         =>     4.87KB     4.87KB     4.87KB     9.73KB
     10.212.25.6:2049                         <=     16.8KB     16.8KB     16.8KB     33.5KB
   4 10.212.25.13:80                          =>     12.7KB     12.7KB     12.7KB     25.4KB
     107.164.194.250:37824                    <=       288B       288B       288B       575B
   5 10.212.25.13:80                          =>     10.6KB     10.6KB     10.6KB     21.2KB
     118.190.107.80:4219                      <=       277B       277B       277B       554B
   6 10.212.25.13:99999                       =>     4.28KB     4.28KB     4.28KB     8.55KB
     106.120.185.159:3306                    <=       277B       277B       277B       554B
--------------------------------------------------------------------------------------------
Total send rate:                                      203KB      203KB      203KB
Total receive rate:                                  27.2KB     27.2KB     27.2KB
Total send and receive rate:                          230KB      230KB      230KB
--------------------------------------------------------------------------------------------
Peak rate (sent/received/total):                      203KB     27.2KB      230KB
Cumulative (sent/received/total):                     406KB     54.5KB      461KB
============================================================================================
...
"""


def startswith_number_and_ip(line):
    line = line.strip()
    pattern = re.compile('\d+ \d+\.')
    m = pattern.match(line)
    return m is not None


def parse_cmd_output(proc):
    in_block = False
    first_line = None
    data_in, data_out = {}, {}

    # break at line is ''
    for line in iter(proc.stdout.readline, ''):

        if in_block:
            parse_block(first_line, line, data_in, data_out)
            in_block = None

        if startswith_number_and_ip(line):
            in_block = True
            first_line = line

        if line.startswith("Cumulative"):
            timestamp = int(time.time()) - 2  # 2 seconds before because bandwidth is last 2s
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            return (date, data_in), (date, data_out)


def parse_block(f_line, line, data_in, data_out):
    # A block is two lines like below:
    # 1 10.212.25.13:80         =>      120KB      120KB      120KB      241KB
    #   171.104.61.0:38676      <=     2.04KB     2.04KB     2.04KB     4.09KB

    parts = f_line.split()
    out_port = parts[1].split(':')[-1]
    out_bytes = parts[3]

    parts = line.split()
    in_ip = parts[0].split(':')[0]
    in_bytes = parts[2]

    if out_port in data_in:
        data_in[out_port][in_ip] += human2bytes(in_bytes)
    else:
        data_in[out_port] = {in_ip: human2bytes(in_bytes)}

    if out_port in data_out:
        data_out[out_port][in_ip] += human2bytes(out_bytes)
    else:
        data_out[out_port] = {in_ip: human2bytes(out_bytes)}


def human2bytes(human):
    """
    >>> human2bytes('0B')
    0
    >>> human2bytes('1KB')
    1024
    >>> human2bytes('1MB')
    1048576
    """
    symbols = {"B": 1, "KB": 1024, "MB": 1048576}

    def split(string):
        for i, char in enumerate(string):
            if not (char.isdigit() or char == "."):
                return string[:i], string[i:]

    num, unit = split(human)
    n = float(num)

    return n * symbols[unit]


if __name__ == '__main__':
    # iftop command arguments
    # -N Do not resolve port
    # -n Do not resolve hostname
    # -P Display port
    # -B Display bandwidth rates in bytes/sec
    # -b Do not display bar graphs of traffic
    # -i interface
    # -t text output mode, print the output to STDOUT
    cmd = "/usr/sbin/iftop -PBbNnt -i eth0"

    # If get error :AttributeError: 'module' object has no attribute 'DEVNULL'
    # see https://github.com/google/python-subprocess32/pull/24
    # wget https://raw.githubusercontent.com/google/python-subprocess32/master/subprocess32.py
    with subprocess.Popen(
            shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as p:
        while p.poll() is None:
            i, o = parse_cmd_output(p)
            print(i, o)
