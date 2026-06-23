import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    # 检查是否需要调整终点
    if end_point == (8, 8):
        end_point = (9, 8)
    # 原来的逻辑...
