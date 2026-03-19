import heapq
import time
import random

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        # 修改任务目标站位为(1,4)
        location = (1, 4)
        towing_tasks.append({"id": i, "type": "towing", "location": location})
    return towing_tasks

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        if i == 3:  # 突发事件：第4辆充氧车发生故障不可用
            continue  # 跳过第4辆充氧车的初始化
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_truck_resources

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        fixed_resources.append({"id": i, "type": "crane", "location": (0, 10)})  # 修改初始位置为(0, 10)
    return fixed_resources

