import heapq
import time
import random

"""
原子函数库 —— 甲板舰载机调度
"""





def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i >= 3:
            interval = 8 * 60
        else:
            interval = 3 * 60
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + interval * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes


def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    faulty_points = {(6,4), (7,4), (6,5), (7,5)}
    fixed_resources = []
    for i in range(nums):
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 10)
            if (x, y) not in faulty_points:
                break
        fixed_resources.append({"id": i, "type": "crane", "location": (x, y)})
    return fixed_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    faulty_points = {(6,4), (7,4), (6,5), (7,5)}
    mobile_resources = []
    for i in range(nums):
        if i == 0:
            continue
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 10)
            if (x, y) not in faulty_points:
                break
        mobile_resources.append({"id": i, "type": "crane", "location": (x, y)})
    return mobile_resources


def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    faulty_points = {(6,4), (7,4), (6,5), (7,5)}
    tractor_resources = []
    for i in range(nums):
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 10)
            if (x, y) not in faulty_points:
                break
        tractor_resources.append({"id": i, "type": "tractor", "location": (x, y)})
    return tractor_resources


def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    faulty_points = {(6,4), (7,4), (6,5), (7,5)}
    fuel_truck_resources = []
    for i in range(nums):
        if i == 0:
            continue
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 10)
            if (x, y) not in faulty_points:
                break
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (x, y)})
    return fuel_truck_resources


def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    faulty_points = {(6,4), (7,4), (6,5), (7,5)}
    nitrogen_truck_resources = []
    for i in range(nums):
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 10)
            if (x, y) not in faulty_points:
                break
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (x, y)})
    return nitrogen_truck_resources


def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    faulty_points = {(6,4), (7,4), (6,5), (7,5)}
    oxygen_truck_resources = []
    for i in range(nums):
        if i == 0:
            continue
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 10)
            if (x, y) not in faulty_points:
                break
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (x, y)})
    return oxygen_truck_resources


def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    faulty_points = {(6,4), (7,4), (6,5), (7,5)}
    power_cart_resources = []
    for i in range(nums):
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 10)
            if (x, y) not in faulty_points:
                break
        power_cart_resources.append({"id": i, "type": "power_cart", "location": (x, y)})
    return power_cart_resources


def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    faulty_points = {(6,4), (7,4), (6,5), (7,5)}
    air_source_car_resources = []
    for i in range(nums):
        if i == 0:
            continue
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 10)
            if (x, y) not in faulty_points:
                break
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (x, y)})
    return air_source_car_resources


def init_hydraulic_cart_resources(nums=10):
    """初始化液压车资源，返回资源列表，每个资源包含id、类型"""
    faulty_points = {(6,4), (7,4), (6,5), (7,5)}
    hydraulic_cart_resources = []
    for i in range(nums):
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 10)
            if (x, y) not in faulty_points:
                break
        hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": (x, y)})
    return hydraulic_cart_resources


def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    faulty_points = {(6,4), (7,4), (6,5), (7,5)}
    maintenance_vehicle_resources = []
    for i in range(nums):
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 10)
            if (x, y) not in faulty_points:
                break
        maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (x, y)})
    return maintenance_vehicle_resources


def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
