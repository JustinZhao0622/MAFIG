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
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes


def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    faulty_points = [(8,5), (9,5), (8,6), (9,6)]
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
    faulty_points = [(8,5), (9,5), (8,6), (9,6)]
    mobile_resources = []
    for i in range(nums):
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 10)
            if (x, y) not in faulty_points:
                break
        mobile_resources.append({"id": i, "type": "crane", "location": (x, y)})
    return mobile_resources


def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    faulty_points = [(8,5), (9,5), (8,6), (9,6)]
    tractor_resources = []
    for i in range(nums):
        if i == 1:
            location = (3, 8)
        else:
            while True:
                x = random.randint(0, 3)
                y = random.randint(0, 10)
                if (x, y) not in faulty_points:
                    break
            location = (x, y)
        tractor_resources.append({"id": i, "type": "tractor", "location": location})
    return tractor_resources


def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    faulty_points = [(8,5), (9,5), (8,6), (9,6)]
    fuel_truck_resources = []
    for i in range(nums):
        if i == 1:
            location = (random.randint(0, 3), random.randint(0, 10))
            while location in faulty_points:
                location = (random.randint(0, 3), random.randint(0, 10))
            fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": location, "available": False})
        else:
            while True:
                x = random.randint(0, 3)
                y = random.randint(0, 10)
                if (x, y) not in faulty_points:
                    break
            fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (x, y), "available": True})
    return fuel_truck_resources


def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    faulty_points = [(8,5), (9,5), (8,6), (9,6)]
    nitrogen_truck_resources = []
    for i in range(nums):
        while True:
            x = random.randint(0, 3)
            y
