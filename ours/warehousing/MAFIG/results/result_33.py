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
        if f"Forklift_{i+1}" != "Forklift_1":
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (0, 25),
            })
    forklifts.append({
        "id": "Forklift_2",
        "location": (22, 46),
    })
    return forklifts

