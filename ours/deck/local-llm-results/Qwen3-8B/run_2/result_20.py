import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    # 检查终点是否为(11,7)，如果是则调整为(12,7)
    if end_point == (11,7):
        end_point = (12,7)
    # 原来的逻辑...
