import heapq
import time
import random

def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time_struct = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    current_ts = time.mktime(start_time_struct)

    for i in range(nums):
        if i == 0:
            interval = 0
        elif i == 1:
            interval = 3 * 60
        else:
            # 从第3辆货车（i=2）开始，间隔改为6分钟
            interval = 6 * 60

        current_ts += interval
        arrival_time = time.strftime("%H:%M:%S", time.localtime(current_ts))
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
        current_stock = 0
        max_capacity = 100
        if i == 1:
            current_stock = 75
            max_capacity = 133
        zones.append({
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": current_stock,
            "max_capacity": max_capacity,
            "desc": f"货物堆积区域{i+1}"
        })
    return zones
