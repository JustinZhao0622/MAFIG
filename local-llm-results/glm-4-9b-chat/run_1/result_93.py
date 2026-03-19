import heapq
import time
import random

def init_planes(nums=5, start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i >= 2:  # 从第3架舰载机开始
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 5 * 60 * (i - 2)))
        else:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i, 10)})
    return planes

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), 3)})  # 调整第2个固定资源初始位置
    return fixed_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), 3)})  # 调整第2个移动资源初始位置
    return mobile_resources

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        tractor_resources.append({"id": i, "type": "tractor", "location": (random.randint(0, 3), 3)})  # 调整第2辆牵引车初始位置
    return tractor_resources

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), 3)})  # 调整第2辆加油车初始位置
    return fuel_truck_resources

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), 3)})  # 调整第2辆加氮车初始位置
    return nitrogen_truck_resources

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), 3)})  # 调整第2辆充氧车初始位置
    return oxygen_truck_resources

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        power_cart_resources.append({"id": i, "type": "power_cart", "location": (2, 3)})  # 调整第2辆供电车初始位置
    return power_cart_resources

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), 3)})  # 调整第2辆气源车初始位置
    return air_source_car_resources

def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), 3)})  # 调整第2辆维修车初始位置
    return maintenance_vehicle_resources

# 其他函数保持不变
