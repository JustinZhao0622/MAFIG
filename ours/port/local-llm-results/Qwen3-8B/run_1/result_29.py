import heapq
import time
import random

def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    fault_points = [(6,3), (7,3), (6,4), (7,4)]
    for i in range(nums):
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 10)
            location = (x, y)
            if location not in fault_points:
                break
        resources.append({"id": i, "type": "crane", "location": location})
    return resources
