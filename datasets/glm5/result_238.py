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
        current_stock = 0
        max_capacity = 100
        
        # 突发事件应对：Zone_3堆积区当前库存增加58
        if i == 2:
            current_stock = 58
            
        # 突发事件应对：Zone_2堆积区最大容量缩减至105
        if i == 1:
            max_capacity = 105
            
        zones.append({
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": current_stock,
            "max_capacity": max_capacity,
            "desc": f"货物堆积区域{i+1}"
        })
    return zones