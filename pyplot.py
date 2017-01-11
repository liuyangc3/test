# -*- coding:utf-8 -*-
from calendar import day_abbr
import matplotlib.pyplot as plt

# (qps,tps,conn)
data = [(15, 4, 10), (17, 5, 9), (10, 3, 5), (4, 2, 1), (20, 14, 6), (8, 3, 2), (16, 3, 14)]

qps_week, tps_week, conn_week = zip(*data)
plt.figure(1)                           # 第一张图

# QPS
plt.subplot(311)                        # 311 = 子图是3行1列共三张，其中的第一个子图
plt.title('daily QPS of this week')     # 标题
plt.axis([0, 6, 0, max(qps_week) + 5])  # 图的范围 x-min x-max y-min y-max
plt.xlabel('this week')                 # x 轴标签
plt.xticks(range(7), day_abbr)          # x 轴各列名称
plt.ylabel('QPS')
plt.plot(range(7), qps_week)

# TPS
plt.subplot(312)                        # 第二个子图
plt.title('daily TPS of this week')
plt.axis([0, 6, 0, max(tps_week) + 5])
plt.xlabel('this week')
plt.xticks(range(7), day_abbr)
plt.ylabel('TPS')
plt.plot(range(7), tps_week)

# Connection
plt.subplot(313)
plt.title('daily connection of this week')
plt.axis([0, 6, 0, max(conn_week) + 5])
plt.xlabel('this week')
plt.xticks(range(7), day_abbr)
plt.ylabel('connection')
plt.plot(range(7), conn_week)

plt.tight_layout()                      # 自动调整子图 subplot 之间的间距
plt.show()
