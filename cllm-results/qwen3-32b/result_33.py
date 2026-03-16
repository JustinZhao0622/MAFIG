import heapq
import time
import random 

def init_cranes(nums=5,start_time="8:00:00"):
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        vessels.append({"time": vessel_time, "id": i, "duration": 10, "location": (i,10)})
    return vessels

def init_resources(nums=10):
    resources = []
    for i in range(nums):
        resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return resources

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    width, height = grid_size

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
            
            # 处理突发情况：站位故障点不能通行
            fault_points = [(8,9), (3,4), (4,4), (3,5), (4,5)]
            if next_pos in fault_points:
                continue
                
            # 处理突发情况：修改终点为(9,9)
            if current == (8,9):
                end_point = (9,9)

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