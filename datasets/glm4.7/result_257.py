import heapq
import time
import random

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
        # 标记第4辆加油车为不可用
        if i == 3:
            fuel_truck_resources[-1]["available"] = False
        else:
            fuel_truck_resources[-1]["available"] = True
    return fuel_truck_resources