import heapq
import time
import random

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        oxygen_truck = {"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))}
        # 标记第4辆充氧车为不可用
        if i == 3:  # 第4辆充氧车，索引从0开始
            oxygen_truck["status"] = "unavailable"
        else:
            oxygen_truck["status"] = "available"
        oxygen_truck_resources.append(oxygen_truck)
    return oxygen_truck_resources