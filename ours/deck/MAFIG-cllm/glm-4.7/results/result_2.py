import heapq
import time
import random

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i == 0:
            location = (3, 2)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": location})
    return fire_vehicle_resources

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        truck_info = {"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))}
        if i == 0:  # 第1辆充氧车（ID为0）发生故障不可用
            truck_info["status"] = "unavailable"
        oxygen_truck_resources.append(truck_info)
    return oxygen_truck_resources

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        if i == 5:  # 第6个任务，id为5
            location = (1, 2)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        towing_tasks.append({"id": i, "type": "towing", "location": location})
    return towing_tasks

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，前3架每隔三分钟到达一架，从第4架开始每隔六分钟到达一架，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    current_offset = 0
    for i in range(nums):
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + current_offset))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})

        if i + 1 < 3:
            current_offset += 3 * 60
        else:
            current_offset += 6 * 60
    return planes

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        # 第1辆加油车(id为0)发生故障不可用，跳过初始化
        if i == 0:
            continue
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fuel_truck_resources

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        # 第1辆气源车(id=0)发生故障不可用，跳过初始化
        if i == 0:
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources
