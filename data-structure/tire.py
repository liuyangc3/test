# -*- coding: utf-8 -*-

# 字母 基数数
# 每个节点有26个字节点[a-z]

class Node(object):
    def __init__(self, char=None, word=None):
        self.char = char  # 当前节点保存的字符
        self.word = word  # 当前节点和到root节点保存的词
        self.childNodes = []  # 当前节点的子节点


class Tire(object):
    """docstring for Tire"""

    def __init__(self, node=Node()):
        self.root = node
        self.char = node.char

    def add(self, word):
        """ 添加子节点 """
        root = self.root
        if word:
            words = list(word)
            child = Node()
            child.char = words.pop(0)
            if words:
                Tire(child).add(''.join(words))
            root.childNodes.append(child)


if __name__ == '__main__':
    tire = Tire()
    tire.add('fuck')
    for node in tire.root.childNodes:
        print(node.childNodes.char)
