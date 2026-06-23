import heapq
import time
import random

def init_forklifts(nums=3):
    forklifts = []
    for i in range(nums):
        if i == 1:
            location = (39, 25)
        else:
            location = (0, 25)
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": location,
        })
    return forklifts
