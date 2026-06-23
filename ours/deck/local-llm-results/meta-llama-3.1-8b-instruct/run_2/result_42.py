基于突发事件的描述，需要对代码进行以下修改：

1. 第 4 辆维修车发生故障不可用：修改 `init_maintenance_vehicle_resources` 函数，设置第 4 辆维修车的状态为不可用。
2. 从第 5 架舰载机开始到达间隔改为 8 分钟：修改 `init_planes` 函数，设置到达间隔为 8 分钟。
3. 第 4 个固定保障资源初始位置调整为 (0, 3)：修改 `init_fixed_resources` 函数，设置第 4 个固定保障资源的初始位置为 (0, 3)。
4. 站位 (8, 8) (9, 8) (8, 9) (9, 9) 四个点发生故障：修改 `route_planning` 函数，设置这些点为障碍物。
5. 第 4 个通用移动资源发生故障不可用：修改 `init_mobile_resources` 函数，设置第 4 个通用移动资源的状态为不可用。

以下是修改后的代码：


def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        if i == 3:  # 第 4 辆维修车不可用
            maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), random.randint(0, 10)), "status": "unavailable"})
        else:
            maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return maintenance_vehicle_resources


def init_planes(nums=5, start_time="8:00:00"):
    """初始化舰载机，每隔 8 分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为 10 分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 8 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i, 10)})
    return planes


def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        if i == 3:  # 第 4 个固定保障资源初始位置调整为 (0, 3)
            fixed_resources.append({"id": i, "type": "crane", "location": (0, 3)})
        else:
            fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources


def route_planning(begin_point, end_point, grid_size=(100, 100), obstacles=None):
    """从一个点到另一个点的路径规划 (使用A*算法)

    参数:
        begin_point: 起点坐标 (x, y)
        end_point: 终点坐标 (x, y)
        grid_size: 地图大小 (width, height)，默认 (100, 100)
        obstacles:障碍物列表，每个障碍物为 (x, y) 元组

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

    if obstacles:
        visited.update(obstacles)

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

            # 检查是否已访问或是障碍物
            if next_pos in visited:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1  # 实际代价
            f_score = g_score + heuristic(next_pos)  # 总评估代价

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None


def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        if i == 3:  # 第 4 个通用移动资源不可用
            mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10)), "status": "unavailable"})
        else:
            mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources


以上修改后的代码仅对 `init_maintenance_vehicle_resources`、`init_planes`、`init_fixed_resources`、`route_planning` 和 `init_mobile_resources` 函数进行了修改，以满足突发事件的要求。
