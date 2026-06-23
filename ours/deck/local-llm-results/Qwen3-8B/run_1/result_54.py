import heapq
import time
import random

def init_power_cart_resources(nums=10):
    power_cart_resources = []
    for i in range(nums):
        power_cart_resources.append({"id": i, "type": "power_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return power_cart_resources
