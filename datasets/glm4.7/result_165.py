import heapq
import time
import random

def init_hydraulic_cart_resources(nums=10):
    """初始化液压车资源，返回资源列表，每个资源包含id、类型"""
    hydraulic_cart_resources = []
    for i in range(nums):
        hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 确保第5辆液压车（id为4）的位置为(3,10)
    for cart in hydraulic_cart_resources:
        if cart["id"] == 4:
            cart["location"] = (3, 10)
            break
    return hydraulic_cart_resources