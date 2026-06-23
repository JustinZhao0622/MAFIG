import heapq
import time
import random

def init_hydraulic_cart_resources(nums=10):
    """初始化液压车资源，返回资源列表，每个资源包含id、类型"""
    hydraulic_cart_resources = []
    for i in range(nums):
        hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    
    # 修改第4辆液压车的初始位置为(3,6)
    for cart in hydraulic_cart_resources:
        if cart["id"] == 3:
            cart["location"] = (3, 6)
            break
    
    return hydraulic_cart_resources