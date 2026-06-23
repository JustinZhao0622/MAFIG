import heapq
import time
import random

def init_air_source_car_resources(nums=10):
    air_source_car_resources = []
    for i in range(nums):
        if i == 2:
            continue  # 跳过第3辆（id=2）
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources
