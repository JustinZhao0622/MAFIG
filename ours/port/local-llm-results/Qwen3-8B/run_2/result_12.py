import heapq
import time
import random

def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    faulty_points = [(5,4), (6,4), (5,5), (6,5), (9,9)]
    resources = []
    for i in range(nums):
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 10)
            pos = (x, y)
            if pos not in faulty_points:
                break
        resources.append({"id": i, "type": "crane", "location": pos})
    return resources
