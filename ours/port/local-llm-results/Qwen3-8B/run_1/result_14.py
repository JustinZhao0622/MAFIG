import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    # 检查终点是否为故障点
    if end_point == (9,9):
        end_point = (10,9)
    # 原有的逻辑...
