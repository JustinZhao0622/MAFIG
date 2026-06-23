import heapq
import time
import random

def init_planes(nums=5, start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
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
        if i != 3:  # 修改第4辆牵引车初始位置
            tractor_resources.append({"id": i, "type": "tractor", "location": (random.randint(0, 3), random.randint(0, 10))})
        else:
            tractor_resources.append({"id": i, "type": "tractor", "location": (1, 5)})  # 设置第4辆牵引车初始位置为(1,5)
    return tractor_resources

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        if i != 3:  # 第4辆充氧车发生故障不可用
            fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
        else:
            continue  # 第4辆充氧车不可用，跳过
    return fuel_truck_resources

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        if i != 3:  # 第4辆供电车初始位置调整为(2,1)
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
        else:
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (2, 1)})  # 设置第4辆供电车初始位置为(2,1)
    return power_cart_resources

def init_hydraulic_cart_resources(nums=10):
    """初始化液压车资源，返回资源列表，每个资源包含id、类型"""
    hydraulic_cart_resources = []
    for i in range(nums):
        if i != 3:  # 第4辆液压车初始位置调整为(2,6)
            hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
        else:
            hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": (2, 6)})  # 设置第4辆液压车初始位置为(2,6)
    return hydraulic_cart_resources

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_vehicle_resources

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        if i != 5:  # 站位(11,10)发生故障，以该点为终点的调整为(12,10)
            towing_tasks.append({"id": i, "type": "towing", "location": (random.randint(0, 3), random.randint(0, 10))})
        else:
            towing_tasks.append({"id": i, "type": "towing", "location": (12, 10)})  # 设置任务终点为(12,10)
    return towing_tasks

def init_inspection_tasks(nums=6):
    """初始化检查任务，返回任务列表，每个任务包含id、类型"""
    inspection_tasks = []
    for i in range(nums):
        if i in [4, 5, 6, 7]:  # 站位(5,4)(6,4)(5,5)(6,5)四个点发生故障
            continue  # 这些任务不可用，跳过
        inspection_tasks.append({"id": i, "type": "inspection", "location": (random.randint(0, 3), random.randint(0, 10))})
    return inspection_tasks

# 其他函数保持不变
