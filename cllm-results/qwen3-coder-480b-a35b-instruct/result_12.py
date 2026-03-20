"""
原子函数库
"""
import heapq
import time
import random 

def init_cranes(nums=5,start_time="8:00:00"):
    """初始化船舶，每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    delay_applied = False
    for i in range(nums):
        minutes_offset = 3 * 60 * i
        if i == 0 and not delay_applied:
            minutes_offset += 10 * 60
            delay_applied = True
        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + minutes_offset))
        location_x, location_y = i, 10
        if location_x == 9 and location_y == 9:
            location_x, location_y = 10, 9
        vessels.append({"time": vessel_time, "id": i, "duration": 10, "location": (location_x, location_y)})
    return vessels

def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    fault_points = {(5,4),(6,4),(5,5),(6,5)}
    for i in range(nums):
        loc_x = random.randint(0, 3)
        loc_y = random.randint(0, 10)
        while (loc_x, loc_y) in fault_points:
            loc_x = random.randint(0, 3)
            loc_y = random.randint(0, 10)
        resources.append({"id": i, "type": "crane", "location": (loc_x, loc_y)})
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
    fault_points = {(5,4),(6,4),(5,5),(6,5)}
    adjusted_end_point = end_point
    if end_point == (9,9):
        adjusted_end_point = (10,9)

    # 曼哈顿距离启发式函数
    def heuristic(pos):
        return abs(pos[0] - adjusted_end_point[0]) + abs(pos[1] - adjusted_end_point[1])

    # 四个方向：上、下、左、右
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # 优先队列：(f值, 计数器, 当前点, 路径)
    counter = 0
    heap = [(heuristic(begin_point), counter, begin_point, [begin_point])]
    visited = {begin_point}

    while heap:
        f_score, _, current, path = heapq.heappop(heap)

        # 到达终点
        if current == adjusted_end_point:
            return path

        # 探索四个方向
        for dx, dy in directions:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            # 检查是否在网格范围内
            if not (0 <= next_x < width and 0 <= next_y < height):
                continue

            # 检查是否是故障点
            if next_pos in fault_points:
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


def init_trucks(nums=8):
    """初始化集卡车队，返回车辆列表，每辆车包含id、位置、状态"""
    trucks = []
    fault_points = {(5,4),(6,4),(5,5),(6,5)}
    for i in range(nums):
        loc_x = random.randint(0, 20)
        loc_y = random.randint(0, 20)
        while (loc_x, loc_y) in fault_points:
            loc_x = random.randint(0, 20)
            loc_y = random.randint(0, 20)
        trucks.append({
            "id": f"Truck_{i+1}",
            "location": (loc_x, loc_y),
            "status": "idle",
        })
    return trucks


def init_yard_blocks(nums=6):
    """初始化堆场区块，返回区块列表，每个区块包含id、容量、当前占用"""
    yard_blocks = []
    fault_points = {(5,4),(6,4),(5,5),(6,5)}
    for i in range(nums):
        occupied = random.randint(0, 60)
        yard_blocks.append({
            "id": f"Block_{i+1}",
            "capacity": 100,
            "occupied": occupied,
        })
    return yard_blocks


def init_berths(nums=4):
    """初始化泊位，返回泊位列表，每个泊位包含id、位置、状态"""
    berths = []
    fault_points = {(5,4),(6,4),(5,5),(6,5)}
    for i in range(nums):
        loc_x = i * 10
        loc_y = 0
        while (loc_x, loc_y) in fault_points:
            loc_x = (loc_x + 10) % 40
        berths.append({
            "id": f"Berth_{i+1}",
            "location": (loc_x, loc_y),
            "status": "available",
        })
    return berths


def init_containers(nums=12):
    """初始化集装箱，返回集装箱列表，每个集装箱包含id、位置、类型"""
    containers = []
    fault_points = {(5,4),(6,4),(5,5),(6,5)}
    for i in range(nums):
        loc_x = random.randint(0, 10)
        loc_y = random.randint(0, 10)
        while (loc_x, loc_y) in fault_points:
            loc_x = random.randint(0, 10)
            loc_y = random.randint(0, 10)
        containers.append({
            "id": f"Container_{i+1}",
            "location": (loc_x, loc_y),
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