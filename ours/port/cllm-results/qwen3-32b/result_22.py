import heapq
import time
import random 

def init_cranes(nums=5,start_time="8:00:00"):
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        if i == 2:
            vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + (3 * 60 * i) + 10 * 60))
        duration = 10
        if i == 1:
            duration = 20
        vessels.append({"time": vessel_time, "id": i, "duration": duration, "location": (i,10)})
    return vessels

def init_resources(nums=10):
    resources = []
    for i in range(nums):
        if i == 2:
            continue
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

    blocked_positions = {(4,6),(5,6),(4,7),(5,7)}
    
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

            if next_pos in visited or next_pos in blocked_positions:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1  
            f_score = g_score + heuristic(next_pos)  

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None


def init_trucks(nums=8):
    trucks = []
    for i in range(nums):
        trucks.append({
            "id": f"Truck_{i+1}",
            "location": (random.randint(0, 20), random.randint(0, 20)),
            "status": "idle",
        })
    return trucks


def init_yard_blocks(nums=6):
    yard_blocks = []
    for i in range(nums):
        yard_blocks.append({
            "id": f"Block_{i+1}",
            "capacity": 100,
            "occupied": random.randint(0, 60),
        })
    return yard_blocks


def init_berths(nums=4):
    berths = []
    for i in range(nums):
        berths.append({
            "id": f"Berth_{i+1}",
            "location": (i * 10, 0),
            "status": "available",
        })
    return berths


def init_containers(nums=12):
    containers = []
    for i in range(nums):
        containers.append({
            "id": f"Container_{i+1}",
            "location": (random.randint(0, 10), random.randint(0, 10)),
            "type": "general",
        })
    return containers


def init_loading_tasks(nums=10):
    loading_tasks = []
    for i in range(nums):
        loading_tasks.append({
            "id": f"Task_{i+1}",
            "target": f"Container_{(i % 12) + 1}",
            "status": "waiting",
        })
    return loading_tasks