import heapq
import time
import random

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        power_cart_resources.append({"id": i, "type": "power_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    for resource in power_cart_resources:
        if resource["id"] == 3:
            resource["location"] = (2, 2)
    return power_cart_resources