import heapq
import time
import random

"""
原子函数库
"""



# 货车到达时间
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是6分钟，从第5辆货车开始
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    for i in range(nums):
        if i < 5:
            arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        else:
            arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 6 * 60 * (i - 4)))
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
        zones.append({
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": 0,
            "max_capacity": 61,
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
            "location": (27, 16),
        })
    return forklifts

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
