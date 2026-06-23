import heapq
import time
import random

def init_stacking_zones(nums=4):
    """
    初始化货物堆积区域 (A, B, C, D 区)。
    每个区域包含：坐标、当前存放数量 (current_stock)、最大容量 (max_capacity)。
    返回可用区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    zones = []
    for i in range(nums):
        if i == 2:
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 122,
                "desc": f"货物堆积区域{i+1}"
            })
        else:
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 100,
                "desc": f"货物堆积区域{i+1}"
            })
    return zones

def update_stock(zones, zone_id, stock_change):
    for zone in zones:
        if zone["id"] == zone_id:
            if zone["current_stock"] + stock_change > zone["max_capacity"]:
                raise Exception(f"超出最大容量: {zone_id} 当前库存: {zone['current_stock']} + 变化量: {stock_change} > 最大容量: {zone['max_capacity']}")
            zone["current_stock"] += stock_change
            break

zones = init_stacking_zones()
update_stock(zones, "Zone_3", 42)

