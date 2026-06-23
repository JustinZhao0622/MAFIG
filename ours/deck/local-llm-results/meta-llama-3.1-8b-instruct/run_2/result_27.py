基于突发事件的描述，需要对代码进行以下修改：

1. 第 4 个牵引任务目标站位调整为 (1, 4)。
2. 站位 (9, 8) 发生故障，调整为终点 (10, 8)。
3. 第 4 辆充氧车发生故障不可用。
4. 第 4 辆加氮车初始位置调整为 (0, 8)。
5. 站位 (7, 7)、(8, 7)、(7, 8)、(8, 8) 四个点发生故障。
6. 第 4 个固定保障资源初始位置调整为 (0, 10)。

以下是修改后的代码：


def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        if i == 4:
            towing_tasks.append({"id": i, "type": "towing", "location": (1, 4)})
        else:
            towing_tasks.append({"id": i, "type": "towing", "location": (random.randint(0, 3), random.randint(0, 10))})
    return towing_tasks


def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        if i == 4:
            oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": None})
        else:
            oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_truck_resources


def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        if i == 4:
            nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (0, 8)})
        else:
            nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_truck_resources


def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        if i == 4:
            fixed_resources.append({"id": i, "type": "crane", "location": (0, 10)})
        else:
            fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources


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

    # 站位 (9, 8) 发生故障，调整为终点 (10, 8)
    if begin_point == (9, 8):
        end_point = (10, 8)

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

            # 站位 (7, 7)、(8, 7)、(7, 8)、(8, 8) 四个点发生故障
            if next_pos in [(7, 7), (8, 7), (7, 8), (8, 8)]:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1  # 实际代价
            f_score = g_score + heuristic(next_pos)  # 总评估代价

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None


以上修改仅在 `init_towing_tasks`、`init_oxygen_truck_resources`、`init_nitrogen_truck_resources`、`init_fixed_resources` 和 `route_planning` 函数中进行了修改，以满足突发事件的要求。
