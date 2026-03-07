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
        if i == 0:
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (28, 38),
            })
        else:
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (0, 25),
            })
    return forklifts

