import heapq
import time
import random

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        # 第1个通用移动资源发生故障不可用
        if i == 0:
            mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10)), "status": "unavailable"})
        else:
            mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources