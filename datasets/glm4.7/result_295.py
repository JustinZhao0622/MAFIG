import heapq
import time
import random

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        truck = {"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))}
        if i == 2:
            truck["available"] = False
        else:
            truck["available"] = True
        oxygen_truck_resources.append(truck)
    return oxygen_truck_resources