import heapq
import time
import random

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10)), "available": True})
    # 标记第5辆气源车（id为4）为不可用
    air_source_car_resources[4]["available"] = False
    return air_source_car_resources

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 标记第5辆加油车（id为4）为不可用
    if len(fuel_truck_resources) > 4:
        fuel_truck_resources[4]["status"] = "unavailable"
    return fuel_truck_resources

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

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        if i == 4:  # 第5个资源（索引为4）
            fixed_resources.append({"id": i, "type": "crane", "location": (3, 3)})
        else:
            fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources

def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), random.randint(0, 10)), "available": True})
    # 标记第5辆维修车（id为4）为不可用
    maintenance_vehicle_resources[4]["available"] = False
    return maintenance_vehicle_resources

def init_hydraulic_cart_resources(nums=10):
    """初始化液压车资源，返回资源列表，每个资源包含id、类型"""
    hydraulic_cart_resources = []
    for i in range(nums):
        if i == 4:  # 第5辆液压车
            hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": (3, 8)})
        else:
            hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return hydraulic_cart_resources

