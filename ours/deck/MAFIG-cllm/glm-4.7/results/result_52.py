import heapq
import time
import random

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        if i == 1:
            location = (2, 8)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        power_cart_resources.append({"id": i, "type": "power_cart", "location": location})
    return power_cart_resources

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        # 第2辆气源车（id为2）发生故障不可用，跳过初始化
        if i == 2:
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        if i == 1:
            continue
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fuel_truck_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        # 突发事件：第2个通用移动资源（id为1）发生故障不可用，跳过初始化
        if i == 1:
            continue
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i == 1:
            loc = (3, 9)
        else:
            loc = (random.randint(0, 3), random.randint(0, 10))
        tractor_resources.append({"id": i, "type": "tractor", "location": loc})
    return tractor_resources

def init_hydraulic_cart_resources(nums=10):
    """初始化液压车资源，返回资源列表，每个资源包含id、类型"""
    hydraulic_cart_resources = []
    for i in range(nums):
        if i == 1:
            location = (0, 6)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": location})
    return hydraulic_cart_resources
