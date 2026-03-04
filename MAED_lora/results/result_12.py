import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)

    参数:
        begin_point: 起点坐标
        end_point: 终点坐标
        grid_size: 地图大小，默认 (100, 100)

    返回:
        包含路径点的列表，每个点为 元组，从起点到终点
        如果没有路径则返回 None
    """
    # 突发事件处理：终点调整
    if end_point == (9, 9):
        end_point = (10, 9)

    # 突发事件处理：故障点集合
    faulty_stations = {(9, 9), (5, 4), (6, 4), (5, 5), (6, 5)}

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

            # 检查是否为故障点
            if next_pos in faulty_stations:
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

def init_cranes(nums=5,start_time="8:00:00"):
    """每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        delay = 0
        if i == 0:
            delay = 10 * 60
        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i + delay))
        vessels.append({"time": vessel_time, "id": i, "duration": 10, "location": (i,10)})
    return vessels

