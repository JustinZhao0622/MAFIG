import heapq
import time
import random 
def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    for i in range(nums):
        if i != 3:
            resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return resources