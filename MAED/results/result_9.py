import heapq
import time
import random

def init_stacking_zones(nums=4):
    """
    初始化货物堆积区域 (A, B, C, D 区)。
    每个区域包含：坐标、当前存放数量 (current_stock)、最大容量 (max_capacity)。
    返回可用区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    zones = []
    for i in range(nums):
        if i == 0:
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 96,
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
        if i == 0:
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (45, 45),
            })
        else:
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (0, 25),
            })
    return forklifts

def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    for i in range(nums):
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 6 * 60 * i))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks

