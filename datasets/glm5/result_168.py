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
        
        # 处理突发事件约束
        if i == 0: # Zone_1
            current_stock = 48 # 当前库存增加48
        elif i == 1: # Zone_2
            max_capacity = 0 # 发生故障不可用，将容量置为0以拒绝新任务
            current_stock = 0
        elif i == 2: # Zone_3
            max_capacity = 135 # 最大容量缩减至135
            
        zones.append({
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": current_stock,
            "max_capacity": max_capacity,
            "desc": f"货物堆积区域{i+1}"
        })
    return zones