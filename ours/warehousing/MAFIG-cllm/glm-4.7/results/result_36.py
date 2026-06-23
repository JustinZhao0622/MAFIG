import heapq
import time
import random

def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    current_offset = 0
    for i in range(nums):
        if i > 0:
            if i < 3:
                current_offset += 3 * 60
            else:
                current_offset += 6 * 60
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + current_offset))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks

def init_stacking_zones(nums=4):
    zones = []
    for i in range(nums):
        zone_id = f"Zone_{i+1}"
        current_stock = 0
        max_capacity = 100
        if zone_id == "Zone_1":
            current_stock = 66
        if zone_id == "Zone_4":
            max_capacity = 50
        zones.append({
            "id": zone_id,
            "location": (0,25),
            "current_stock": current_stock,
            "max_capacity": max_capacity,
            "desc": f"货物堆积区域{i+1}"
        })
    return zones
