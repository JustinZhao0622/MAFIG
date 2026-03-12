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
    return aircrafts

def init_fixed_resources(nums=4):
    resources = []
    for i in range(nums):
        resources.append({
            "id": f"FixedRes_{i+1}",
        })
    return resources

def init_mobile_resources(nums=3):
    mobile_resources = []
    for i in range(nums):
        mobile_resources.append({
            "id": f"Tractor_{i+1}",
        })
    return mobile_resources

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

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1
            f_score = g_score + heuristic(next_pos)

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None

def init_a():
    return 1

def init_b():
    return 2

def init_c():
    return 3    

def init_d():
    return 4
    
def init_e():
    return 5

def init_f():
    return 6
    
def init_g():
    return 7

def init_h():
    return 8
    
def init_i():
    return 9

def init_j():
    return 10
    
def init_k():
    return 11

def init_l():
    return 12
    
def init_m():
    return 13

def init_n():
    return 14
    
def init_o():
    return 15

def init_p():
    return 16

def init_q():
    return 17

def init_r():
    return 18

def init_s():
    return 19

def init_t():
    return 20

def init_u():
    return 21
