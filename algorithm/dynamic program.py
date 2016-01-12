# -*- coding:utf-8 -*-

coins = [1, 3, 5]


def dp(money):
    """递归"""
    if money == 0:
        return 0
    result = []
    for i in range(len(coins)):
        coin = coins[i]
        if money >= coin:
            result.append(dp(money - coin) + 1)
    return min(result)

print dp(11)
