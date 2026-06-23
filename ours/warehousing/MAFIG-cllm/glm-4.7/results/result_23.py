import heapq
import time
import random

def init_stacking_zones(nums=4):
    """
    初始化货物堆积区域 (A, B, C, D 区)。
    每个区域包含：坐标、当前存放数量 (current_stock)、最大容量 (max_capacity)。
    返回可用区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    zones = []
    for i in range(nums):
        if i + 1 == 3:
            continue
        zones.append({
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": 0,
            "max_capacity": 100,
            "desc": f"货物堆积区域{i+1}"
        })
    return zones

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    width, height = grid_size

    blocked_points = {(5, 3), (6, 3), (5, 4), (6, 4), (7, 8)}

    actual_end_point = end_point
    if end_point == (7, 8):
        actual_end_point = (8, 8)

    def heuristic(pos):
        return abs(pos[0] - actual_end_point[0]) + abs(pos[1] - actual_end_point[1])

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    counter = 0
    heap = [(heuristic(begin_point), counter, begin_point, [begin_point])]
    visited = {begin_point}

    while heap:
        f_score, _, current, path = heapq.heappop(heap)

        if current == actual_end_point:
            return path

        for dx, dy in directions:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            if not (0 <= next_x < width and 0 <= next_y < height):
                continue

            if next_pos in blocked_points:
                continue

            if next_pos in visited:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1
            f_score = g_score + heuristic(next_pos)

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None

def init_forklifts(nums=3):
    """
    初始化叉车队。
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        f_id = f"Forklift_{i+1}"
        location = (0, 25)
        if f_id == "Forklift_2":
            location = (42, 24)
            # Forklift_2 发生故障不可用，跳过添加到返回列表
            continue
        forklifts.append({
            "id": f_id,
            "location": location,
        })
    return forklifts
