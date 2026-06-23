import heapq
import time
import random

def init_forklifts(nums=3):
    forklifts = []
    for i in range(nums):
        if i == 2:  # 跳过第三个叉车
            continue
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": (0, 25),
        })
    return forklifts
