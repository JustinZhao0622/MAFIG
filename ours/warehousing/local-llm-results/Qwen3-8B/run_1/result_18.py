import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    # 修改end_point为(10,9)如果原为(9,9)
    if end_point == (9,9):
        end_point = (10,9)
    # 原来的逻辑...
