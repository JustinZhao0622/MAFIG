import heapq
import time
import random

def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    
    # 第3辆维修车发生故障不可用
    if len(maintenance_vehicle_resources) > 2:
        maintenance_vehicle_resources[2]["location"] = None
    
    return maintenance_vehicle_resources