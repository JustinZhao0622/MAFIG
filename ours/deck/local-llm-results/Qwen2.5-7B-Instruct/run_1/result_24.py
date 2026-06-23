import heapq
import time
import random

def init_planes(nums=5, start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes


def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources


def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i != 4:  # 调整第5辆牵引车初始位置
            tractor_resources.append({"id": i, "type": "tractor", "location": (random.randint(0, 3), random.randint(0, 10))})
        else:
            tractor_resources.append({"id": i, "type": "tractor", "location": (0, 3)})
    return tractor_resources


def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        if i != 4:  # 调整第5辆加油车初始位置
            fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
        else:
            fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (1, 7)})
    return fuel_truck_resources


def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_truck_resources


def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        if i == 4:  # 第5辆充氧车发生故障不可用
            continue
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_truck_resources


def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        if i == 4:  # 调整第5辆供电车初始位置
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (1, 7)})
        else:
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return power_cart_resources


def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources


def init_hydraulic_cart_resources(nums=10):
    """初始化液压车资源，返回资源列表，每个资源包含id、类型"""
    hydraulic_cart_resources = []
    for i in range(nums):
        hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return hydraulic_cart_resources


def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return maintenance_vehicle_resources


def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_vehicle_resources


def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        if i == 2:  # 调整第3个牵引任务目标站位
            towing_tasks.append({"id": i, "type": "towing", "location": (2, 8)})
        else:
            towing_tasks.append({"id": i, "type": "towing", "location": (random.randint(0, 3), random.randint(0, 10))})
    return towing_tasks


def init_refueling_tasks(nums=6):
    """初始化加油任务，返回任务列表，每个任务包含id、类型"""
    refueling_tasks = []
    for i in range(nums):
        refueling_tasks.append({"id": i, "type": "refueling", "location": (random.randint(0, 3), random.randint(0, 10))})
    return refueling_tasks


def init_nitrogen_filling_tasks(nums=6):
    """初始化加氮任务，返回任务列表，每个任务包含id、类型"""
    nitrogen_filling_tasks = []
    for i in range(nums):
        nitrogen_filling_tasks.append({"id": i, "type": "nitrogen_filling", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_filling_tasks


def init_oxygen_filling_tasks(nums=6):
    """初始化充氧任务，返回任务列表，每个任务包含id、类型"""
    oxygen_filling_tasks = []
    for i in range(nums):
        oxygen_filling_tasks.append({"id": i, "type": "oxygen_filling", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_filling_tasks


def init_power_supply_tasks(nums=6):
    """初始化供电任务，返回任务列表，每个任务包含id、类型"""
    power_supply_tasks = []
    for i in range(nums):
        power_supply_tasks.append({"id": i, "type": "power_supply", "location": (random.randint(0, 3), random.randint(0, 10))})
    return power_supply_tasks


def init_air_supply_tasks(nums=6):
    """初始化供气任务，返回任务列表，每个任务包含id、类型"""
    air_supply_tasks = []
    for i in range(nums):
        air_supply_tasks.append({"id": i, "type": "air_supply", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_supply_tasks


def init_hydraulic_support_tasks(nums=6):
    """初始化液压保障任务，返回任务列表，每个任务包含id、类型"""
    hydraulic_support_tasks = []
    for i in range(nums):
        hydraulic_support_tasks.append({"id": i, "type": "hydraulic_support", "location": (random.randint(0, 3), random.randint(0, 10))})
    return hydraulic_support_tasks


def init_maintenance_tasks(nums=6):
    """初始化维修保障任务，返回任务列表，每个任务包含id、类型"""
    maintenance_tasks = []
    for i in range(nums):
        maintenance_tasks.append({"id": i, "type": "maintenance", "location": (random.randint(0, 3), random.randint(0, 10))})
    return maintenance_tasks


def init_inspection_tasks(nums=6):
    """初始化检查任务，返回任务列表，每个任务包含id、类型"""
    inspection_tasks = []
    for i in range(nums):
        inspection_tasks.append({"id": i, "type": "inspection", "location": (random.randint(0, 3), random.randint(0, 10))})
    return inspection_tasks


def init_fire_watch_tasks(nums=6):
    """初始化消防监护任务，返回任务列表，每个任务包含id、类型"""
    fire_watch_tasks = []
    for i in range(nums):
        fire_watch_tasks.append({"id": i, "type": "fire_watch", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_watch_tasks

def init_tasks(nums=6):
    """初始化挂载弹药任务，返回任务列表，每个任务包含id、类型"""
    ammo_tasks = []
    for i in range(nums):
        ammo_tasks.append({"id": i, "type": "ammo", "location": (random.randint(0, 3), random.randint(0, 10))})
    return ammo_tasks

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)

    参数:
        begin_point: 起点坐标 (x, y)
        end_point: 终点坐标 (x, y)
        grid_size: 地图大小 (width, height)，默认 (100, 100)

    返回:
        包含路径点的列表，每个点为 (x, y) 元组，从起点到终点
        如果没有路径则返回 None
    """
    width, height = grid_size

    # 曼哈顿距离启发式函数
    def heuristic(pos):
        return abs(pos[0] - end_point[0]) + abs(pos[1] - end_point[1])

    # 四个方向：上、下、左、右
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # 优先队列：(f值, 计数器, 当前点, 路径)
    counter = 0
    heap = [(heuristic(begin_point), counter, begin_point, [begin_point])]
    visited = {begin_point}

    while heap:
        f_score, _, current, path = heapq.heappop(heap)

        # 到达终点
        if current == end_point:
            return path

        # 探索四个方向
        for dx, dy in directions:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            # 检查是否在网格范围内
            if not (0 <= next_x < width and 0 <= next_y < height):
                continue

            # 检查是否已访问
            if next_pos in visited:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1  # 实际代价
            f_score = g_score + heuristic(next_pos)  # 总评估代价

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None
