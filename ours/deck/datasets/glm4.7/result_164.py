import heapq
import time
import random

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        fuel_truck = {"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))}
        if i == 4:  # 第5辆车，id为4
            fuel_truck["status"] = "unavailable"  # 标记为不可用
        else:
            fuel_truck["status"] = "available"  # 其他车标记为可用
        fuel_truck_resources.append(fuel_truck)
    return fuel_truck_resources