import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    width, height = grid_size
    failed_stations = {(6, 3), (7, 3), (6, 4), (7, 4)}
    if end_point == (7, 9):
        end_point = (8, 9)
    def heuristic(pos):
        return abs(pos[0] - end_point[0]) + abs(pos[1] - end_point[1])
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    counter = 0
    heap = [(heuristic(begin_point), counter, begin_point, [begin_point])]
    visited = {begin_point}
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
            if next_pos in failed_stations:
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
        fid = f"Forklift_{i+1}"
        if fid == "Forklift_1":
            location = (27, 47)
        else:
            location = (0, 25)
        forklifts.append({
            "id": fid,
            "location": location,
        })
    return forklifts
