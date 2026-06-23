import heapq
import time
import random

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        resource = {"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))}
        # 标记第1个移动资源(id=0)为不可用
        if i == 0:
            resource["status"] = "unavailable"
        else:
            resource["status"] = "available"
        mobile_resources.append(resource)
    return mobile_resources