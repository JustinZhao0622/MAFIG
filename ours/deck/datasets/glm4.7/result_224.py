import heapq
import time
import random

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        oxygen_truck = {"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))}
        if i == 1:  # 第1辆充氧车发生故障不可用
            oxygen_truck["status"] = "fault"
        oxygen_truck_resources.append(oxygen_truck)
    return oxygen_truck_resources