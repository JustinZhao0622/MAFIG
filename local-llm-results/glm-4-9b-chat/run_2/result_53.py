import heapq
import time
import random

def init_planes(nums=5, start_time="8:00:00"):
    """初始化舰载机，每隔五分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i >= 4:  # 从第5架舰载机开始
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 5 * 60 * (i - 4)))
        else:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i, 10)})
    return planes

# 修改固定资源初始化，排除故障点
def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        while True:
            location = (random.randint(0, 3), random.randint(0, 10))
            if location not in [(6, 3), (7, 3), (6, 4), (7, 4)]:  # 排除故障点
                fixed_resources.append({"id": i, "type": "crane", "location": location})
                break
    return fixed_resources

# 修改移动资源初始化，排除故障点
def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        while True:
            location = (random.randint(0, 3), random.randint(0, 10))
            if location not in [(6, 3), (7, 3), (6, 4), (7, 4)]:  # 排除故障点
                mobile_resources.append({"id": i, "type": "crane", "location": location})
                break
    return mobile_resources

# 修改牵引任务目标站位
def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        if i == 3:  # 第3个牵引任务目标站位调整为(0,6)
            towing_tasks.append({"id": i, "type": "towing", "location": (0, 6)})
        else:
            towing_tasks.append({"id": i, "type": "towing", "location": (random.randint(0, 3), random.randint(0, 10))})
    return towing_tasks

# 修改消防车初始位置
def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i == 3:  # 第3辆消防车初始位置调整为(2,10)
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (2, 10)})
        else:
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_vehicle_resources

# 修改气源车故障
def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        if i == 3:  # 第3辆气源车发生故障不可用
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources
