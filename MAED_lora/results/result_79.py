import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，前4架每隔三分钟到达，从第5架开始每隔5分钟到达，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i < 4:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        else:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * 3 + 5 * 60 * (i - 3)))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes

def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), random.randint(0, 10)), "available": True})
    # 标记第5辆维修车（id为4）为不可用
    maintenance_vehicle_resources[4]["available"] = False
    return maintenance_vehicle_resources

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10)), "available": True})
    # 标记第5辆充氧车（id为4）为不可用
    oxygen_truck_resources[4]["available"] = False
    return oxygen_truck_resources

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i == 4:  # 第5辆消防车
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (0, 6)})
        else:
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_vehicle_resources

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        if i == 4:  # 第5辆供电车
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (2, 8)})
        else:
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return power_cart_resources

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 标记第5辆加油车（id为4）为不可用
    if len(fuel_truck_resources) > 4:
        fuel_truck_resources[4]["status"] = "unavailable"
    return fuel_truck_resources

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i == 4:  # 第5辆牵引车
            tractor_resources.append({"id": i, "type": "tractor", "location": (0, 4)})
        else:
            tractor_resources.append({"id": i, "type": "tractor", "location": (random.randint(0, 3), random.randint(0, 10))})
    return tractor_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        resource = {"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))}
        if i == 4:  # 第5个资源（索引为4）发生故障
            resource["status"] = "unavailable"
        else:
            resource["status"] = "available"
        mobile_resources.append(resource)
    return mobile_resources

