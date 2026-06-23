import heapq
import time
import random

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        if i == 2:  # 第3辆供电车（id为2）
            location = (0, 5)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        power_cart_resources.append({"id": i, "type": "power_cart", "location": location})
    return power_cart_resources