基于突发事件的描述，需要对代码进行以下修改：

1. 位置 (6,7)(7,7)(6,8)(7,8) 四个点发生故障，需要将这些点标记为不可用。
2. 位置 (7,9) 发生故障，需要将以该点为终点的调整为 (8,9)。
3. 第 3 个固定保障资源初始位置调整为 (1,3)。
4. 第 3 辆消防车初始位置调整为 (0,8)。
5. 第 3 辆液压车初始位置调整为 (1,1)。

以下是修改后的代码：


import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes


def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        if i == 2:  # 第 3 个固定保障资源初始位置调整为 (1,3)
            fixed_resources.append({"id": i, "type": "crane", "location": (1, 3)})
        else:
            fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        if i == 2:  # 第 3 辆消防车初始位置调整为 (0,8)
            mobile_resources.append({"id": i, "type": "crane", "location": (0, 8)})
        elif i == 3:  # 第 3 辆液压车初始位置调整为 (1,1)
            mobile_resources.append({"id": i, "type": "hydraulic_cart", "location": (1, 1)})
        else:
            mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources


def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)

    参数:
        begin_point: 起点坐标 (x, y)
        end_point: 终点坐标 (x, y)
        grid_size: 地图大小 (width, height)，默认 (100, 100)

    返回:
        包含路径点的列表，每个点为 (x, y) 元组，从起点到终点
        如果没有路径则返回 None
    """
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

    # 将 (7,9) 点标记为不可用
    if end_point == (7, 9):
        end_point = (8, 9)

    # 将 (6,7)(7,7)(6,8)(7,8) 四个点标记为不可用
    for x, y in [(6, 7), (7, 7), (6, 8), (7, 8)]:
        visited.add((x, y))

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


以上修改后的代码将根据突发事件的描述进行了必要的调整，确保系统在当前突发条件下可以正确执行。
