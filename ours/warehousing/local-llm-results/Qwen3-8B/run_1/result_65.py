import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)
    ...
    """
    # 故障点列表
    faulty_points = {(6,5), (7,5), (6,6), (7,6)}
    # 原来的代码...
    while heap:
        f_score, _, current, path = heapq.heappop(heap)
        if current == end_point:
            return path
        for dx, dy in directions:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)
            if not (0 <= next_x < width and 0 <= next_y < height):
                continue
            if next_pos in faulty_points:
                continue  # 跳过故障点
            if next_pos in visited:
                continue
            # 原来的代码...
