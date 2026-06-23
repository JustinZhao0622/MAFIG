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
        capacity = 100
        stock = 0
        if i == 0:
            capacity = 111
            stock = 69
        zones.append({
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": stock,
            "max_capacity": capacity,
            "desc": f"货物堆积区域{i+1}"
        })
    return zones

def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。前两辆货车间隔3分钟，从第3辆开始间隔6分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    for i in range(nums):
        if i == 0:
            offset_seconds = 0
        elif i == 1:
            offset_seconds = 3 * 60
        else:
            offset_seconds = 3 * 60 + (i - 1) * 6 * 60

        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + offset_seconds))
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
        if fid == "Forklift_1":
            loc = (13, 35)
        else:
            loc = (0, 25)
        forklifts.append({
            "id": fid,
            "location": loc,
        })
    return forklifts
