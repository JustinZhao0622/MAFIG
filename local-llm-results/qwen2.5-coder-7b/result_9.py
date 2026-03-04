import heapq
import time
import random 

def init_cranes(nums=5,start_time="8:00:00"):
    """初始化船舶，每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        vessels.append({"time": vessel_time, "id": i, "duration": 10, "location": (i,10)})
    # 第0艘到达的船舶延迟10分钟到达
    vessels[0]["time"] = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * 10))
    return vessels

def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    for i in range(nums):
        # 站位(6,3)(7,3)(6,4)(7,4)四个点发生故障
        if (6, 3) != (i // 5, i % 5) and (7, 3) != (i // 5, i % 5) and (6, 4) != (i // 5, i % 5) and (7, 4) != (i // 5, i % 5):
            resources.append({"id": i, "type": "crane", "location": (i // 5, i % 5)})
    return resources

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
