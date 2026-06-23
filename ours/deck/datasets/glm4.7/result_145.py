import heapq
import time
import random

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        truck = {"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))}
        if i == 4:  # 第5辆加油车（id为4）发生故障不可用
            truck["available"] = False
        else:
            truck["available"] = True
        fuel_truck_resources.append(truck)
    return fuel_truck_resources