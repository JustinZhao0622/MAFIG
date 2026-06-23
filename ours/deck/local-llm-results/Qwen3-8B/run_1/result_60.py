import heapq
import time
import random

def init_air_source_car_resources(nums=10):
    air_source_car_resources = []
    for i in range(nums):
        if i == 1:  # 第2辆（i=1）不可用，跳过
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources
