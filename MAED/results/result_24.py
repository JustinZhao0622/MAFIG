import heapq
import time
import random

def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间改为8分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    for i in range(nums):
        if i >= 6:  # 从第7辆货车开始
            arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 8 * 60 * (i - 6)))
        else:
            arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
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
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": (46, 48) if i == 0 else (0, 25),
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
        if i == 2:  # Zone_3
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0, 25),
                "current_stock": 24,  # 突发事件：Zone_3堆积区当前库存增加24
                "max_capacity": 100,
                "desc": f"货物堆积区域{i+1}",
                "available": False  # 突发事件：Zone_3堆积区发生故障不可用
            })
        else:
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0, 25),
                "current_stock": 0,
                "max_capacity": 100,
                "desc": f"货物堆积区域{i+1}",
                "available": True
            })
    return zones

