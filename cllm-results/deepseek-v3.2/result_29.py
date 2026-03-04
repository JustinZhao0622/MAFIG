import heapq
import time
import random 

def init_cranes(nums=5,start_time="8:00:00"):
    """初始化船舶，每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        duration = 10
        if i == 3:
            duration = 20
        vessels.append({"time": vessel_time, "id": i, "duration": duration, "location": (i,10)})
    return vessels

def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    for i in range(nums):
        if i == 4:
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
    faulty_points = {(6,3),(7,3),(6,4),(7,4)}

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

            if next_pos in faulty_points:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1
            f_score = g_score + heuristic(next_pos)

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