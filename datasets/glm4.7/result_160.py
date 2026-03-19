import heapq
import time
import random

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        # 默认状态为"available"
        status = "available"
        # 如果是第4个资源（id为3），则标记为不可用
        if i == 3:
            status = "unavailable"
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10)), "status": status})
    return mobile_resources