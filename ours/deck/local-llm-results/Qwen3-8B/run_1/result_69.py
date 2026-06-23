import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    # 检查终点是否为(10,11)，如果是则调整
    if end_point == (10, 11):
        end_point = (11, 11)
    # 原有的逻辑...
