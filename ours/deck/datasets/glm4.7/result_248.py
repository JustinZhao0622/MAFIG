import heapq
import time
import random

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 突发事件：第3辆加氮车初始位置调整为(1,8)
    if len(nitrogen_truck_resources) >= 3:
        nitrogen_truck_resources[2]["location"] = (1, 8)
    return nitrogen_truck_resources