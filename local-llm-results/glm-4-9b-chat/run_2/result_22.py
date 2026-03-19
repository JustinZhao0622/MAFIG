import heapq
import time
import random

def init_planes(nums=5, start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i, 10)})
    return planes

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i != 4:  # 修改第5辆牵引车初始位置
            tractor_resources.append({"id": i, "type": "tractor", "location": (random.randint(0, 3), random.randint(0, 10))})
        else:
            tractor_resources.append({"id": i, "type": "tractor", "location": (3, 2)})  # 设置第5辆牵引车初始位置为(3,2)
    return tractor_resources

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        if i != 4:  # 第5辆加油车发生故障不可用
            fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fuel_truck_resources

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        if i != 4:  # 第5个通用移动资源发生故障不可用
            nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_truck_resources

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        if i != 4:  # 第5辆充氧车发生故障不可用
            oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
        else:
            oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (3, 7)})  # 设置第5辆消防车初始位置为(3,7)
    return oxygen_truck_resources

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i != 4:  # 第5辆消防车发生故障不可用
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
        else:
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (3, 7)})  # 设置第5辆消防车初始位置为(3,7)
    return fire_vehicle_resources

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        if i != 5:  # 第6个牵引任务目标站位调整为(0,3)
            towing_tasks.append({"id": i, "type": "towing", "location": (random.randint(0, 3), random.randint(0, 10))})
        else:
            towing_tasks.append({"id": i, "type": "towing", "location": (0, 3)})  # 设置第6个牵引任务目标站位为(0,3)
    return towing_tasks

# 其他函数保持不变
