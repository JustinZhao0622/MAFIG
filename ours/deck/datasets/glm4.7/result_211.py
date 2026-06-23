import heapq
import time
import random

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        if i == 2:  # 第3辆充氧车
            location = (-1, -1)  # 特殊位置表示故障
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": location})
    return oxygen_truck_resources