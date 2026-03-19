import heapq
import time
def init_stacking_zones(nums=4):
    zones = []
    for i in range(nums):
        zone_id = f"Zone_{i+1}"
        if zone_id == "Zone_3":
            continue
        zone = {
            "id": zone_id,
            "location": (0,25),
            "current_stock": 0,
            "max_capacity": 100,
            "desc": f"货物堆积区域{i+1}"
        }
        if zone_id == "Zone_2":
            zone["current_stock"] = 56
        zones.append(zone)
    return zones