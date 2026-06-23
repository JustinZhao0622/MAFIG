import heapq
import time
import random

def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    total_offset_minutes = 0
    for i in range(nums):
        if i == 0:
            interval = 0
        elif i < 3:
            interval = 3
        else:
            interval = 5
        total_offset_minutes += interval

        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + total_offset_minutes * 60))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks

def init_forklifts(nums=3):
    """
    初始化叉车队。
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        fid = f"Forklift_{i+1}"
        if fid != "Forklift_2":
            forklifts.append({
                "id": fid,
                "location": (0, 25),
            })
    return forklifts

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
            continue

        zone = {
            "id": zone_id,
            "location": (0,25),
            "current_stock": 0,
            "max_capacity": 100,
            "desc": f"货物堆积区域{i+1}"
        }

        if zone_id == "Zone_3":
            zone["current_stock"] = 51
            zone["max_capacity"] = 91

        zones.append(zone)
    return zones
