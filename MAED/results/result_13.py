import heapq
import time
import random

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        if i == 2:  # 假设第3辆气源车发生故障，不添加到资源列表中
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        # 根据突发事件描述，将第3辆加氮车的初始位置调整为(0,6)
        if i == 2:
            location = (0, 6)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": location})
    return nitrogen_truck_resources

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i == 2:  # 突发事件约束：第3辆消防车初始位置调整为(1,3)
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (1, 3)})
        else:
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_vehicle_resources

def init_hydraulic_cart_resources(nums=10):
    """初始化液压车资源，返回资源列表，每个资源包含id、类型"""
    hydraulic_cart_resources = []
    for i in range(nums):
        if i == 2:  # 确保第3辆液压车的位置调整为(3,8)
            hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": (3, 8)})
        else:
            hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return hydraulic_cart_resources

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        if i == 2:
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (2, 8)})
        else:
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return power_cart_resources

