import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    target_end_point = end_point
    if end_point == (7, 7):
        target_end_point = (8, 7)

    width, height = grid_size

    def heuristic(pos):
        return abs(pos[0] - target_end_point[0]) + abs(pos[1] - target_end_point[1])

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    counter = 0
    heap = [(heuristic(begin_point), counter, begin_point, [begin_point])]
    visited = {begin_point}

    while heap:
        f_score, _, current, path = heapq.heappop(heap)

        if current == target_end_point:
            return path

        for dx, dy in directions:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            if not (0 <= next_x < width and 0 <= next_y < height):
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
        if fid == "Forklift_2":
            continue
        loc = (0, 25)
        if fid == "Forklift_1":
            loc = (27, 44)
        forklifts.append({
            "id": fid,
            "location": loc,
        })
    return forklifts

def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    current_timestamp = time.mktime(start_time)
    for i in range(nums):
        if i > 0:
            if i < 4:
                current_timestamp += 3 * 60
            else:
                current_timestamp += 5 * 60
        arrival_time = time.strftime("%H:%M:%S", time.localtime(current_timestamp))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks
