import heapq
import time
import random


def init_planes(nums=5,start_time="8:00:00"):
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes


def init_fixed_resources(nums=10):
    fixed_resources = []
    for i in range(nums):
        if i == 2:
            fixed_resources.append({"id": i, "type": "fixed_support", "location": (2, 0)})
        else:
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
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fuel_truck_resources


def init_nitrogen_truck_resources(nums=10):
    nitrogen_truck_resources = []
    for i in range(nums):
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_truck_resources


def init_oxygen_truck_resources(nums=10):
    oxygen_truck_resources = []
    for i in range(nums):
        if i == 2:
            continue  # 第3辆充氧车故障不可用，跳过初始化
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_truck_resources


def init_power_cart_resources(nums=10):
    power_cart_resources = []
    for i in range(nums):
        if i == 2:
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (0, 3)})  # 第3辆供电车位置调整为(0,3)
        else:
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return power_cart_resources


def init_air_source_car_resources(nums=10):
    air_source_car_resources = []
    for i in range(nums):
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources


def init_hydraulic_cart_resources(nums=10):
    hydraulic_cart_resources = []
    for i in range(nums):
        hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return hydraulic_cart_resources


def init_maintenance_vehicle_resources(nums=10):
    maintenance_vehicle_resources = []
    for i in range(nums):
        if i == 2:
            continue  # 第3辆维修车发生故障不可用，跳过初始化
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
        towing_tasks.append({"id": i, "type": "towing", "location": (random.randint(0, 3), random.randint(0, 10))})
    return towing_tasks


def init_refueling_tasks(nums=6):
    refueling_tasks = []
    for i in range(nums):
        refueling_tasks.append({"id": i, "type": "refueling", "location": (random.randint(0, 3), random.randint(0, 10))})
    return refueling_tasks


def init_nitrogen_filling_tasks(nums=6):
    nitrogen_filling_tasks = []
    for i in range(nums):
        nitrogen_filling_tasks.append({"id": i, "type": "nitrogen_filling", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_filling_tasks


def init_oxygen_filling_tasks(nums=6):
    oxygen_filling_tasks = []
    for i in range(nums):
        if i == 2 and ((random.randint(0, 3), random.randint(0, 10)) == (4, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (4, 9) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 9)):
            continue  # 避开故障点分配任务
        oxygen_filling_tasks.append({"id": i, "type": "oxygen_filling", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_filling_tasks


def init_power_supply_tasks(nums=6):
    power_supply_tasks = []
    for i in range(nums):
        if i == 2 and ((random.randint(0, 3), random.randint(0, 10)) == (4, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (4, 9) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 9)):
            continue  # 避开故障点分配任务
        power_supply_tasks.append({"id": i, "type": "power_supply", "location": (random.randint(0, 3), random.randint(0, 10))})
    return power_supply_tasks


def init_air_supply_tasks(nums=6):
    air_supply_tasks = []
    for i in range(nums):
        if i == 2 and ((random.randint(0, 3), random.randint(0, 10)) == (4, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (4, 9) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 9)):
            continue  # 避开故障点分配任务
        air_supply_tasks.append({"id": i, "type": "air_supply", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_supply_tasks


def init_hydraulic_support_tasks(nums=6):
    hydraulic_support_tasks = []
    for i in range(nums):
        if i == 2 and ((random.randint(0, 3), random.randint(0, 10)) == (4, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (4, 9) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 9)):
            continue  # 避开故障点分配任务
        hydraulic_support_tasks.append({"id": i, "type": "hydraulic_support", "location": (random.randint(0, 3), random.randint(0, 10))})
    return hydraulic_support_tasks


def init_maintenance_tasks(nums=6):
    maintenance_tasks = []
    for i in range(nums):
        if i == 2 and ((random.randint(0, 3), random.randint(0, 10)) == (4, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (4, 9) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 9)):
            continue  # 避开故障点分配任务
        maintenance_tasks.append({"id": i, "type": "maintenance", "location": (random.randint(0, 3), random.randint(0, 10))})
    return maintenance_tasks


def init_inspection_tasks(nums=6):
    inspection_tasks = []
    for i in range(nums):
        if i == 2 and ((random.randint(0, 3), random.randint(0, 10)) == (4, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (4, 9) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 9)):
            continue  # 避开故障点分配任务
        inspection_tasks.append({"id": i, "type": "inspection", "location": (random.randint(0, 3), random.randint(0, 10))})
    return inspection_tasks


def init_fire_watch_tasks(nums=6):
    fire_watch_tasks = []
    for i in range(nums):
        if i == 2 and ((random.randint(0, 3), random.randint(0, 10)) == (4, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (4, 9) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 9)):
            continue  # 避开故障点分配任务
        fire_watch_tasks.append({"id": i, "type": "fire_watch", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_watch_tasks

def init_tasks(nums=6):
    ammo_tasks = []
    for i in range(nums):
        if i == 2 and ((random.randint(0, 3), random.randint(0, 10)) == (4, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 8) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (4, 9) or 
                       (random.randint(0, 3), random.randint(0, 10)) == (5, 9)):
            continue  # 避开故障点分配任务
        ammo_tasks.append({"id": i, "type": "ammo", "location": (random.randint(0, 3), random.randint(0, 10))})
    return ammo_tasks

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

        # 到达终点
        if current == end_point:
            # 检查路径是否经过故障点
            if any(pos in [(4,8),(5,8),(4,9),(5,9)] for pos in path):
                # 如果经过故障点，尝试绕行
                alternative_path = _find_alternative_route(path)
                return alternative_path if alternative_path else None
            return path

        # 探索四个方向
        for dx, dy in directions:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            # 检查是否在网格范围内
            if not (0 <= next_x < width and 0 <= next_y < height):
                continue

            # 检查是否已访问或是否是故障点
            if next_pos in visited or next_pos in [(4,8),(5,8),(4,9),(5,9)]:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1
            f_score = g_score + heuristic(next_pos)

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    
    return None

def _find_alternative_route(original_path):
    """寻找替代路径"""
    # 寻找第一个遇到的故障点
    for i, point in enumerate(original_path):
        if point in [(4,8),(5,8),(4,9),(5,9)]:
            # 尝试从该点前一个位置到终点寻找新路径
            if i > 0:
                new_path_start = original_path[i-1]
                return route_planning(new_path_start, original_path[-1], grid_size=(100, 100))
            break
    return None