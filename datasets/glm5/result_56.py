import heapq
import time
def init_stacking_zones(nums=4):
    """
    初始化货物堆积区域 (A, B, C, D 区)。
    每个区域包含：坐标、当前存放数量、最大容量。
    返回可用区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    zones = []
    for i in range(nums):
        stock = 0
        if i == 2:
            stock = 44
        zones.append({
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": stock,
            "max_capacity": 100,
            "desc": f"货物堆积区域{i+1}"
        })
    return zones