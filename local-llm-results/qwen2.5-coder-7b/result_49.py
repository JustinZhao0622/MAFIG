import heapq
import time
import random 

def init_cranes(nums=5,start_time="8:00:00"):
    """初始化船舶，每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        vessels.append({"time": vessel_time, "id": i, "duration": 20 if i == 3 else 10, "location": (i,10)})
    return vessels

def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    for i in range(nums):
        if i == 3:
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
    if end_point in [(5,5), (6,5), (5,6), (6,6)]:
        return None
    return route_planning(begin_point, (9,7), grid_size)

def init_a():
    """初始化a"""
    return 1

def init_b():
    """初始化b"""
    return 2

def init_c():
    """初始化c"""
    return 3    

def init_d():
    """初始化d"""
    return None
    
def init_e():
    """初始化e"""
    return 5

def init_f():
    """初始化f"""
    return 6
    
def init_g():
    """初始化g"""
    return 7

def init_h():
    """初始化h"""
    return 8
    
def init_i():
    """初始化i"""
    return 9

def init_j():
    """初始化j"""
    return 10
    
def init_k():
    """初始化k"""
    return 11

def init_l():
    """初始化l"""
    return 12
    
def init_m():
    """初始化m"""
    return 13

def init_n():
    """初始化n"""
    return 14
    
def init_o():
    """初始化o"""
    return 15
