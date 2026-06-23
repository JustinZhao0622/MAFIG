import heapq
import time
import random

"""
原子函数库 —— 甲板舰载机调度
"""





def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    start_time_seconds = time.mktime(start_time)
    for i in range(nums):
        if i <5:
            interval =3
        else:
            interval=5
        if i <5:
            total_time = start_time_seconds + 3 * 60 * i
        else:
            total_time = start_time_seconds + 3 * 60 *5 +5 *60*(i-5)
        plane_time = time.strftime("%H:%M:%S", time.localtime(total_time))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes


def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        if i ==1:
            location = (2,0)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        fixed_resources.append({"id": i, "type": "crane", "location": location})
    return fixed_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        if i ==1:
            location = (random.randint(0, 3), random.randint(0, 10))
            mobile_resources.append({"id": i, "type": "crane", "location": location, "available": False})
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
            mobile_resources.append({"id": i, "type": "crane", "location": location, "available": True})
    return mobile_resources


def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        if i ==1:
            location = (random.randint(0, 3), random.randint(0, 10))
            oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": location, "available": False})
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
            oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": location, "available": True})
    return oxygen_truck_resources


def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        if i ==1:
            location = (random.randint(0, 3), random.randint(0, 10))
            air_source_car_resources.append({"id": i, "type": "air_source_car", "location": location, "available": False})
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
            air_source_car_resources.append({"id": i, "type": "air_source_car", "location": location, "available": True})
    return air_source_car_resources


def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i ==1:
            location = (2,0)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": location})
    return fire_vehicle_resources
