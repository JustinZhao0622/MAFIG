import heapq
import time

def init_aircraft_arrival(nums=10, start_time="8:00:00"):
    start_time = time.strptime(start_time, "%H:%M:%S")
    aircrafts = []
    for i in range(nums):
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        aircrafts.append({
            "id": f"Aircraft_{i}",
            "arrival_time": arrival_time,
        })
    # Aircraft_2延迟5分钟到达
    if nums > 2:
        original_arrival = aircrafts[2]["arrival_time"]
        # 将时间转换为秒数并+5分钟后再转回格式化时间
        aircrafts[2]["arrival_time"] = time.strftime("%H:%M:%S", time.localtime(time.mktime(time.strptime(original_arrival, "%H:%M:%S")) + 5 * 60))
    return aircrafts

def init_fixed_resources(nums=4):
    resources = []
    for i in range(nums):
        if i == 3:  # FixedRes_4损坏不可用
            continue
        resources.append({
            "id": f"FixedRes_{i+1}",
        })
    return resources

def init_mobile_resources(nums=3):
    mobile_resources = []
    for i in range(nums):
        if i == 0:  # Tractor_1牵引车损坏不可用
            continue
        mobile_resources.append({
            "id": f"Tractor_{i+1}",
        })
    return mobile_resources

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    width, height = grid_size

    def heuristic(pos):
        return abs(pos[0] - end_point[0]) + abs(pos[1] - end_point[1])

    def is_blocked(point):
        # 故障点列表：(7,8); (6,5)(7,5)(6,6)(7,6)
        blocked_points = [(7,8), (6,5), (7,5), (6,6), (7,6)]
        if point in blocked_points:
            return True
        return False

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    counter = 0
    heap = [(heuristic(begin_point), counter, begin_point, [begin_point])]
    visited = {begin_point}

    while heap:
        f_score, _, current, path = heapq.heappop(heap)

        # 到达终点
        if current == end_point:
            return path

        # 如果当前点是故障点(7,8)，则终点调整为(8,8)
        if current == (7,8):
            end_point = (8,8)

        # 探索四个方向
        for dx, dy in directions:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            # 检查是否在网格范围内
            if not (0 <= next_x < width and 0 <= next_y < height):
                continue

            # 检查是否已访问或是否是故障点
            if next_pos in visited or is_blocked(next_pos):
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1
            f_score = g_score + heuristic(next_pos)

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None

def init_a():
    a = 1
    return a

def init_b():
    b = 2
    return b

def init_c():
    c = 3
    return c    

def init_d():
    d = 4
    return d
    
def init_e():
    e = 5
    return e

def init_f():
    f = 6
    return f
    
def init_g():
    g = 7
    return g

def init_h():
    h = 8
    return h
    
def init_i():
    i = 9
    return i

def init_j():
    j = 10
    return j
    
def init_k():
    k = 11
    return k

def init_l():
    l = 12
    return l
    
def init_m():
    m = 13
    return m

def init_n():
    n = 14
    return n
    
def init_o():
    o = 15
    return o

def init_p():
    p = 16
    return p

def init_q():
    q = 17
    return q

def init_r():
    r = 18
    return r

def init_s():
    s = 19
    return s

def init_t():
    t = 20
    return t

def init_u():
    u = 21
    return u