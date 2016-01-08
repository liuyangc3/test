#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import struct

# A simple raw socket implementation in Python
# TCP SYN packet on Linux

"""
IP Header
0                   1                   2                   3
 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Version : 4 is ipv4 and 6 is ipv6
IHL: IP Header Length, represent how many 32 bit words(4bytes)
     the maximum length is 15 words (15×32 bits) or 480 bits = 60 bytes.
Type of Service: if not zero first 6 bit define special protocol like VoIP, last 2 bit for ECN
Total Length: total IP datagram length in bytes
Flags:
    bit 0: Reserved; must be zero
    bit 1: Don't Fragment (DF)
    bit 2: More Fragments (MF)
Fragment Offset: a maximum offset of (2^13 – 1) × 8 = 65,528 bytes
Time To Live (TTL): how many hops before router drop packets, minus 1 when through a router
Protocol: 1 ICMP, 2 IGMP, 6 TCP, 17 UDP, 41 ENCAP, 89 OSPF, 132 SCTP
Options (if IHL > 5)
"""


def create_ip_header(sip, dip):
    """Raw socket允许用户自定义构建TCP/IP数据包的header
    跳过底层操作系统TCP/IP 协议栈
    """
    # ip header fields
    version = 4  # ipv4
    header_len = 5  # 5 * 4 = 20 bytes
    ver_hl = (version << 4) + header_len  # 两个 4-bit数据合并成一个字节
    ip_dscp = 0  # new name of tos
    total_len = 0  # kernel will fill the correct total length
    ip_id = 54321  # Id of this packet
    ip_frag_offset = 0
    ip_ttl = 255
    ip_protocol = socket.IPPROTO_TCP
    ip_checksum = 0  # kernel will fill the correct checksum
    ip_saddr = socket.inet_aton(sip)
    ip_daddr = socket.inet_aton(dip)

    # the ! in the pack format string means network order (big-endian)
    ip_header = struct.pack('!BBHHHBBH4s4s',
                            ver_hl, ip_dscp, total_len,
                            ip_id, ip_frag_offset,
                            ip_ttl, ip_protocol, ip_checksum,
                            ip_saddr, ip_daddr)
    return ip_header


"""
TCP Header
0                   1                   2                   3
    1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |          Source Port          |       Destination Port        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                        Sequence Number                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Acknowledgment Number                      |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Data |           |U|A|P|R|S|F|                               |
   | Offset| Reserved  |R|C|S|S|Y|I|            Window             |
   |       |           |G|K|H|T|N|N|                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |           Checksum            |         Urgent Pointer        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Options                    |    Padding    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                             data                              |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Urgent Pointer:
"""


# make a tcp header without checksum
tcp_sport = 15821
tcp_dport = 80

tcp_seq = 19861010  # 32-bit sequence number random (my birth day!)
tcp_ack_seq = 0     # 32-bit ACK number
tcp_data_offset = 5
tcp_offset_reserv = (tcp_data_offset << 4)

# flags
tcp_flag_urg = 0
tcp_flag_ack = 0
tcp_flag_psh = 0
tcp_flag_rst = 0
tcp_flag_syn = 1  # SYN
tcp_flag_fin = 0
tcp_flags = tcp_flag_fin + (tcp_flag_syn << 1) + (tcp_flag_rst << 2) + (tcp_flag_psh << 3) + (tcp_flag_ack << 4) + (tcp_flag_urg << 5)

tcp_window_size = 3000
tcp_check = 0  # re fill it later
tcp_urgent_ptr = 0
tcp_header = struct.pack('!HHLLBBHHH', tcp_sport, tcp_dport,
                         tcp_seq,
                         tcp_ack_seq,
                         tcp_offset_reserv, tcp_flags, tcp_window_size,
                         tcp_check, tcp_urgent_ptr)


def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)


def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = (ord(msg[i]) << 8) + ord(msg[i+1])
        s = carry_around_add(s, w)
    return ~s & 0xffff


ip_src = '10.100.27.29'
ip_dst = socket.gethostbyname("www.nxin.com")

send_data = "Hello World!"

# pseudo header fields
tcp_src = socket.inet_aton(ip_src)
tcp_dst = socket.inet_aton(ip_dst)
tcp_length = len(tcp_header) + len(send_data)
psh = struct.pack('!4s4sBBH', tcp_src, tcp_dst, 0, socket.IPPROTO_TCP, tcp_length)
psh = psh + tcp_header + send_data

if len(psh) % 2 != 0:
    psh += '\0'  # padding
tcp_checksum = checksum(psh)

# make the tcp header again and fill the correct checksum
tcp_header = struct.pack('!HHLLBBHHH', tcp_sport, tcp_dport, tcp_seq, tcp_ack_seq,
                         tcp_offset_reserv, tcp_flags, tcp_window_size, tcp_checksum, tcp_urgent_ptr)


ip_header = create_ip_header(ip_src, ip_dst)
packet = ip_header + tcp_header + send_data

# create a raw socket
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
s.sendto(packet, (ip_dst, 0))
