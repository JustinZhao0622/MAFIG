import heapq
import time
import random

def init_mobile_resources(nums=10):
    mobile_resources = []
    for i in range(1, nums):  # 从i=1开始，跳过第一个资源
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources
