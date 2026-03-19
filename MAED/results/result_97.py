import heapq
import time
import random

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        # 根据突发事件描述，将第2辆加氮车的初始位置调整为(3,1)
        if i == 1:
            nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (3, 1)})
        else:
            nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_truck_resources

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        # 根据突发事件描述，将第3个牵引任务目标站位调整为(1,8)
        if i == 2:
            location = (1, 8)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        towing_tasks.append({"id": i, "type": "towing", "location": location})
    return towing_tasks

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        if i == 1:  # 假设第2辆气源车发生故障不可用
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        if i == 1:  # 假设第2辆充氧车发生故障，不添加到资源列表中
            continue
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_truck_resources

