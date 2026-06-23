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
        # 根据突发事件调整Zone_1的参数
        # Zone_1故障不可用：通过将current_stock设置为max_capacity来实现
        # Zone_1最大容量缩减至96
        if i == 0:
            max_capacity = 96
            current_stock = 96
        else:
            max_capacity = 100
            current_stock = 0

        zones.append({
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": current_stock,
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
        current_id = f"Forklift_{i+1}"
        if current_id == "Forklift_3":
            continue
        if current_id == "Forklift_1":
            location = (45, 45)
        else:
            location = (0, 25)
        forklifts.append({
            "id": current_id,
            "location": location,
        })
    return forklifts

def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    base_timestamp = time.mktime(start_time)
    trucks = []
    for i in range(nums):
        if i < 4:
            offset_seconds = 3 * 60 * i
        else:
            offset_seconds = (3 * 3 + 6 * (i - 3)) * 60
        arrival_time = time.strftime("%H:%M:%S", time.localtime(base_timestamp + offset_seconds))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks
