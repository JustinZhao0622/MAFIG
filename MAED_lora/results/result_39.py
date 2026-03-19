import heapq
import time
import random

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        if i == 0:
            fixed_resources.append({"id": i, "type": "crane", "location": (3, 5)})
        else:
            fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources

def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        resource = {"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))}
        if i == 0:  # 第1辆维修车发生故障不可用
            resource["available"] = False
        else:
            resource["available"] = True
        maintenance_vehicle_resources.append(resource)
    return maintenance_vehicle_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        resource = {"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))}
        # 第1个通用移动资源发生故障不可用
        if i == 0:
            resource["available"] = False
        else:
            resource["available"] = True
        mobile_resources.append(resource)
    return mobile_resources

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10)), "available": True})
    # 标记第1辆气源车（id=0）为不可用
    if len(air_source_car_resources) > 0:
        air_source_car_resources[0]["available"] = False
    return air_source_car_resources

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i == 0:
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (2, 6)})
        else:
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_vehicle_resources

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        resource = {"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))}
        # 第1辆充氧车（id=0）发生故障不可用
        if i == 0:
            resource["status"] = "unavailable"
        else:
            resource["status"] = "available"
        oxygen_truck_resources.append(resource)
    return oxygen_truck_resources

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10)), "available": True})
    # 第1辆加油车发生故障不可用
    fuel_truck_resources[0]["available"] = False
    return fuel_truck_resources

