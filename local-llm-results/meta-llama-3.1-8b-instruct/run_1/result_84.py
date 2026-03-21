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

def init_stacking_zones(nums=4):
    """
    初始化货物堆积区域 (A, B, C, D 区)。
    每个区域包含：坐标、当前存放数量 (current_stock)、最大容量 (max_capacity)。
    返回可用区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    zones = []
    for i in range(nums):
        if i == 2:  # Zone_3堆积区发生故障不可用
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 0,  # 故障不可用
                "desc": f"货物堆积区域{i+1}故障不可用"
            })
        else:
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 100,
                "desc": f"货物堆积区域{i+1}"
            })
    return zones

def init_forklifts(nums=3):
    """
    初始化叉车队。
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": (39, 25),  # Forklift_2叉车初始位置调整为(39,25)
        })
    return forklifts

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

def init_loading_docks(nums=4):
    """
    初始化装货月台。
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

def init_unloading_docks(nums=4):
    """
    初始化卸货月台。
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

def init_shelves(nums=10):
    """
    初始化货架。
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

def init_sorting_stations(nums=3):
    """
    初始化分拣台。
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

def init_workers(nums=6):
    """
    初始化仓储作业人员。
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

def init_pallets(nums=20):
    """
    初始化托盘。
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

def init_orders(nums=8):
    """
    初始化订单。
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

def init_inventory_records(nums=10):
    """
    初始化库存记录。
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

def init_conveyors(nums=2):
    """
    初始化传送带。
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

def init_picking_tasks(nums=6):
    """
    初始化拣货任务。
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

def init_shipping_tasks(nums=6):
    """
    初始化发货任务。
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

def init_truck_arrival_schedule(trucks):
    """
    初始化货车到达时间表。
    返回时间表列表，每个时间表包含id、到达时间
    """
    schedule = []
    for truck in trucks:
        schedule.append({
            "id": truck["id"],
            "arrival_time": truck["arrival_time"],
        })
    return schedule

def update_truck_arrival_interval(trucks):
    """
    更新货车到达间隔时间。
    返回更新后的时间表列表，每个时间表包含id、到达时间
    """
    for truck in trucks:
        if truck["id"] == "Truck_7":  # 从第7辆货车开始间隔改为5分钟
            truck["arrival_time"] = time.strftime("%H:%M:%S", time.localtime(time.strptime(truck["arrival_time"], "%H:%M:%S") + 5 * 60))
    return trucks

def update_forklift_location(forklifts):
    """
    更新叉车位置。
    返回更新后的叉车列表，每个叉车包含id、位置
    """
    for forklift in forklifts:
        if forklift["id"] == "Forklift_2":  # Forklift_2叉车初始位置调整为(39,25)
            forklift["location"] = (39, 25)
    return forklifts

def update_zone_status(zones):
    """
    更新货物堆积区域状态。
    返回更新后的区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    for zone in zones:
        if zone["id"] == "Zone_3":  # Zone_3堆积区发生故障不可用
            zone["max_capacity"] = 0
            zone["desc"] = "货物堆积区域3故障不可用"
    return zones

def update_station_status(stations):
    """
    更新分拣台状态。
    返回更新后的分拣台列表，每个分拣台包含id、位置、状态
    """
    for station in stations:
        station["status"] = "idle"
    return stations

def update_dock_status(docks):
    """
    更新装货月台状态。
    返回更新后的月台列表，每个月台包含id、位置、状态
    """
    for dock in docks:
        dock["status"] = "idle"
    return docks

def update_unload_dock_status(unload_docks):
    """
    更新卸货月台状态。
    返回更新后的月台列表，每个月台包含id、位置、状态
    """
    for unload_dock in unload_docks:
        unload_dock["status"] = "idle"
    return unload_docks

def update_shelf_status(shelves):
    """
    更新货架状态。
    返回更新后的货架列表，每个货架包含id、位置、容量
    """
    for shelf in shelves:
        shelf["capacity"] = 50
    return shelves

def update_pallet_status(pallets):
    """
    更新托盘状态。
    返回更新后的托盘列表，每个托盘包含id、位置、载重
    """
    for pallet in pallets:
        pallet["max_weight"] = 1000
    return pallets

def update_order_status(orders):
    """
    更新订单状态。
    返回更新后的订单列表，每个订单包含id、货物数量、状态
    """
    for order in orders:
        order["status"] = "pending"
    return orders

def update_inventory_record(records):
    """
    更新库存记录。
    返回更新后的库存记录列表，每条记录包含id、sku、数量
    """
    for record in records:
        record["quantity"] = 100
    return records

def update_conveyor_status(conveyors):
    """
    更新传送带状态。
    返回更新后的传送带列表，每条传送带包含id、长度、状态
    """
    for conveyor in conveyors:
        conveyor["status"] = "running"
    return conveyors

def update_picking_task(tasks):
    """
    更新拣货任务。
    返回更新后的任务列表，每个任务包含id、目标货架、状态
    """
    for task in tasks:
        task["status"] = "waiting"
    return tasks

def update_shipping_task(tasks):
    """
    更新发货任务。
    返回更新后的任务列表，每个任务包含id、目标月台、状态
    """
    for task in tasks:
        task["status"] = "waiting"
    return tasks

# 初始化数据
trucks = init_truck_arrival_time()
zones = init_stacking_zones()
forklifts = init_forklifts()
docks = init_loading_docks()
unload_docks = init_unloading_docks()
shelves = init_shelves()
stations = init_sorting_stations()
workers = init_workers()
pallets = init_pallets()
orders = init_orders()
records = init_inventory_records()
conveyors = init_conveyors()
tasks = init_picking_tasks()
ship_tasks = init_shipping_tasks()

# 更新数据
trucks = update_truck_arrival_interval(trucks)
forklifts = update_forklift_location(forklifts)
zones = update_zone_status(zones)
stations = update_station_status(stations)
docks = update_dock_status(docks)
unload_docks = update_unload_dock_status(unload_docks)
shelves = update_shelf_status(shelves)
pallets = update_pallet_status(pallets)
orders = update_order_status(orders)
records = update_inventory_record(records)
conveyors = update_conveyor_status(conveyors)
tasks = update_picking_task(tasks)
ship_tasks = update_shipping_task(ship_tasks)

# 输出数据
print(trucks)
print(zones)
print(forklifts)
print(docks)
print(unload_docks)
print(shelves)
print(stations)
print(workers)
print(pallets)
print(orders)
print(records)
print(conveyors)
print(tasks)
print(ship_tasks)
