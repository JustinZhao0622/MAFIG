import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)
    ...
    """
    # 检查终点是否为故障点
    if end_point == (7, 8):
        end_point = (8, 8)
    # 原有的逻辑...
