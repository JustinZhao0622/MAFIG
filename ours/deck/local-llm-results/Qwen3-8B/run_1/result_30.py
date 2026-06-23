import heapq
import time
import random

def init_fixed_resources(nums=10):
    faulty_points = {(3,4), (4,4), (3,5), (4,5)}
    fixed_resources = []
    for i in range(nums):
        loc = (random.randint(0,3), random.randint(0,10))
        available = loc not in faulty_points
        fixed_resources.append({"id": i, "type": "crane", "location": loc, "available": available})
    return fixed_resources
