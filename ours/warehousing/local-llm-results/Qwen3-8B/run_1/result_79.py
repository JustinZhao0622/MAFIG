import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)
    ...
    """
    # 修改：检查end_point是否为(9,7)，如果是则改为(10,7)
    if end_point == (9,7):
        end_point = (10,7)
    # 原有逻辑...
