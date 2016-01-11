# -*- coding:utf-8 -*-

def max_heapify(array, index, array_size):
    # 使当前节点,及子节点满足最大堆性质
    i_left = 2 * index + 1
    i_right = 2 * (index + 1)

    i_max = index
    if i_left < array_size and array[i_max] < array[i_left]:
        i_max = i_left
    if i_right < array_size and array[i_max] < array[i_right]:
        i_max = i_right

    # 如果最大值不在跟节点 则交换子节点和根节点
    if i_max != index:
        array[index], array[i_max] = array[i_max], array[index]
        max_heapify(array, i_max, array_size)


def build_max_heap(array, array_size):
    # 构建最大堆
    # 从非子叶节点开始
    indexes = range(array_size/2)
    indexes.reverse()
    for i in indexes:
        max_heapify(array, i, array_size)
    return array


def heap_sort(array):
    array_size = len(array)
    array = build_max_heap(array, array_size)
    # 交换最后一个子节点和根节点
    # 重新调整堆
    for i in range(array_size - 1, -1, -1):
        array[i], array[0] = array[0], array[i]
        max_heapify(array, 0, i)
    return array


print heap_sort([16,7,3,20,17,8])


