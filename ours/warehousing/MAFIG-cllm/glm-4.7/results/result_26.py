import heapq
import time
import random

def init_stacking_zones(nums=4):
    zones = []
    for i in range(nums):
        zone_id = f"Zone_{i+1}"
        current_stock = 0
        max_capacity = 100
        if zone_id == "Zone_4":
            current_stock = 59
            max_capacity = 59
        zones.append({
            "id": zone_id,
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
        if i == 1:
            continue
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": (0, 25),
        })
    return forklifts
