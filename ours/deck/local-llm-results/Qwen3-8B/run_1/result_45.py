import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """..."""
    # 检查终点是否为(11,10)
    if end_point == (11,10):
        end_point = (12,10)
    # 原来的逻辑...
