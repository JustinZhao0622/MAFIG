import heapq
import time
import random

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        location = (random.randint(0, 3), random.randint(0, 10))
        if i == 2:  # 第3辆加氮车（索引为2）
            location = (0, 5)
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": location})
    return nitrogen_truck_resources

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        location = (random.randint(0, 3), random.randint(0, 10))
        if i == 2:
            location = (0, 5)
        fixed_resources.append({"id": i, "type": "crane", "location": location})
    return fixed_resources

def init_hydraulic_cart_resources(nums=10):
    """初始化液压车资源，返回资源列表，每个资源包含id、类型"""
    hydraulic_cart_resources = []
    for i in range(nums):
        if i == 2:
            location = (1, 9)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": location})
    return hydraulic_cart_resources

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        # 基础资源信息
        resource = {
            "id": i,
            "type": "fuel_truck",
            "location": (random.randint(0, 3), random.randint(0, 10))
        }

        # 应对突发事件：第3辆加油车发生故障不可用
        if i == 3:
            resource["status"] = "unavailable"
        else:
            resource["status"] = "available"

        fuel_truck_resources.append(resource)
    return fuel_truck_resources

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        location = (random.randint(0, 3), random.randint(0, 10))
        if i == 2:
            location = (3, 2)
        power_cart_resources.append({"id": i, "type": "power_cart", "location": location})
    return power_cart_resources

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        if i == 3:
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)"""
    # 突发事件处理：如果终点是故障点(7,8)，则调整为(8,8)
    if end_point == (7, 8):
        end_point = (8, 8)

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
