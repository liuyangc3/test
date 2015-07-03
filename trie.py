# -*- coding: utf-8 -*-

# 字母 基数数
# 每个节点有26个字节点[a-z]




class Node(object):
    """docstring for Node"""

    def __init__(self):
        self.children = {}  # 子节点
        self.flag = False  # 是否有words结束在这个节点上

    def add(self, char):
        """ 子节点添加字母操作, char 作为 key, Node实例作为值 """
        self.children[char] = Node()


class Trie(object):
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        """ 向 Trie 树添加单词"""
        node = self.root
        for char in word:
            # 先判断这个词的第一个字母 是否已经被添加过了
            if char not in node.children:
                node.add(char)  # 没有添加过,新建这个节点
            node = node.children[char]  # 指向子节点
        node.flag = True  # 单词结束时, 标记这个节点

    def find(self, word):
        """ Trie 树里是否有这个单词 """
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
        return node.flag

    def _get_node(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def find_prefix(self, prefix):
        """ 返回所有 前缀是 prefix 的单词"""
        node = self._get_node(prefix)
        result = []
        if not node:
            return result

        def find_word(_prefix, _dict):
            """ 递归函数
            如果找到 flag 为 True 的节点, 将该节点代表的单词加入列表
            """
            for _char, _node in _dict.items():
                if _node.flag:
                    result.append(_prefix + _char)
                if _node.children:
                    find_word(_prefix + _char, _node.children)

        find_word(prefix, node.children)
        return result

if __name__ == '__main__':
    t = Trie()
    t.insert('fuck')
    t.insert('fucy')
    t.insert('fucn')
    t.insert('fucp')
    print(t.find_prefix('fuck'))