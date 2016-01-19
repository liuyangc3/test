#!/usr/bin/python
# -*- coding: utf-8 -*-


class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None


    def loop(cls):
        result = [cls.v]
        while node.next:
            node = node.next
            result.append(node.v)
        return result

def reverse(node):
    """ pass first node and reverse linklist """
    yesterday = current = None
    i = 0
    while node:
        if i > 0:
            if i > 1:
                before_yesterday, yesterday = yesterday, current
                yesterday.next = before_yesterday
            yesterday = current
        current = Node(node.v)
        node = node.next
        i += 1
    current.next = yesterday
    return current
