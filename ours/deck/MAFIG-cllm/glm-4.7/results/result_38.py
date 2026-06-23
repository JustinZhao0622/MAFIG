import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)"""
    width, height = grid_size

    # 突发事件处理：定义故障点位
    faulty_points = {(6, 6), (7, 6), (6, 7), (7, 7)}

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

            # 跳过故障点位
            if next_pos in faulty_points:
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

def init_hydraulic_cart_resources(nums=10):
    """初始化液压车资源，返回资源列表，每个资源包含id、类型"""
    hydraulic_cart_resources = []
    for i in range(nums):
        if i == 3:
            location = (2, 5)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": location})
    return hydraulic_cart_resources

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i == 3:
            location = (2, 9)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        tractor_resources.append({"id": i, "type": "tractor", "location": location})
    return tractor_resources

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i < 6:
            offset_seconds = 3 * 60 * i
        else:
            # 前6架飞机（索引0-5）在第15分钟到达。
            # 从第7架飞机（索引6）开始，间隔变为8分钟。
            # 计算方式：前6架的总耗时 + (当前架次 - 6) * 8分钟
            # 注意：第7架飞机(i=6)与第6架飞机(i=5)的间隔为8分钟，因此第7架飞机到达时间为 15 + 8 = 23分钟
            offset_seconds = (3 * 5 + 8 * (i - 5)) * 60

        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + offset_seconds))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        if i == 3:
            loc = (3, 8)
        else:
            loc = (random.randint(0, 3), random.randint(0, 10))
        power_cart_resources.append({"id": i, "type": "power_cart", "location": loc})
    return power_cart_resources

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        if i == 5:
            loc = (2, 5)
        else:
            loc = (random.randint(0, 3), random.randint(0, 10))
        towing_tasks.append({"id": i, "type": "towing", "location": loc})
    return towing_tasks

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        if i == 3:
            loc = (0, 5)
        else:
            loc = (random.randint(0, 3), random.randint(0, 10))
        fixed_resources.append({"id": i, "type": "crane", "location": loc})
    return fixed_resources

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        if i == 3:
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources
