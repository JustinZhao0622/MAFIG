import heapq
import time
import random

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        if i == 2:
            location = (0, 2)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": location})
    return nitrogen_truck_resources

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)"""
    width, height = grid_size

    # 突发事件处理：定义故障点
    blocked_points = {(4, 6), (5, 6), (4, 7), (5, 7), (9, 7)}

    # 突发事件处理：终点调整
    effective_end_point = end_point
    if end_point == (9, 7):
        effective_end_point = (10, 7)

    def heuristic(pos):
        return abs(pos[0] - effective_end_point[0]) + abs(pos[1] - effective_end_point[1])

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    counter = 0
    heap = [(heuristic(begin_point), counter, begin_point, [begin_point])]
    visited = {begin_point}

    while heap:
        f_score, _, current, path = heapq.heappop(heap)
        if current == effective_end_point:
            return path

        for dx, dy in directions:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            if not (0 <= next_x < width and 0 <= next_y < height):
                continue

            if next_pos in visited:
                continue

            # 突发事件处理：避开故障点
            if next_pos in blocked_points:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1
            f_score = g_score + heuristic(next_pos)

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        if i == 2:  # 第3辆车（索引为2）发生故障不可用，跳过初始化
            continue
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_truck_resources

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        towing_tasks.append({"id": i, "type": "towing", "location": (3, 3) if i == 1 else (random.randint(0, 3), random.randint(0, 10))})
    return towing_tasks

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    current_offset_minutes = 0
    for i in range(nums):
        if i > 0:
            # 从第4架舰载机（索引为3）开始，到达间隔改为6分钟
            if i >= 3:
                current_offset_minutes += 6
            else:
                current_offset_minutes += 3
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + current_offset_minutes * 60))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes
