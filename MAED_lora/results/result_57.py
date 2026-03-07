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
        current_stock = 0
        max_capacity = 100

        if zone_id == "Zone_4":
            max_capacity = 145
        if zone_id == "Zone_3":
            current_stock = 69

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
        forklift_id = f"Forklift_{i+1}"
        if forklift_id == "Forklift_3":
            continue
        location = (0, 25)
        if forklift_id == "Forklift_2":
            location = (10, 23)
        forklifts.append({
            "id": forklift_id,
            "location": location,
        })
    return forklifts

