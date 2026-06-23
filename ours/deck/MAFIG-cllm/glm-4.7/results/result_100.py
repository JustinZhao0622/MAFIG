import heapq
import time
import random

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i == 0:
            loc = (0, 2)
        else:
            loc = (random.randint(0, 3), random.randint(0, 10))
        tractor_resources.append({"id": i, "type": "tractor", "location": loc})
    return tractor_resources

def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        if i == 0:  # 第1辆维修车发生故障不可用
            continue
        maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return maintenance_vehicle_resources

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    current_offset = 0
    for i in range(nums):
        if i > 0:
            if i >= 3:
                current_offset += 8
            else:
                current_offset += 3
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + current_offset * 60))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        # 突发事件：第1辆气源车（ID为0）发生故障不可用
        if i == 0:
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        if i == 0:
            location = (3, 3)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": location})
    return nitrogen_truck_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        resource = {"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))}
        if i == 0:
            resource["status"] = "fault"
        mobile_resources.append(resource)
    return mobile_resources

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i == 0:
            location = (0, 8)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": location})
    return fire_vehicle_resources

def init_hydraulic_cart_resources(nums=10):
    """初始化液压车资源，返回资源列表，每个资源包含id、类型"""
    hydraulic_cart_resources = []
    for i in range(nums):
        if i == 0:
            location = (1, 1)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": location})
    return hydraulic_cart_resources
