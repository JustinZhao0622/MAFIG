import heapq
import time
import random

def init_stacking_zones(nums=4):
    zones = []
    for i in range(nums):
        zone_data = {
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": 0,
            "max_capacity": 100,
            "desc": f"货物堆积区域{i+1}"
        }
        if i == 1:
            zone_data["max_capacity"] = 115
            zone_data["current_stock"] = 33
        zones.append(zone_data)
    return zones

def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    parsed_start_time = time.strptime(start_time, "%H:%M:%S")
    current_timestamp = time.mktime(parsed_start_time)
    trucks = []
    for i in range(nums):
        arrival_time = time.strftime("%H:%M:%S", time.localtime(current_timestamp))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
        if i >= 4:
            current_timestamp += 6 * 60
        else:
            current_timestamp += 3 * 60
    return trucks

def init_forklifts(nums=3):
    """
    初始化叉车队。
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        loc = (0, 25)
        if i == 0:
            loc = (36, 14)
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": loc,
        })
    return forklifts

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    width, height = grid_size

    if end_point == (8, 7):
        end_point = (9, 7)

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

            if next_pos in visited:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1
            f_score = g_score + heuristic(next_pos)

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None
