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
        if i == 1:  # Zone_2堆积区最大容量缩减至143
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 143,
                "desc": f"货物堆积区域{i+1}"
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
        if i == 2:  # Forklift_3叉车初始位置调整为(22,19)
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (22, 19),
            })
        else:
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (0, 25),
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

def adjust_truck_arrival_interval(trucks):
    """
    调整货车到达间隔。
    返回调整后的时间表列表，每个时间表包含id、到达时间
    """
    schedule = []
    for i, truck in enumerate(trucks):
        arrival_time = truck["arrival_time"]
        if i >= 5:  # 从第6辆货车开始间隔改为6分钟
            arrival_time = time.strftime("%H:%M:%S", time.localtime(time.strptime(arrival_time, "%H:%M:%S") + 6 * 60))
        schedule.append({
            "id": truck["id"],
            "arrival_time": arrival_time,
        })
    return schedule

def adjust_zone_1_status(zones):
    """
    调整Zone_1堆积区状态。
    返回调整后的区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    for zone in zones:
        if zone["id"] == "Zone_1":
            zone["status"] = "unavailable"
    return zones

def adjust_forklift_3_location(forklifts):
    """
    调整Forklift_3叉车位置。
    返回调整后的叉车列表，每个叉车包含id、坐标
    """
    for forklift in forklifts:
        if forklift["id"] == "Forklift_3":
            forklift["location"] = (22, 19)
    return forklifts

def adjust_route_planning(begin_point, end_point, grid_size=(100, 100)):
    """
    调整路径规划。
    返回调整后的路径规划列表，每个路径规划包含路径点
    """
    return route_planning(begin_point, end_point, grid_size)

def adjust_station_status(stations):
    """
    调整分拣台状态。
    返回调整后的分拣台列表，每个分拣台包含id、位置、状态
    """
    for station in stations:
        station["status"] = "idle"
    return stations

def adjust_worker_status(workers):
    """
    调整仓储作业人员状态。
    返回调整后的人员列表，每个人员包含id、岗位、状态
    """
    for worker in workers:
        worker["status"] = "available"
    return workers

def adjust_pallet_location(pallets):
    """
    调整托盘位置。
    返回调整后的托盘列表，每个托盘包含id、位置、载重
    """
    for pallet in pallets:
        pallet["location"] = (pallet["location"][0], pallet["location"][1])
    return pallets

def adjust_order_status(orders):
    """
    调整订单状态。
    返回调整后的订单列表，每个订单包含id、货物数量、状态
    """
    for order in orders:
        order["status"] = "pending"
    return orders

def adjust_inventory_records(records):
    """
    调整库存记录。
    返回调整后的库存记录列表，每条记录包含id、sku、数量
    """
    for record in records:
        record["quantity"] = 100
    return records

def adjust_conveyor_status(conveyors):
    """
    调整传送带状态。
    返回调整后的传送带列表，每条传送带包含id、长度、状态
    """
    for conveyor in conveyors:
        conveyor["status"] = "running"
    return conveyors

def adjust_picking_task_status(tasks):
    """
    调整拣货任务状态。
    返回调整后的任务列表，每个任务包含id、目标货架、状态
    """
    for task in tasks:
        task["status"] = "waiting"
    return tasks

def adjust_shipping_task_status(tasks):
    """
    调整发货任务状态。
    返回调整后的任务列表，每个任务包含id、目标月台、状态
    """
    for task in tasks:
        task["status"] = "waiting"
    return tasks

def adjust_truck_arrival_time(trucks):
    """
    调整货车到达时间。
    返回调整后的时间表列表，每个时间表包含id、到达时间
    """
    for truck in trucks:
        truck["arrival_time"] = time.strftime("%H:%M:%S", time.strptime(truck["arrival_time"], "%H:%M:%S") + 3 * 60)

def adjust_zone_2_capacity(zones):
    """
    调整Zone_2堆积区最大容量。
    返回调整后的区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    for zone in zones:
        if zone["id"] == "Zone_2":
            zone["max_capacity"] = 143
    return zones

def adjust_forklift_location(forklifts):
    """
    调整叉车位置。
    返回调整后的叉车列表，每个叉车包含id、坐标
    """
    for forklift in forklifts:
        forklift["location"] = (forklift["location"][0], forklift["location"][1])
    return forklifts

def adjust_station_location(stations):
    """
    调整分拣台位置。
    返回调整后的分拣台列表，每个分拣台包含id、位置、状态
    """
    for station in stations:
        station["location"] = (station["location"][0], station["location"][1])
    return stations

def adjust_worker_location(workers):
    """
    调整仓储作业人员位置。
    返回调整后的人员列表，每个人员包含id、岗位、状态
    """
    for worker in workers:
        worker["location"] = (worker["location"][0], worker["location"][1])
    return workers

def adjust_pallet_weight(pallets):
    """
    调整托盘载重。
    返回调整后的托盘列表，每个托盘包含id、位置、载重
    """
    for pallet in pallets:
        pallet["max_weight"] = pallet["max_weight"]
    return pallets

def adjust_order_item_count(orders):
    """
    调整订单货物数量。
    返回调整后的订单列表，每个订单包含id、货物数量、状态
    """
    for order in orders:
        order["item_count"] = order["item_count"]
    return orders

def adjust_inventory_quantity(records):
    """
    调整库存数量。
    返回调整后的库存记录列表，每条记录包含id、sku、数量
    """
    for record in records:
        record["quantity"] = record["quantity"]
    return records

def adjust_conveyor_length(conveyors):
    """
    调整传送带长度。
    返回调整后的传送带列表，每条传送带包含id、长度、状态
    """
    for conveyor in conveyors:
        conveyor["length"] = conveyor["length"]
    return conveyors

def adjust_picking_task_target_shelf(tasks):
    """
    调整拣货任务目标货架。
    返回调整后的任务列表，每个任务包含id、目标货架、状态
    """
    for task in tasks:
        task["target_shelf"] = task["target_shelf"]
    return tasks

def adjust_shipping_task_target_dock(tasks):
    """
    调整发货任务目标月台。
    返回调整后的任务列表，每个任务包含id、目标月台、状态
    """
    for task in tasks:
        task["target_dock"] = task["target_dock"]
    return tasks

def adjust_truck_arrival_interval(trucks):
    """
    调整货车到达间隔。
    返回调整后的时间表列表，每个时间表包含id、到达时间
    """
    schedule = []
    for i, truck in enumerate(trucks):
        arrival_time = truck["arrival_time"]
        if i >= 5:  # 从第6辆货车开始间隔改为6分钟
            arrival_time = time.strftime("%H:%M:%S", time.strptime(arrival_time, "%H:%M:%S") + 6 * 60)
        schedule.append({
            "id": truck["id"],
            "arrival_time": arrival_time,
        })
    return schedule

def adjust_zone_1_status(zones):
    """
    调整Zone_1堆积区状态。
    返回调整后的区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    for zone in zones:
        if zone["id"] == "Zone_1":
            zone["status"] = "unavailable"
    return zones

def adjust_forklift_3_location(forklifts):
    """
    调整Forklift_3叉车位置。
    返回调整后的叉车列表，每个叉车包含id、坐标
    """
    for forklift in forklifts:
        if forklift["id"] == "Forklift_3":
            forklift["location"] = (22, 19)
    return forklifts

def adjust_route_planning(begin_point, end_point, grid_size=(100, 100)):
    """
    调整路径规划。
    返回调整后的路径规划列表，每个路径规划包含路径点
    """
    return route_planning(begin_point, end_point, grid_size)

def adjust_station_status(stations):
    """
    调整分拣台状态。
    返回调整后的分拣台列表，每个分拣台包含id、位置、状态
    """
    for station in stations:
        station["status"] = "idle"
    return stations

def adjust_worker_status(workers):
    """
    调整仓储作业人员状态。
    返回调整后的人员列表，每个人员包含id、岗位、状态
    """
    for worker in workers:
        worker["status"] = "available"
    return workers

def adjust_pallet_location(pallets):
    """
    调整托盘位置。
    返回调整后的托盘列表，每个托盘包含id、位置、载重
    """
    for pallet in pallets:
        pallet["location"] = (pallet["location"][0], pallet["location"][1])
    return pallets

def adjust_order_status(orders):
    """
    调整订单状态。
    返回调整后的订单列表，每个订单包含id、货物数量、状态
    """
    for order in orders:
        order["status"] = "pending"
    return orders

def adjust_inventory_records(records):
    """
    调整库存记录。
    返回调整后的库存记录列表，每条记录包含id、sku、数量
    """
    for record in records:
        record["quantity"] = 100
    return records

def adjust_conveyor_status(conveyors):
    """
    调整传送带状态。
    返回调整后的传送带列表，每条传送带包含id、长度、状态
    """
    for conveyor in conveyors:
        conveyor["status"] = "running"
    return conveyors

def adjust_picking_task_status(tasks):
    """
    调整拣货任务状态。
    返回调整后的任务列表，每个任务包含id、目标货架、状态
    """
    for task in tasks:
        task["status"] = "waiting"
    return tasks

def adjust_shipping_task_status(tasks):
    """
    调整发货任务状态。
    返回调整后的任务列表，每个任务包含id、目标月台、状态
    """
    for task in tasks:
        task["status"] = "waiting"
    return tasks

def adjust_truck_arrival_time(trucks):
    """
    调整货车到达时间。
    返回调整后的时间表列表，每个时间表包含id、到达时间
    """
    for truck in trucks:
        truck["arrival_time"] = time.strftime("%H:%M:%S", time.strptime(truck["arrival_time"], "%H:%M:%S") + 3 * 60)

def adjust_zone_2_capacity(zones):
    """
    调整Zone_2堆积区最大容量。
    返回调整后的区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    for zone in zones:
        if zone["id"] == "Zone_2":
            zone["max_capacity"] = 143
    return zones

def adjust_forklift_location(forklifts):
    """
    调整叉车位置。
    返回调整后的叉车列表，每个叉车包含id、坐标
    """
    for forklift in forklifts:
        forklift["location"] = (forklift["location"][0], forklift["location"][1])
    return forklifts

def adjust_station_location(stations):
    """
    调整分拣台位置。
    返回调整后的分拣台列表，每个分拣台包含id、位置、状态
    """
    for station in stations:
        station["location"] = (station["location"][0], station["location"][1])
    return stations

def adjust_worker_location(workers):
    """
    调整仓储作业人员位置。
    返回调整后的人员列表，每个人员包含id、岗位、状态
    """
    for worker in workers:
        worker["location"]
