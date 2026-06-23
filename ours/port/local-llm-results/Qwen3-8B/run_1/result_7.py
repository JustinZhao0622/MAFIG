import heapq
import time
import random

def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    faulty_positions = [(6,5), (7,5), (6,6), (7,6)]
    for i in range(nums):
        location = (random.randint(0, 3), random.randint(0, 10))
        if location in faulty_positions:
            resources.append({"id": i, "type": "crane", "location": location, "status": "faulty"})
        else:
            resources.append({"id": i, "type": "crane", "location": location, "status": "available"})
    return resources
