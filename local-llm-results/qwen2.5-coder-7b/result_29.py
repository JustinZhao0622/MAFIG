import heapq
import time

def init_aircraft_arrival(nums=10, start_time="8:00:00"):
    aircrafts = []
    for i in range(nums):
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(time.strptime(start_time, "%H:%M:%S")) + 3 * 60 * i))
        aircrafts.append({
            "id": f"Aircraft_{i}",
            "arrival_time": arrival_time,
        })
    return aircrafts

def init_fixed_resources(nums=4):
    resources = []
    for i in range(nums):
        if i == 1:  # FixedRes_2损坏不可用
            continue
        resources.append({
            "id": f"FixedRes_{i+1}",
        })
    return resources

def init_mobile_resources(nums=3):
    mobile_resources = []
    for i in range(nums):
        if i == 0:  # Tractor_2损坏不可用
            continue
        mobile_resources.append({
            "id": f"Tractor_{i+1}",
        })
    return mobile_resources

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    if end_point == (8, 9):  # 站位(8,9)发生故障,以该点为终点的调整为(9,9)
        end_point = (9, 9)
    width, height = grid_size
    counter = 0
    heap = [(abs(begin_point[0] - end_point[0]) + abs(begin_point[1] - end_point[1]), counter, begin_point, [begin_point])]
    visited = {begin_point}
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    while heap:
        _, _, current, path = heapq.heappop(heap)
        if current == end_point:
            return path
        for dx, dy in directions:
            next_x, next_y = current[0] + dx, current[1] + dy
            next_pos = (next_x, next_y)
            if not (0 <= next_x < width and 0 <= next_y < height):
                continue
            if next_pos in visited:
                continue
            visited.add(next_pos)
            new_path = path + [next_pos]
            heapq.heappush(heap, (len(new_path) - 1 + abs(next_pos[0] - end_point[0]) + abs(next_pos[1] - end_point[1]), counter, next_pos, new_path))
    return None

def init_a():  # 初始化a
    a = 1
    return a

def init_b():  # 初始化b
    b = 2
    return b

def init_c():  # 初始化c
    c = 3
    return c    

def init_d():  # 初始化d
    d = 4
    return d
    
def init_e():  # 初始化e
    e = 5
    return e

def init_f():  # 初始化f
    f = 6
    return f
    
def init_g():  # 初始化g
    g = 7
    return g

def init_h():  # 初始化h
    h = 8
    return h
    
def init_i():  # 初始化i
    i = 9
    return i

def init_j():  # 初始化j
    j = 10
    return j
    
def init_k():  # 初始化k
    k = 11
    return k

def init_l():  # 初始化l
    l = 12
    return l
    
def init_m():  # 初始化m
    m = 13
    return m

def init_n():  # 初始化n
    n = 14
    return n
    
def init_o():  # 初始化o
    o = 15
    return o

def init_p():  # 初始化p
    p = 16
    return p

def init_q():  # 初始化q
    q = 17
    return q

def init_r():  # 初始化r
    r = 18
    return r

def init_s():  # 初始化s
    s = 19
    return s

def init_t():  # 初始化t
    t = 20
    return t

def init_u():  # 初始化u
    u = 21
    return u
