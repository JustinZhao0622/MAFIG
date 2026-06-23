import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)"""
    # 处理终点调整
    if end_point == (9, 8):
        end_point = (10, 8)
    # 其他逻辑...
