import heapq
import time
import random

def init_fixed_resources(nums=10):
    fixed_resources = []
    for i in range(nums):
        if i == 1:
            location = (2, 1)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        fixed_resources.append({"id": i, "type": "crane", "location": location})
    return fixed_resources
