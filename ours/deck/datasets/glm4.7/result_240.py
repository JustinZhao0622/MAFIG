import heapq
import time
import random

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    
    # 标记第3辆充氧车为故障不可用
    for resource in oxygen_truck_resources:
        if resource["id"] == 3:
            resource["status"] = "fault"
            break
            
    return oxygen_truck_resources