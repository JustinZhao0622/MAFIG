import heapq
import time
import random

def init_planes(nums=5, start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i == 2:  # 从第3架舰载机开始
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 6 * 60 * (i - 2)))
        else:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i, 10)})
    return planes

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        if i == 4:  # 第5辆液压车
            mobile_resources.append({"id": i, "type": "hydraulic_cart", "location": (0, 3)})
        elif i == 5:  # 第5辆气源车
            continue  # 不可用，跳过
        elif i == 6:  # 第5辆维修车
            continue  # 不可用，跳过
        elif i == 7:  # 第5辆加氮车
            mobile_resources.append({"id": i, "type": "nitrogen_truck", "location": (1, 9)})
        elif i == 8:  # 第5辆充氧车
            continue  # 不可用，跳过
        elif i == 9:  # 第5个固定保障资源
            mobile_resources.append({"id": i, "type": "crane", "location": (3, 2)})
        elif i == 10:  # 第5辆供电车
            mobile_resources.append({"id": i, "type": "power_cart", "location": (2, 6)})
        else:
            mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources
