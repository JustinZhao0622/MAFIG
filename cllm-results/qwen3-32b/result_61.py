import heapq
import time

# 货车到达时间
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    for i in range(nums):
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks

def init_stacking_zones(nums=4):
    """
    初始化货物堆积区域 (A, B, C, D 区)。
    每个区域包含：坐标、当前存放数量 (current_stock)、最大容量 (max_capacity)。
    返回可用区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    zones = []
    for i in range(nums):
        # Zone_1 堆积区最大容量缩减至146
        if i == 0:
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 146,
                "desc": f"货物堆积区域{i+1}"
            })
        elif i == 2:
            # Zone_3 堆积区发生故障不可用
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 0,
                "desc": f"货物堆积区域{i+1}"
            })
        else:
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 100,
                "desc": f"货物堆积区域{i+1}"
            })
    return zones

def init_forklifts(nums=3):
    """
    初始化叉车队。
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": (0, 25),
        })
    return forklifts

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

    # 故障点集合
    faulty_points = {(8,7), (4,6), (5,6), (4,7), (5,7)}
    
    # 如果终点是(8,7)，则改为(9,7)
    if end_point == (8,7):
        end_point = (9,7)
        
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
                
            # 检查是否为故障点
            if next_pos in faulty_points:
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

def init_a():
    """初始化a"""
    a = 1
    return a

def init_b():
    """初始化b"""
    b = 2
    return b

def init_c():
    """初始化c"""
    c = 3
    return c    

def init_d():
    """初始化d"""
    d = 4
    return d
    
def init_e():
    """初始化e"""
    e = 5
    return e

def init_f():
    """初始化f"""
    f = 6
    return f
    
def init_g():
    """初始化g"""
    g = 7
    return g

def init_h():
    """初始化h"""
    h = 8
    return h
    
def init_i():
    """初始化i"""
    i = 9
    return i

def init_j():
    """初始化j"""
    j = 10
    return j
    
def init_k():
    """初始化k"""
    k = 11
    return k

def init_l():
    """初始化l"""
    l = 12
    return l
    
def init_m():
    """初始化m"""
    m = 13
    return m

def init_n():
    """初始化n"""
    n = 14
    return n
    
def init_o():
    """初始化o"""
    o = 15
    return o