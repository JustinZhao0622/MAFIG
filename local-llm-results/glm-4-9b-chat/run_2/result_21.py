import heapq
import time
import random

def init_planes(nums=5, start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i >= 3:  # 从第4架舰载机开始，间隔改为8分钟
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 8 * 60 * (i - 3)))
        else:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i, 10)})
    return planes

# 以下函数保持不变，因为没有需要修改的逻辑
def init_fixed_resources(nums=10):
    fixed_resources = []
    for i in range(nums):
        fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources

def init_mobile_resources(nums=10):
    mobile_resources = []
    for i in range(nums):
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources

def init_tractor_resources(nums=10):
    tractor_resources = []
    for i in range(nums):
        tractor_resources.append({"id": i, "type": "tractor", "location": (random.randint(0, 3), random.randint(0, 10))})
    return tractor_resources

def init_fuel_truck_resources(nums=10):
    fuel_truck_resources = []
    for i in range(nums):
        if i == 0:  # 第1辆加油车发生故障不可用
            continue
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fuel_truck_resources

def init_nitrogen_truck_resources(nums=10):
    nitrogen_truck_resources = []
    for i in range(nums):
        if i == 0:  # 第1辆气源车发生故障不可用
            continue
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_truck_resources

def init_oxygen_truck_resources(nums=10):
    oxygen_truck_resources = []
    for i in range(nums):
        if i == 0:  # 第1辆充氧车发生故障不可用
            continue
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_truck_resources

def init_power_cart_resources(nums=10):
    power_cart_resources = []
    for i in range(nums):
        mobile_resources = init_mobile_resources(nums=10)
        for resource in mobile_resources:
            if resource["id"] == 0:  # 第1个通用移动资源发生故障不可用
                continue
            power_cart_resources.append(resource)
    return power_cart_resources

def init_air_source_car_resources(nums=10):
    air_source_car_resources = []
    for i in range(nums):
        if i == 0:  # 第1辆气源车发生故障不可用
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources

def init_hydraulic_cart_resources(nums=10):
    hydraulic_cart_resources = []
    for i in range(nums):
        if i == 0:  # 站位(6,4)(7,4)(6,5)(7,5)四个点发生故障
            continue
        hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return hydraulic_cart_resources

def init_maintenance_vehicle_resources(nums=10):
    maintenance_vehicle_resources = []
    for i in range(nums):
        maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return maintenance_vehicle_resources

def init_fire_vehicle_resources(nums=10):
    fire_vehicle_resources = []
    for i in range(nums):
        fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_vehicle_resources

def init_towing_tasks(nums=6):
    towing_tasks = []
    for i in range(nums):
        if i == 4:  # 第5个牵引任务目标站位调整为(1,2)
            towing_tasks.append({"id": i, "type": "towing", "location": (1, 2)})
        else:
            towing_tasks.append({"id": i, "type": "towing", "location": (random.randint(0, 3), random.randint(0, 10))})
    return towing_tasks

# 以下函数保持不变，因为没有需要修改的逻辑
def route_planning(begin_point, end_point, grid_size=(100, 100)):
    width, height = grid_size
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
