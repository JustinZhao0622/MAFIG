import heapq
import time
import random

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    
    # 标记第2辆充氧车为不可用
    for truck in oxygen_truck_resources:
        if truck["id"] == 2:
            truck["available"] = False
            break
    
    # 确保所有其他充氧车都标记为可用
    for truck in oxygen_truck_resources:
        if truck["id"] != 2 and "available" not in truck:
            truck["available"] = True
            
    return oxygen_truck_resources