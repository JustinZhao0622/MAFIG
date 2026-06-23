import heapq
import time
import random

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    
    # 标记第1辆加油车为不可用
    for truck in fuel_truck_resources:
        if truck["id"] == 1:
            truck["available"] = False
            break
    
    return fuel_truck_resources