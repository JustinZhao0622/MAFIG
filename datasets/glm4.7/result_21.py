import heapq
import time
import random

def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        # 初始化可用性状态
        is_available = True
        # 第4辆维修车(id=4)标记为不可用
        if i == 4:
            is_available = False
        maintenance_vehicle_resources.append({
            "id": i, 
            "type": "maintenance_vehicle", 
            "location": (random.randint(0, 3), random.randint(0, 10)),
            "is_available": is_available
        })
    return maintenance_vehicle_resources