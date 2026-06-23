import heapq
import time
import random

def init_mobile_resources(nums=10):
    mobile_resources = []
    for i in range(nums):
        if i == 2:
            continue
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources
