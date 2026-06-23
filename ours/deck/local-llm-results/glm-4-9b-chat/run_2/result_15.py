import heapq
import time
import random

def init_planes(nums=5, start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i, 10)})
    # 修改舰载机到达间隔
    if i >= 5:
        planes[i]["time"] = time.strftime("%H:%M:%S", time.localtime(time.mktime(planes[i]["time"]) + 8 * 60))
    return planes

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 修改第2个固定资源初始位置
    if i == 1:
        fixed_resources[i]["location"] = (1, 6)
    return fixed_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 修改第2辆气源车、维修车、液压车、消防车初始位置
    if i == 1:
        mobile_resources[i]["type"] = "air_source_car"
        mobile_resources[i]["location"] = (1, 6)
    elif i == 2:
        mobile_resources[i]["type"] = "maintenance_vehicle"
        mobile_resources[i]["location"] = (1, 2)
    elif i == 3:
        mobile_resources[i]["type"] = "hydraulic_cart"
        mobile_resources[i]["location"] = (2, 7)
    elif i == 4:
        mobile_resources[i]["type"] = "fire_vehicle"
        mobile_resources[i]["location"] = (2, 7)
    return mobile_resources

# 其他函数保持不变
