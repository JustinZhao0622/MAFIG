import heapq
import time
import random

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        if i == 3:  # 第4辆加油车(id=3)发生故障
            fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10)), "status": "unavailable"})
        else:
            fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10)), "status": "available"})
    return fuel_truck_resources