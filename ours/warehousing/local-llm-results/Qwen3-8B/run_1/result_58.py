import heapq
import time
import random

def init_stacking_zones(nums=4):
    zones = []
    for i in range(nums):
        if i == 0:  # Zone_1
            zone = {
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 100,
                "status": "unavailable",
                "desc": f"货物堆积区域{i+1}"
            }
        elif i == 2:  # Zone_3
            zone = {
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 29,
                "max_capacity": 100,
                "status": "available",
                "desc": f"货物堆积区域{i+1}"
            }
        elif i == 3:  # Zone_4
            zone = {
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 92,
                "status": "available",
                "desc": f"货物堆积区域{i+1}"
            }
        else:  # Zone_2
            zone = {
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 100,
                "status": "available",
                "desc": f"货物堆积区域{i+1}"
            }
        zones.append(zone)
    return zones
