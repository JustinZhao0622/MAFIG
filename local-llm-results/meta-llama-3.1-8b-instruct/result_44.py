突发事件描述：Zone_1堆积区最大容量缩减至77;Zone_2堆积区当前库存增加51;从第4辆货车开始间隔改为6分钟

基于突发事件描述，需要修改的代码是`init_stacking_zones`函数和`init_truck_arrival_time`函数。


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
        if i >= 3:  # 从第4辆货车开始间隔改为6分钟
            interval = 6 * 60
        else:
            interval = 3 * 60
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + interval * i))
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
        if i == 0:  # Zone_1最大容量缩减至77
            max_capacity = 77
        elif i == 1:  # Zone_2当前库存增加51
            current_stock = 51
        else:
            max_capacity = 100
            current_stock = 0
        zones.append({
            "id": f"Zone_{i+1}",
            "location": (0,25),
            "current_stock": current_stock,
            "max_capacity": max_capacity,
            "desc": f"货物堆积区域{i+1}"
        })
    return zones
