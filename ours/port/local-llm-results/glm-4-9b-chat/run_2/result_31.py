import heapq
import time
import random 

def init_cranes(nums=5,start_time="8:00:00"):
    """初始化船舶，每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        vessels.append({"time": vessel_time, "id": i, "duration": 10, "location": (i,10)})
    # 修改id为2的船舶任务时长
    if vessels[1]["id"] == 2:
        vessels[1]["duration"] = 20
    # 修改站位(9,8)的终点为(10,8)
    for vessel in vessels:
        if vessel["location"] == (9, 8):
            vessel["location"] = (10, 8)
    # 修改id为0的资源不可用
    # 修改站位(5,4)(6,4)(5,5)(6,5)四个点发生故障
    for i in range(4):
        vessels.append({"time": vessels[0]["time"], "id": i, "duration": 10, "location": (5, 4 + i)})
    # 第1艘到达的船舶延迟10分钟到达
    vessels[0]["time"] = time.strftime("%H:%M:%S", time.localtime(time.mktime(time.strptime(vessels[0]["time"], "%H:%M:%S")) + 10 * 60))
    return vessels

def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    for i in range(nums):
        resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    # id为0的资源不可用
    if resources[0]["id"] == 0:
        resources[0]["status"] = "unavailable"
    # 站位(5,4)(6,4)(5,5)(6,5)四个点发生故障
    for i in range(4):
        resources.append({"id": nums + i, "type": "crane", "location": (5, 4 + i), "status": "unavailable"})
    return resources

# 其他函数保持不变
