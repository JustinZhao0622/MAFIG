import heapq
import time
import random

def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        resource = {
            "id": i, 
            "type": "maintenance_vehicle", 
            "location": (random.randint(0, 3), random.randint(0, 10))
        }
        # 应对突发事件：第2辆维修车（索引为1）发生故障不可用
        if i == 1:
            resource["status"] = "unavailable"
        else:
            resource["status"] = "available"
        maintenance_vehicle_resources.append(resource)
    return maintenance_vehicle_resources

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i == 1:
            loc = (0, 6)
        else:
            loc = (random.randint(0, 3), random.randint(0, 10))
        tractor_resources.append({"id": i, "type": "tractor", "location": loc})
    return tractor_resources

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        if i == 2:
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        towing_tasks.append({"id": i, "type": "towing", "location": (random.randint(0, 3), random.randint(0, 10))})

    # 突发事件应对：第6个牵引任务目标站位调整为(3,7)
    if nums >= 6:
        towing_tasks[5]["location"] = (3, 7)

    return towing_tasks

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        if i == 1:
            continue
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        # 突发事件：第2辆充氧车（id=1）发生故障不可用
        if i == 1:
            oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10)), "status": "unavailable"})
        else:
            oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_truck_resources

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    base_time = time.mktime(start_time)
    planes = []
    current_offset = 0
    for i in range(nums):
        if i > 0:
            if i < 3:
                current_offset += 3 * 60
            else:
                current_offset += 5 * 60
        plane_time = time.strftime("%H:%M:%S", time.localtime(base_time + current_offset))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        if i == 1:
            location = (2, 2)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        fixed_resources.append({"id": i, "type": "crane", "location": location})
    return fixed_resources
