import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    # 处理终点调整
    if end_point == (9,8):
        end_point = (10,8)
    # 原来的逻辑...
