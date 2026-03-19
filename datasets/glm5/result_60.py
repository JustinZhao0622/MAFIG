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
        current_stock = 0
        max_capacity = 100
        desc = f"货物堆积区域{i+1}"

        if i == 1:  # Zone_2
            # Zone_2堆积区发生故障不可用，设置最大容量为0或标记状态
            # 此处通过设置max_capacity为0使其逻辑上不可用
            max_capacity = 0
            desc = f"货物堆积区域{i+1}(故障)"

        if i == 2:  # Zone_3
            # Zone_3堆积区当前库存增加61
            current_stock = 61

        zones.append({
            "id": zone_id,
            "location": (0,25),
            "current_stock": current_stock,
            "max_capacity": max_capacity,
            "desc": desc
        })
    return zones