import heapq
import time
import random

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        location = (random.randint(0, 3), random.randint(0, 10))
        if i == 1:  # 第2辆加氮车（索引为1）初始位置调整为(3,5)
            location = (3, 5)
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": location})
    return nitrogen_truck_resources

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        location = (random.randint(0, 3), random.randint(0, 10))
        if i == 1:
            location = (1, 10)
        power_cart_resources.append({"id": i, "type": "power_cart", "location": location})
    return power_cart_resources

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        if i == 1:
            continue
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fuel_truck_resources

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        # 从第4架舰载机(id=3)开始，到达间隔改为5分钟
        # 前三架(i=0,1,2)间隔3分钟，后续间隔5分钟
        minutes = i * 3
        if i >= 3:
            minutes += (i - 2) * 2

        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + minutes * 60))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        if i == 2:
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)"""
    width, height = grid_size

    # 突发事件应对：处理(10,8)故障，将以该点为终点的调整为(11,8)
    target_end_point = end_point
    if end_point == (10, 8):
        target_end_point = (11, 8)

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
