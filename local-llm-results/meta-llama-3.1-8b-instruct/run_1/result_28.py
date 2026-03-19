基于突发事件的描述，需要对以下资源进行调整：

*   第2个固定保障资源初始位置调整为(1,9)
*   第2辆牵引车初始位置调整为(3,2)
*   第2个通用移动资源发生故障不可用
*   第2辆加油车发生故障不可用

以下是修改后的代码：


"""
原子函数库 —— 甲板舰载机调度
"""
import heapq
import time
import random


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
    fixed_resources = []
    for i in range(nums):
        if i == 1:  # 第2个固定保障资源初始位置调整为(1,9)
            fixed_resources.append({"id": i, "type": "crane", "location": (1, 9)})
        else:
            fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        if i == 1:  # 第2个通用移动资源发生故障不可用
            continue
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources


def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i == 1:  # 第2辆牵引车初始位置调整为(3,2)
            tractor_resources.append({"id": i, "type": "tractor", "location": (3, 2)})
        else:
            tractor_resources.append({"id": i, "type": "tractor", "location": (random.randint(0, 3), random.randint(0, 10))})
    return tractor_resources


def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        if i == 1:  # 第2辆加油车发生故障不可用
            continue
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fuel_truck_resources


# ... (其他函数保持不变)


以上修改仅在 `init_fixed_resources()`, `init_mobile_resources()`, `init_tractor_resources()`, `init_fuel_truck_resources()` 函数中进行了调整，以满足突发事件的要求。
