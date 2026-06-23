import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    # 调整终点
    if end_point == (9,8):
        end_point = (10,8)
    # 原来的逻辑...
