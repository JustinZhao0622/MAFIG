import heapq
import time
import random

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        # 标记第4辆充氧车（id=3）为不可用
        available = True
        if i == 3:  # 第4辆充氧车
            available = False
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10)), "available": available})
    return oxygen_truck_resources