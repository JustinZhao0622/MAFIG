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
        fid = f"Forklift_{i+1}"
        if fid == "Forklift_2":
            continue
        loc = (0, 25)
        if fid == "Forklift_3":
            loc = (36, 15)
        forklifts.append({
            "id": fid,
            "location": loc,
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

        # 初始化默认值
        current_stock = 0
        max_capacity = 100
        status = "available"

        # 根据突发事件调整 Zone_2 和 Zone_3 的状态
        if zone_id == "Zone_2":
            max_capacity = 51
        elif zone_id == "Zone_3":
            current_stock = 79
            status = "unavailable"

        zones.append({
            "id": zone_id,
            "location": (0,25),
            "current_stock": current_stock,
            "max_capacity": max_capacity,
            "desc": f"货物堆积区域{i+1}",
            "status": status
        })
    return zones
