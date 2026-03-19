import heapq
import time
import random

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        if i == 1:
            fixed_resources.append({"id": i, "type": "crane", "location": (1, 9)})
        else:
            fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i == 1:  # 确保第2辆牵引车初始位置调整为(3,2)
            tractor_resources.append({"id": i, "type": "tractor", "location": (3, 2)})
        else:
            tractor_resources.append({"id": i, "type": "tractor", "location": (random.randint(0, 3), random.randint(0, 10))})
    return tractor_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        if i == 1:  # 假设第二个资源发生故障
            continue
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        if i == 1:  # 假设第2辆加油车发生故障不可用
            continue
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fuel_truck_resources

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        # 修改任务目标站位为(2,9)
        location = (2, 9) if i == 0 else (random.randint(0, 3), random.randint(0, 10))
        towing_tasks.append({"id": i, "type": "towing", "location": location})
    return towing_tasks

