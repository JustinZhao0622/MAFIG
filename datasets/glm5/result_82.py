import heapq
import time
def init_stacking_zones(nums=4):
    """
    初始化货物堆积区域 (A, B, C, D 区)。
    每个区域包含：坐标、当前存放数量 (current_stock)、最大容量 (max_capacity)。
    返回可用区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    zones = []
    for i in range(nums):
        zone_id = i + 1
        
        if zone_id == 4:
            continue
            
        zone = {
            "id": f"Zone_{zone_id}",
            "location": (0,25),
            "current_stock": 0,
            "max_capacity": 100,
            "desc": f"货物堆积区域{zone_id}"
        }
        
        if zone_id == 1:
            zone["max_capacity"] = 64
            
        if zone_id == 3:
            zone["current_stock"] = 44
            
        zones.append(zone)
    return zones