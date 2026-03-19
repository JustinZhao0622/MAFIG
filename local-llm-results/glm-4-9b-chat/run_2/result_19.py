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
    # 修改牵引任务目标站位
    planes[3]["location"] = (0, 0)
    planes[5]["location"] = (13, 12)
    return planes

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 修改第2辆维修车、加氮车、充氧车、加油车的初始位置
    mobile_resources[1]["location"] = (1, 5)
    return mobile_resources

def init_maintenance_tasks(nums=6):
    """初始化维修保障任务，返回任务列表，每个任务包含id、类型"""
    maintenance_tasks = []
    for i in range(nums):
        maintenance_tasks.append({"id": i, "type": "maintenance", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 修改维修任务目标站位
    maintenance_tasks[1]["location"] = (0, 0)
    maintenance_tasks[5]["location"] = (13, 12)
    return maintenance_tasks

# 其他函数保持不变
