import heapq
import time
import random

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    count = 0
    i = 0
    while count < nums:
        if i != 1:  # 跳过ID为1的故障加油车
            fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
            count += 1
        i += 1
    return fuel_truck_resources