import heapq
import time
import random

def route_planning(...):
    ...
    if end_point == (8,7):
        end_point = (9,7)
    ...

但需要确保这不会影响其他情况。这可能是一个可行的修改。

第二个修改，在init_stacking_zones函数中，当i=0时（即Zone_1），current_stock设为24，其他保持0。原代码中，每个zone的current_stock初始化为0，所以修改为：

for i in range(nums):
    if i == 0:
        current_stock = 24
    else:
        current_stock = 0
    zones.append({...})

或者更准确地说，在循环中，当i=0时，设置current_stock为24，其他保持0。

第三个修改，在init_truck_arrival_time函数中，计算到达时间时，如果i >=4（即第5辆货车，因为i从0开始），则间隔为5分钟，否则3分钟。原代码中的计算是3*60*i，现在改为：

arrival_time = time.strftime(..., time.mktime(start_time) + (3 if i <4 else 5)*60*i )

或者更准确地说，对于每个i，计算间隔为3分钟，当i >=4时改为5分钟。因此，修改为：

for i in range(nums):
    interval = 3 if i <4 else 5
    arrival_time = time.mktime(start_time) + interval * 60 * i

第四个修改，在route_planning函数中，添加故障点列表，并在探索方向时检查next_pos是否在故障点列表中。例如：

faulty_points = [(5,4), (6,4), (5,5), (6,5)]

然后，在探索方向时，检查next_pos是否在faulty_points中，如果是，则跳过。

现在，我需要将这些修改应用到原始代码中，确保不违反任何规则。

现在，检查每个修改是否符合要求：

1. route_planning函数的修改：在函数内部检查end_point是否为(8,7)，如果是则改为(9,7)。这属于修改函数体内部逻辑，符合规则。

2. init_stacking_zones函数：在循环中，当i=0时设置current_stock为24，其他为0。这属于修改函数体内部逻辑，符合规则。

3. init_truck_arrival_time函数：修改间隔计算，从第5辆开始改为5分钟。这属于修改函数体内部逻辑，符合规则。

4. route_planning函数：添加故障点列表，并在探索方向时检查next_pos是否在其中。这属于修改函数体内部逻辑，符合规则。

现在，需要确保这些修改不会引入其他问题，例如，故障点列表是否正确，是否影响其他路径规划。

此外，需要确保所有修改后的代码仍然可以运行，没有语法错误。

现在，将这些修改整合到原始代码中，确保没有其他改动，如import语句保持原样，函数名、参数、返回值不变。
</think>

"""
原子函数库
"""



# 货车到达时间
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    for i in range(nums):
        interval = 3 if i <4 else 5
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + interval * 60 * i))
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
        if i == 0:
            current_stock = 24
        else:
            current_stock = 0
        zones.append({
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": current_stock,
            "max_capacity": 100,
            "desc": f"货物堆积区域{i+1}"
        })
    return zones

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

    # 故障点列表
    faulty_points = [(5,4), (6,4), (5,5), (6,5)]

    # 优先队列：(f值, 计数器, 当前点, 路径)
    counter = 0
    heap = [(heuristic(begin_point), counter, begin_point, [begin_point])]
    visited = {begin_point}

    # 检查终点是否为故障点
    if end_point == (8,7):
        end_point = (9,7)

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

            # 检查是否是故障点
            if next_pos in faulty_points:
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
