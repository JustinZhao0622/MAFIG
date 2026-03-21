import heapq
import time

def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    for i in range(nums):
        interval_minutes = 3 if i < 5 else 5
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + interval_minutes * 60 * i))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks

def init_stacking_zones(nums=4):
    zones = []
    for i in range(nums):
        zone = {
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": 0,
            "max_capacity": 100,
            "desc": f"货物堆积区域{i+1}"
        }
        if i == 1:
            zone["max_capacity"] = 141
        zones.append(zone)
    return zones

def init_forklifts(nums=3):
    forklifts = []
    for i in range(nums):
        location = (0, 25)
        if i == 0:
            location = (26, 32)
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": location,
        })
    return forklifts

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    width, height = grid_size
    def is_blocked(pos):
        blocked_positions = [(3,3), (4,3), (3,4), (4,4)]
        return pos in blocked_positions
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
            if is_blocked(next_pos):
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