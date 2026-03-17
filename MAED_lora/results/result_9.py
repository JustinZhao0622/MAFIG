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
        zone_id = f"Zone_{i+1}"
        if zone_id == "Zone_1":
            max_capacity = 96
        else:
            max_capacity = 100
        zones.append({
            "id": zone_id,
            "location": (0,25),
            "current_stock": 0,
            "max_capacity": max_capacity,
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
        forklift_id = f"Forklift_{i+1}"
        if forklift_id == "Forklift_3":
            continue
        location = (0, 25)
        if forklift_id == "Forklift_1":
            location = (45, 45)
        forklifts.append({
            "id": forklift_id,
            "location": location,
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
        if i < 4:
            offset = 3 * 60 * i
        else:
            offset = 3 * 60 * 3 + 6 * 60 * (i - 3)
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + offset))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks

