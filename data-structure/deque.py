# -*- coding:utf-8 -*-
"""
Deque : double-ended queue

add to rear -->      +----+----+---+ <-- add to front
                     |item|item|...|
remove from rear <-- +----+----+---+ --> remove from front
"""


class Deque(object):
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def add_front(self, value):
        self.items.append(value)

    def remove_front(self):
        return self.items.pop()

    def add_rear(self, value):
        self.items.insert(0, value)

    def remove_rear(self):
        return self.items.pop(0)

    def __len__(self):
        return len(self.items)


"""
 A palindrome is a string that reads the same forward and backward, for example, radar, toot, and madam
"""


def palchecker(string):
    deque = Deque()
    for char in string:
        deque.add_front(char)

    equal = True
    while len(deque) > 1 and equal:
        first = deque.remove_front()
        last = deque.remove_rear()
        if first != last:
            equal = False
    return equal

print(palchecker("madam"))
