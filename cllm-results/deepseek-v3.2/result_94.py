import heapq
import time

def init_truck_arrival_time(nums=10, start_time="8:00:00"):
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
    zones = []
    for i in range(nums):
        if i == 1:
            continue
        zones.append({
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": 0,
            "max_capacity": 100,
            "desc": f"货物堆积区域{i+1}"
        })
    return zones

def init_forklifts(nums=3):
    forklifts = []
    for i in range(nums):
        loc = (0, 25)
        if i == 2:
            loc = (19, 20)
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": loc,
        })
    return forklifts

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    width, height = grid_size
    def heuristic(pos):
        return abs(pos[0] - end_point[0]) + abs(pos[1] - end_point[1])
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    counter = 0
    heap = [(heuristic(begin_point), counter, begin_point, [begin_point])]
    visited = {begin_point}
    fault_points = {(6,4),(7,4),(6,5),(7,5)}
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
            if next_pos in fault_points:
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