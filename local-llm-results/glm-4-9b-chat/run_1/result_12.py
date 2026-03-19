import heapq
import time
import random

def init_planes(nums=5, start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i >= 4:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 5 * 60 * (i - 4)))
        else:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i, 10)})
    return planes

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 修改第4个固定资源初始位置
    fixed_resources[3] = {"id": 3, "type": "crane", "location": (2, 7)}
    return fixed_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 修改第4辆供电车初始位置
    mobile_resources[3] = {"id": 3, "type": "power_cart", "location": (3, 0)}
    return mobile_resources

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        tractor_resources.append({"id": i, "type": "tractor", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 修改第5个牵引任务目标站位
    tractor_resources[4] = {"id": 4, "type": "tractor", "location": (1, 0)}
    return tractor_resources

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 修改第4辆加氮车初始位置
    nitrogen_truck_resources[3] = {"id": 3, "type": "nitrogen_truck", "location": (2, 5)}
    return nitrogen_truck_resources

# 其他函数保持不变
