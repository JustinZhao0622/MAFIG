import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，前5架每隔三分钟到达一架，从第6架开始每隔五分钟到达一架，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i < 5:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        else:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * 4 + (i - 4) * 5 * 60))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i == 1:
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (2, 0)})
        else:
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_vehicle_resources

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        if i == 1:
            fixed_resources.append({"id": i, "type": "crane", "location": (2, 0)})
        else:
            fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        resource = {"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))}
        if i == 1:  # 第2辆充氧车（id为1）发生故障不可用
            resource["available"] = False
        else:
            resource["available"] = True
        oxygen_truck_resources.append(resource)
    return oxygen_truck_resources

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10)), "available": True})
    # 第2辆气源车发生故障不可用
    air_source_car_resources[1]["available"] = False
    return air_source_car_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        resource = {"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))}
        if i == 1:  # 第2个通用移动资源发生故障不可用
            resource["available"] = False
        else:
            resource["available"] = True

