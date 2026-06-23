import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    # 检查终点是否为故障点
    if end_point == (11, 12):
        end_point = (12, 12)
    # 原来的逻辑...
