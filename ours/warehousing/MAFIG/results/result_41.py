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
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (29, 35),
            })
        else:
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (0, 25),
            })
    return forklifts

def find_forklift(forklifts, target_id):
    for forklift in forklifts:
        if forklift["id"] == target_id:
            return forklift
    return None

def main():
    forklifts = init_forklifts()
    forklift_2 = find_forklift(forklifts, "Forklift_2")
    if forklift_2 is None:
        print("Forklift_2 is unavailable")
    else:
        print(f"Forklift_2 location: {forklift_2['location']}")

main()

def init_stacking_zones(nums=4):
    """
    初始化货物堆积区域 (A, B, C, D 区)。
    每个区域包含：坐标、当前存放数量 (current_stock)、最大容量 (max_capacity)。
    返回可用区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    zones = []
    for i in range(nums):
        if i == 3:
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 87,
                "desc": f"货物堆积区域{i+1}"
            })
        else:
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 100,
                "desc": f"货物堆积区域{i+1}"
            })
    return zones

