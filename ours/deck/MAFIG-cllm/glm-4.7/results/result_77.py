import heapq
import time
import random

def init_hydraulic_cart_resources(nums=10):
    """初始化液压车资源，返回资源列表，每个资源包含id、类型"""
    hydraulic_cart_resources = []
    for i in range(nums):
        if i == 0:
            location = (1, 5)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": location})
    return hydraulic_cart_resources

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i == 0:
            location = (3, 3)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": location})
    return fire_vehicle_resources

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        if i == 0:
            location = (2, 6)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": location})
    return nitrogen_truck_resources

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        # 应对突发事件：第1辆气源车（ID为0）发生故障不可用
        if i == 0:
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i == 0:
            location = (1, 6)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        tractor_resources.append({"id": i, "type": "tractor", "location": location})
    return tractor_resources

def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        # 应对突发事件：第1辆维修车(id=0)发生故障不可用，跳过初始化
        if i == 0:
            continue
        maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return maintenance_vehicle_resources
