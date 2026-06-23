import heapq
import time
import random

def init_planes(nums=5, start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i >= 5:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 5 * 60 * (i - 4)))
        else:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
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
        if i != 2:
            mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources


def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if (i != 5 and i != 6 and i != 7 and i != 8):
            tractor_resources.append({"id": i, "type": "tractor", "location": (random.randint(0, 3), random.randint(0, 10))})
    return tractor_resources


def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        if i != 2:
            fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fuel_truck_resources


def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        if i != 2:
            air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources


def init_tasks(nums=6):
    """初始化挂载弹药任务，返回任务列表，每个任务包含id、类型"""
    tasks = []
    for i in range(nums):
        if (i != 5 and i != 6 and i != 7 and i != 8 and i != 2):
            tasks.append({"id": i, "type": "ammo", "location": (random.randint(0, 3), random.randint(0, 10))})
    return tasks

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        if i != 5:
            towing_tasks.append({"id": i, "type": "towing", "location": (random.randint(0, 3), random.randint(0, 10))})
    return towing_tasks


def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i != 2:
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_vehicle_resources


def init_nitrogen_filling_tasks(nums=6):
    """初始化加氮任务，返回任务列表，每个任务包含id、类型"""
    nitrogen_filling_tasks = []
    for i in range(nums):
        if i != 2:
            nitrogen_filling_tasks.append({"id": i, "type": "nitrogen_filling", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_filling_tasks


def init_oxygen_filling_tasks(nums=6):
    """初始化充氧任务，返回任务列表，每个任务包含id、类型"""
    oxygen_filling_tasks = []
    for i in range(nums):
        if i != 2:
            oxygen_filling_tasks.append({"id": i, "type": "oxygen_filling", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_filling_tasks


def init_power_supply_tasks(nums=6):
    """初始化供电任务，返回任务列表，每个任务包含id、类型"""
    power_supply_tasks = []
    for i in range(nums):
        if i != 2:
            power_supply_tasks.append({"id": i, "type": "power_supply", "location": (random.randint(0, 3), random.randint(0, 10))})
    return power_supply_tasks


def init_air_supply_tasks(nums=6):
    """初始化供气任务，返回任务列表，每个任务包含id、类型"""
    air_supply_tasks = []
    for i in range(nums):
        if i != 2:
            air_supply_tasks.append({"id": i, "type": "air_supply", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_supply_tasks


def init_hydraulic_support_tasks(nums=6):
    """初始化液压保障任务，返回任务列表，每个任务包含id、类型"""
    hydraulic_support_tasks = []
    for i in range(nums):
        if i != 2:
            hydraulic_support_tasks.append({"id": i, "type": "hydraulic_support", "location": (random.randint(0, 3), random.randint(0, 10))})
    return hydraulic_support_tasks


def init_maintenance_tasks(nums=6):
    """初始化维修保障任务，返回任务列表，每个任务包含id、类型"""
    maintenance_tasks = []
    for i in range(nums):
        if i != 2:
            maintenance_tasks.append({"id": i, "type": "maintenance", "location": (random.randint(0, 3), random.randint(0, 10))})
    return maintenance_tasks


def init_inspection_tasks(nums=6):
    """初始化检查任务，返回任务列表，每个任务包含id、类型"""
    inspection_tasks = []
    for i in range(nums):
        if i != 2:
            inspection_tasks.append({"id": i, "type": "inspection", "location": (random.randint(0, 3), random.randint(0, 10))})
    return inspection_tasks


def init_fire_watch_tasks(nums=6):
    """初始化消防监护任务，返回任务列表，每个任务包含id、类型"""
    fire_watch_tasks = []
    for i in range(nums):
        if i != 2:
            fire_watch_tasks.append({"id": i, "type": "fire_watch", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_watch_tasks
