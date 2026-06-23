import heapq
import time
import random

def init_forklifts(nums=3):
    forklifts = []
    for i in range(nums):
        if i == 1:  # Forklift_2 is the second forklift (index 1)
            location = (24, 29)
            status = "unavailable"
        else:
            location = (0, 25)
            status = "available"
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": location,
            "status": status,
        })
    return forklifts
