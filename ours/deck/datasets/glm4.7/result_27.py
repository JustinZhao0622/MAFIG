import heapq
import time
import random

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        resource = {"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))}
        if i == 3:  # 第4辆充氧车(id=3)发生故障
            resource["status"] = "faulty"
        oxygen_truck_resources.append(resource)
    return oxygen_truck_resources