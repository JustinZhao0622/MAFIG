import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    width, height = grid_size

    if end_point == (9, 7):
        end_point = (10, 7)

    blocked_points = {(4, 3), (5, 3), (4, 4), (5, 4)}

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

            if next_pos in blocked_points:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1
            f_score = g_score + heuristic(next_pos)

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None

def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    for i in range(nums):
        if i != 5:
            resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return resources

def init_cranes(nums=5,start_time="8:00:00"):
    """每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        base_timestamp = time.mktime(start_time) + 3 * 60 * i
        if i == 2:
            base_timestamp += 10 * 60
        vessel_time = time.strftime("%H:%M:%S", time.localtime(base_timestamp))
        duration = 20 if i == 1 else 10
        vessels.append({"time": vessel_time, "id": i, "duration": duration, "location": (i,10)})
    return vessels
