# -*- coding: utf-8 -*-
# divide a iter Object into specific groups

import math

def divide(data_list, groups):
    """
    :param data_list: 带分组数组
    :param groups: 分组组数
    """
    length = len(data_list)
    if length == 1:
        return tuple(data_list)

    # 组数应该小于长度
    if groups > length:
        groups = length

    
    
    # 保证每组内元素个数更接近一些
    # 例如 o-7 分3组应该是 ([0,1,2], [3,4,5], [6,7]
    # 而不是 ([0,1], [2,3], [4,5,6,7] 
    # a non math lib version:
    # num_per_group = length // groups
    # if num_per_group <= length % groups:
    #    num_per_group += 1
    
    num_per_group = int(math.ceil(length * 1.0 / groups))

    slices = []
    start = 0
    for i in range(groups):
        end = start + num_per_group
        slices.append(slice(start, end))
        start = end
    # 最后一次切割应该到data的末尾
    slices[-1] = slice(start - num_per_group, length)
    return tuple([data_list[s] for s in slices])


print divide(range(8), 3)
print divide(range(14), 4)
print divide(range(14), 3)
print divide(range(14), 2)

# groups is bigger than iter
print divide(range(3), 5)
