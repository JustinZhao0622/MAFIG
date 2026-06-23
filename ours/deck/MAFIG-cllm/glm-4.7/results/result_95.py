import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    base_ts = time.mktime(start_time)
    for i in range(nums):
        # 从第6架舰载机开始(id=5)，到达间隔改为5分钟
        # 前5架(id=0~4)间隔仍为3分钟
        if i < 5:
            offset = i * 3 * 60
        else:
            # 第5架(id=4)的时间点是 4 * 3 * 60
            # 第6架(id=5)及之后，每架间隔5分钟
            offset = (4 * 3 * 60) + (i - 4) * 5 * 60

        plane_time = time.strftime("%H:%M:%S", time.localtime(base_ts + offset))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i == 1:
            location = (2, 0)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": location})
    return fire_vehicle_resources

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        location = (random.randint(0, 3), random.randint(0, 10))
        if i == 1:
            location = (2, 0)
        fixed_resources.append({"id": i, "type": "crane", "location": location})
    return fixed_resources

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        if i == 1:
            continue
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_truck_resources

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        if i == 1:
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        # 突发事件：第2个通用移动资源（索引为1）发生故障不可用
        if i == 1:
            continue
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources
