import heapq
import time
import random

def init_forklifts(nums=3):
    forklifts = []
    for i in range(nums):
        if i == 0:  # Forklift_1不可用，跳过
            continue
        if i == 1:  # Forklift_2的位置改为(22,46)
            location = (22, 46)
        else:
            location = (0, 25)
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": location,
        })
    return forklifts
