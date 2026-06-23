import heapq
import time
import random

def init_nitrogen_truck_resources(nums=10):
    nitrogen_truck_resources = []
    for i in range(nums):
        if i == 1:
            location = (1, 10)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": location})
    return nitrogen_truck_resources
