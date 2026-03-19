import heapq
import time
import random

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        if i == 0:  # 第1辆加氮车
            nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (2, 3)})
        else:  # 其他加氮车随机位置
            nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_truck_resources