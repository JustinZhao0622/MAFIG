import heapq
import time
import random

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i == 0:
            loc = (1, 7)
        else:
            loc = (random.randint(0, 3), random.randint(0, 10))
        tractor_resources.append({"id": i, "type": "tractor", "location": loc})
    return tractor_resources

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，前两架间隔3分钟，从第3架开始间隔6分钟，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time_struct = time.strptime(start_time, "%H:%M:%S")
    start_timestamp = time.mktime(start_time_struct)
    planes = []
    current_offset = 0
    for i in range(nums):
        if i == 0:
            interval = 0
        elif i == 1:
            interval = 3
        else:
            interval = 6

        current_offset += interval * 60
        plane_time = time.strftime("%H:%M:%S", time.localtime(start_timestamp + current_offset))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)"""
    width, height = grid_size

    # 突发事件应对：站位(12,7)发生故障，以该点为终点的调整为(13,7)
    actual_end_point = end_point
    if end_point == (12, 7):
        actual_end_point = (13, 7)

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

            if next_pos in visited:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1
            f_score = g_score + heuristic(next_pos)

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i == 0:
            location = (0, 0)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": location})
    return fire_vehicle_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        # 应对突发事件：第1个通用移动资源(id=0)发生故障不可用
        if i == 0:
            status = "unavailable"
        else:
            status = "available"

        mobile_resources.append({
            "id": i, 
            "type": "crane", 
            "location": (random.randint(0, 3), random.randint(0, 10)),
            "status": status
        })
    return mobile_resources

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        if i == 0:
            location = (3, 0)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        towing_tasks.append({"id": i, "type": "towing", "location": location})
    return towing_tasks

def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        if i == 0: # 第1辆维修车(id=0)发生故障不可用，跳过初始化
            continue
        maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return maintenance_vehicle_resources

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        if i == 0:
            loc = (3, 6)
        else:
            loc = (random.randint(0, 3), random.randint(0, 10))
        power_cart_resources.append({"id": i, "type": "power_cart", "location": loc})
    return power_cart_resources
