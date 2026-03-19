import heapq
import time

# 货车到达时间
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    for i in range(nums):
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks

# 初始化货物堆积区域 (A, B, C, D 区)。
def init_stacking_zones(nums=4):
    """
    每个区域包含：坐标、当前存放数量 (current_stock)、最大容量 (max_capacity)。
    返回可用区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    zones = []
    for i in range(nums):
        zones.append({
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": 0,
            "max_capacity": 100,
            "desc": f"货物堆积区域{i+1}"
        })
    # 根据突发事件，Zone_3堆积区当前库存增加65
    zones[2]["current_stock"] += 65
    return zones

# 初始化叉车队。
def init_forklifts(nums=3):
    """
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": (0, 25),
        })
    return forklifts

# 从一个点到另一个点的路径规划 (使用A*算法)
def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """ 
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

# 初始化装货月台。
def init_loading_docks(nums=4):
    """
    返回月台列表，每个月台包含id、位置、状态
    """
    docks = []
    for i in range(nums):
        docks.append({
            "id": f"Dock_{i+1}",
            "location": (i * 5, 0),
            "status": "idle",
        })
    return docks

# 初始化卸货月台。
def init_unloading_docks(nums=4):
    """
    返回月台列表，每个月台包含id、位置、状态
    """
    docks = []
    for i in range(nums):
        docks.append({
            "id": f"UnloadDock_{i+1}",
            "location": (i * 5, 5),
            "status": "idle",
        })
    return docks

# 初始化货架。
def init_shelves(nums=10):
    """
    返回货架列表，每个货架包含id、位置、容量
    """
    shelves = []
    for i in range(nums):
        shelves.append({
            "id": f"Shelf_{i+1}",
            "location": (i % 5, i // 5),
            "capacity": 50,
        })
    return shelves

# 初始化分拣台。
def init_sorting_stations(nums=3):
    """
    返回分拣台列表，每个分拣台包含id、位置、状态
    """
    stations = []
    for i in range(nums):
        stations.append({
            "id": f"SortStation_{i+1}",
            "location": (10, i * 3),
            "status": "idle",
        })
    return stations

# 初始化仓储作业人员。
def init_workers(nums=6):
    """
    返回人员列表，每个人员包含id、岗位、状态
    """
    workers = []
    for i in range(nums):
        workers.append({
            "id": f"Worker_{i+1}",
            "role": "operator",
            "status": "available",
        })
    return workers

# 初始化托盘。
def init_pallets(nums=20):
    """
    返回托盘列表，每个托盘包含id、位置、载重
    """
    pallets = []
    for i in range(nums):
        pallets.append({
            "id": f"Pallet_{i+1}",
            "location": (i % 5, i // 5),
            "max_weight": 1000,
        })
    return pallets

# 初始化订单。
def init_orders(nums=8):
    """
    返回订单列表，每个订单包含id、货物数量、状态
    """
    orders = []
    for i in range(nums):
        orders.append({
            "id": f"Order_{i+1}",
            "item_count": 10,
            "status": "pending",
        })
    return orders

# 初始化库存记录。
def init_inventory_records(nums=10):
    """
    返回库存记录列表，每条记录包含id、sku、数量
    """
    records = []
    for i in range(nums):
        records.append({
            "id": f"Inventory_{i+1}",
            "sku": f"SKU_{i+1}",
            "quantity": 100,
        })
    return records

# 初始化传送带。
def init_conveyors(nums=2):
    """
    返回传送带列表，每条传送带包含id、长度、状态
    """
    conveyors = []
    for i in range(nums):
        conveyors.append({
            "id": f"Conveyor_{i+1}",
            "length": 20,
            "status": "running",
        })
    return conveyors

# 初始化拣货任务。
def init_picking_tasks(nums=6):
    """
    返回任务列表，每个任务包含id、目标货架、状态
    """
    tasks = []
    for i in range(nums):
        tasks.append({
            "id": f"PickTask_{i+1}",
            "target_shelf": f"Shelf_{(i % 5) + 1}",
            "status": "waiting",
        })
    return tasks

# 初始化发货任务。
def init_shipping_tasks(nums=6):
    """
    返回任务列表，每个任务包含id、目标月台、状态
    """
    tasks = []
    for i in range(nums):
        tasks.append({
            "id": f"ShipTask_{i+1}",
            "target_dock": f"Dock_{(i % 4) + 1}",
            "status": "waiting",
        })
    return tasks

# 根据突发事件，站位(9,9)发生故障，调整为(10,9)
def adjust_station_location(stations):
    for station in stations:
        if station["location"] == (9, 9):
            station["location"] = (10, 9)
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status2(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status3(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status4(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status5(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status6(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status7(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status8(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status9(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status10(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status11(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status12(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status13(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status14(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status15(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status16(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status17(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status18(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status19(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status20(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status21(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status22(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status23(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status24(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status25(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status26(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status27(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status28(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status29(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status30(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status31(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station_status32(stations):
    for station in stations:
        if station["location"] in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            station["status"] = "faulty"
    return stations

# 根据突发事件，站位(3,3)(4,3)(3,4)(4,4)四个点发生故障
def adjust_station
