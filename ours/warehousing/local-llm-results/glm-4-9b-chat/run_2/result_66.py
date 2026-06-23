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
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * (i + 6)))  # 修改起始点为第7辆货车
        trucks.append({
            "id": f"Truck_{i+7}",  # 修改id从Truck_7开始
            "arrival_time": arrival_time,
        })
    return trucks

# 初始化货物堆积区域 (A, B, C, D 区)
def init_stacking_zones(nums=4):
    """
    初始化货物堆积区域 (A, B, C, D 区)。
    每个区域包含：坐标、当前存放数量 (current_stock)、最大容量 (max_capacity)。
    返回可用区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    zones = []
    for i in range(nums):
        zones.append({
            "id": f"Zone_{i+1}",
            "location": (0, 25),
            "current_stock": 0 if i != 3 else 31,  # 修改Zone_4的当前库存为31
            "max_capacity": 100,
            "desc": f"货物堆积区域{i+1}"
        })
    return zones

# 初始化叉车队
def init_forklifts(nums=3):
    """
    初始化叉车队。
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": (0, 25) if i not in [3, 4] else (0, 0),  # 修改故障叉车坐标
        })
    return forklifts

# 初始化装货月台
def init_loading_docks(nums=4):
    """
    初始化装货月台。
    返回月台列表，每个月台包含id、位置、状态
    """
    docks = []
    for i in range(nums):
        docks.append({
            "id": f"Dock_{i+1}",
            "location": (i * 5, 0),
            "status": "idle" if i not in [3] else "failed",  # 修改Zone_4的月台状态为failed
        })
    return docks
