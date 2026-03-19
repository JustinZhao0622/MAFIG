import heapq
import time

# 货车到达时间
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
        if i == 2:  # 修改Zone_3的坐标和可用性
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0, 25),
                "current_stock": 41,  # 增加库存
                "max_capacity": 100,
                "desc": f"货物堆积区域{i+1}",
                "available": False  # 不可用
            })
        else:
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0, 25),
                "current_stock": 0,
                "max_capacity": 100,
                "desc": f"货物堆积区域{i+1}",
                "available": True
            })
    return zones

def init_forklifts(nums=3):
    forklifts = []
    for i in range(nums):
        if i == 1:  # 修改Forklift_2的初始位置
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (45, 25),
            })
        else:
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (0, 25),
            })
    return forklifts

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    width, height = grid_size

    # 曼哈顿距离启发式函数
    def heuristic(pos):
        return abs(pos[0] - end_point[0]) + abs(pos[1] - end_point[1])

    # 四个方向：上、下、左、右
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # 优先队列：(f值, 计数器, 当前点, 路径)
    counter = 0
    heap = [(heuristic(begin_point), counter, begin_point, [begin_point])]
    visited = {begin_point}

    while heap:
        f_score, _, current, path = heapq.heappop(heap)

        # 到达终点
        if current == end_point:
            return path

        # 探索四个方向
        for dx, dy in directions:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            # 检查是否在网格范围内
            if not (0 <= next_x < width and 0 <= next_y < height):
                continue

            # 检查是否已访问
            if next_pos in visited:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1  # 实际代价
            f_score = g_score + heuristic(next_pos)  # 总评估代价

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None

# 其他函数保持不变
