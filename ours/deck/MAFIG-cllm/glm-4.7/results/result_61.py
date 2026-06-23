import heapq
import time
import random

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i == 3:
            location = (1, 5)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        tractor_resources.append({"id": i, "type": "tractor", "location": location})
    return tractor_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        resource = {"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))}
        if i == 3:  # 第4个资源（索引为3）发生故障不可用
            resource["status"] = "unavailable"
        mobile_resources.append(resource)
    return mobile_resources

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        location = (random.randint(0, 3), random.randint(0, 10))
        if i == 3:
            oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": location, "status": "fault"})
        else:
            oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": location})
    return oxygen_truck_resources

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        if i == 3:
            loc = (2, 1)
        else:
            loc = (random.randint(0, 3), random.randint(0, 10))
        power_cart_resources.append({"id": i, "type": "power_cart", "location": loc})
    return power_cart_resources

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)"""
    width, height = grid_size

    # 突发事件：故障点设置
    obstacles = {(5, 4), (6, 4), (5, 5), (6, 5), (11, 10)}

    # 突发事件：终点调整
    if end_point == (11, 10):
        end_point = (12, 10)

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

            # 突发事件：避开故障点
            if next_pos in obstacles:
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
        # 突发事件约束：第4辆液压车(id=3)初始位置调整为(2,6)
        if i == 3:
            loc = (2, 6)
        else:
            loc = (random.randint(0, 3), random.randint(0, 10))
        hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": loc})
    return hydraulic_cart_resources
