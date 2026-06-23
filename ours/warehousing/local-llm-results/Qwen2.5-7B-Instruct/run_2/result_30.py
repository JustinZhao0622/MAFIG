import heapq
import time
import random

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
        if i != 1 and i != 2:
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 141 if i == 0 else 100,
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
        if i != 2:
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (0, 25),
            })
    return forklifts

def init_unloading_docks(nums=4):
    """
    初始化卸货月台。
    返回月台列表，每个月台包含id、位置、状态
    """
    docks = []
    for i in range(nums):
        if i != 1:
            docks.append({
                "id": f"UnloadDock_{i+1}",
                "location": (i * 5, 5),
                "status": "idle",
            })
    return docks

def init_workers(nums=6):
    """
    初始化仓储作业人员。
    返回人员列表，每个人员包含id、岗位、状态
    """
    workers = []
    for i in range(nums):
        if i != 3:
            workers.append({
                "id": f"Worker_{i+1}",
                "role": "operator",
                "status": "available",
            })
    return workers

def init_picking_tasks(nums=6):
    """
    初始化拣货任务。
    返回任务列表，每个任务包含id、目标货架、状态
    """
    tasks = []
    for i in range(nums):
        if i != 2:
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
        if i != 2:
            tasks.append({
                "id": f"ShipTask_{i+1}",
                "target_dock": f"Dock_{(i % 4) + 1}",
                "status": "waiting",
            })
    return tasks
