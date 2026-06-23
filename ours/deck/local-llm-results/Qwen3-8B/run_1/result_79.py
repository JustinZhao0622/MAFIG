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
        if i >=4:
            interval = 5 * 60
        else:
            interval = 3 * 60
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + interval * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes


def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        if i ==4:
            location = (random.randint(0, 3), random.randint(0, 10))
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
    mobile_resources.append({"id": 0, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    mobile_resources.append({"id": 1, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    mobile_resources.append({"id": 2, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    mobile_resources.append({"id": 3, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    mobile_resources.append({"id": 4, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    mobile_resources.append({"id": 5, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    mobile_resources.append({"id": 6, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    mobile_resources.append({"id": 7, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    mobile_resources.append({"id": 8, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    mobile_resources.append({"id": 9, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    mobile_resources.pop(4)
    return mobile_resources


def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i ==4:
            location = (0,4)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        tractor_resources.append({"id": i, "type": "tractor", "location": location})
    return tractor_resources


def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        if i ==4:
            location = (random.randint(0, 3), random.randint(0, 10))
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
    fuel_truck_resources.append({"id": 0, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    fuel_truck_resources.append({"id": 1, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    fuel_truck_resources.append({"id": 2, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    fuel_truck_resources.append({"id": 3, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    fuel_truck_resources.append({"id": 4, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    fuel_truck_resources.append({"id": 5, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    fuel_truck_resources.append({"id": 6, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    fuel_truck_resources.append({"id": 7, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    fuel_truck_resources.append({"id": 8, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    fuel_truck_resources.append({"id": 9, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    fuel_truck_resources.pop(4)
    return fuel_truck_resources


def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_truck_resources


def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        if i ==4:
            location = (random.randint(0, 3), random.randint(0, 10))
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
    oxygen_truck_resources.append({"id": 0, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    oxygen_truck_resources.append({"id": 1, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    oxygen_truck_resources.append({"id": 2, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    oxygen_truck_resources.append({"id": 3, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    oxygen_truck_resources.append({"id": 4, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    oxygen_truck_resources.append({"id": 5, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    oxygen_truck_resources.append({"id": 6, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    oxygen_truck_resources.append({"id": 7, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    oxygen_truck_resources.append({"id": 8, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    oxygen_truck_resources.append({"id": 9, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    oxygen_truck_resources.pop(4)
    return oxygen_truck_resources


def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        if i ==4:
            location = (2,8)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        power_cart_resources.append({"id": i, "type": "power_cart", "location": location})
    return
