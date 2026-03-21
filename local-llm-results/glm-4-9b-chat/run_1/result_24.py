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
        if i >= 6:  # 从第7辆货车开始
            arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 8 * 60 * (i - 6)))
        else:
            arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks

# 其他函数保持不变
# ...

# 修改Forklift_1叉车初始位置
def init_forklifts(nums=3):
    forklifts = []
    for i in range(nums):
        if i == 0:  # 修改Forklift_1的初始位置
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (46, 48),
            })
        else:
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (0, 25),
            })
    return forklifts

# 修改Zone_3堆积区当前库存
def init_stacking_zones(nums=4):
    zones = []
    for i in range(nums):
        if i == 2:  # 修改Zone_3的当前库存
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0, 25),
                "current_stock": 24,
                "max_capacity": 100,
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

# 修改Zone_3堆积区为不可用
def init_stacking_zones(nums=4):
    zones = []
    for i in range(nums):
        if i == 2:  # 修改Zone_3为不可用
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0, 25),
                "current_stock": 24,
                "max_capacity": 100,
                "desc": f"货物堆积区域{i+1}",
                "status": "unavailable"
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

# 其他函数保持不变
# ...
