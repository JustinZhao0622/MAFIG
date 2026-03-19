import heapq
import time
import random

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        resource = {"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10)), "available": True}
        if i == 2:  # 第3个资源（索引为2）标记为不可用
            resource["available"] = False
        mobile_resources.append(resource)
    return mobile_resources