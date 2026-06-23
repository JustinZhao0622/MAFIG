import heapq
import time
import random

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    
    # 标记第4辆气源车为不可用
    for car in air_source_car_resources:
        if car["id"] == 4:
            car["available"] = False
            break
    
    return air_source_car_resources