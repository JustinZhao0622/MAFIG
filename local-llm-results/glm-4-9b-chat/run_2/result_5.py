import heapq
import time

# 货车到达时间
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    for i in range(nums):
        if i >= 2:  # 从第3辆货车开始间隔改为6分钟
            arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 6 * 60 * (i - 2)))
        else:
            arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks

def init_stacking_zones(nums=4):
    """
    初始化货物堆积区域 (A, B, C, D 区)。
    每个区域包含：坐标、当前存放数量 (current_stock)、最大容量 (max_capacity)。
    返回可用区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    zones = []
    for i in range(nums):
        if i == 2:  # Zone_2堆积区最大容量缩减至133
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0, 25),
                "current_stock": 0,
                "max_capacity": 133,
                "desc": f"货物堆积区域{i+1}"
            })
        else:
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0, 25),
                "current_stock": 0,
                "max_capacity": 100,
                "desc": f"货物堆积区域{i+1}"
            })
    return zones

def init_inventory_records(nums=10):
    """
    初始化库存记录。
    返回库存记录列表，每条记录包含id、sku、数量
    """
    records = []
    for i in range(nums):
        if i == 2:  # Zone_2堆积区当前库存增加75
            records.append({
                "id": f"Inventory_{i+1}",
                "sku": f"SKU_{i+1}",
                "quantity": 175,
            })
        else:
            records.append({
                "id": f"Inventory_{i+1}",
                "sku": f"SKU_{i+1}",
                "quantity": 100,
            })
    return records
