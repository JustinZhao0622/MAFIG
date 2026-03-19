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
        zone_id = f"Zone_{i+1}"
        
        # 突发事件处理：Zone_4故障不可用，跳过创建
        if zone_id == "Zone_4":
            continue
            
        zone = {
            "id": zone_id,
            "location": (0,25),
            "current_stock": 0,
            "max_capacity": 100,
            "desc": f"货物堆积区域{i+1}"
        }
        
        # 突发事件处理：Zone_2容量缩减至124
        if zone_id == "Zone_2":
            zone["max_capacity"] = 124
            
        zones.append(zone)
    return zones