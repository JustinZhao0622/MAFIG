import heapq
import time
import random 

def init_cranes(nums=5,start_time="8:00:00"):
    """初始化船舶，每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        delay = 10 if i == 0 else 0
        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i + delay * 60))
        vessels.append({"time": vessel_time, "id": i, "duration": 10, "location": (i,10)})
    return vessels

def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    unavailable_ids = {8}
    for i in range(nums):
        if i in unavailable_ids:
            continue
        resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return resources

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

    fault_points = {(6,3), (7,3), (6,4), (7,4)}
    adjusted_end_point = (8, 8) if end_point == (7, 8) else end_point
    
    def heuristic(pos):
        return abs(pos[0] - adjusted_end_point[0]) + abs(pos[1] - adjusted_end_point[1])

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    counter = 0
    heap = [(heuristic(begin_point), counter, begin_point, [begin_point])]
    visited = {begin_point}

    while heap:
        f_score, _, current, path = heapq.heappop(heap)

        if current == adjusted_end_point:
            return path

        for dx, dy in directions:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            if not (0 <= next_x < width and 0 <= next_y < height):
                continue

            if next_pos in visited or next_pos in fault_points:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1
            f_score = g_score + heuristic(next_pos)

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None


def init_trucks(nums=8):
    """初始化集卡车队，返回车辆列表，每辆车包含id、位置、状态"""
    trucks = []
    for i in range(nums):
        trucks.append({
            "id": f"Truck_{i+1}",
            "location": (random.randint(0, 20), random.randint(0, 20)),
            "status": "idle",
        })
    return trucks


def init_yard_blocks(nums=6):
    """初始化堆场区块，返回区块列表，每个区块包含id、容量、当前占用"""
    yard_blocks = []
    for i in range(nums):
        yard_blocks.append({
            "id": f"Block_{i+1}",
            "capacity": 100,
            "occupied": random.randint(0, 60),
        })
    return yard_blocks


def init_berths(nums=4):
    """初始化泊位，返回泊位列表，每个泊位包含id、位置、状态"""
    berths = []
    for i in range(nums):
        berths.append({
            "id": f"Berth_{i+1}",
            "location": (i * 10, 0),
            "status": "available",
        })
    return berths


def init_containers(nums=12):
    """初始化集装箱，返回集装箱列表，每个集装箱包含id、位置、类型"""
    containers = []
    for i in range(nums):
        containers.append({
            "id": f"Container_{i+1}",
            "location": (random.randint(0, 10), random.randint(0, 10)),
            "type": "general",
        })
    return containers


def init_loading_tasks(nums=10):
    """初始化装卸任务，返回任务列表，每个任务包含id、目标资源、状态"""
    loading_tasks = []
    for i in range(nums):
        loading_tasks.append({
            "id": f"Task_{i+1}",
            "target": f"Container_{(i % 12) + 1}",
            "status": "waiting",
        })
    return loading_tasks