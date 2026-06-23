import heapq
import time
import random

def init_forklifts(nums=3):
    """
    初始化叉车队。
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        if i + 1 == 3:
            continue
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
        if i < 2:
            offset_seconds = 3 * 60 * i
        else:
            # 从第3辆货车开始(i=2)，间隔改为5分钟
            # 前2辆货车耗时6分钟(3分钟间隔)，后续货车每辆间隔5分钟
            offset_seconds = 3 * 60 + (i - 1) * 5 * 60

        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + offset_seconds))
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
        # 默认初始化参数
        z_id = f"Zone_{i+1}"
        location = (0, 25)
        current_stock = 0
        max_capacity = 100
        desc = f"货物堆积区域{i+1}"

        # 根据突发事件调整参数
        if i == 0:  # Zone_1
            # Zone_1 发生故障不可用，将最大容量设为0以阻止调度
            max_capacity = 0
        elif i == 1:  # Zone_2
            # Zone_2 最大容量缩减至93
            max_capacity = 93
        elif i == 3:  # Zone_4
            # Zone_4 当前库存增加48
            current_stock = 48

        zones.append({
            "id": z_id,
            "location": location,
            "current_stock": current_stock,
            "max_capacity": max_capacity,
            "desc": desc
        })
    return zones
