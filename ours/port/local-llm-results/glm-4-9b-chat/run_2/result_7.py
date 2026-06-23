import heapq
import time
import random 

def init_cranes(nums=5,start_time="8:00:00"):
    """初始化船舶，每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        vessels.append({"time": vessel_time, "id": i, "duration": 10, "location": (i,10)})
    # 修改：第1艘船舶延迟10分钟到达
    vessels[0]["time"] = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i + 10))
    return vessels

def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    for i in range(nums):
        resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 修改：站位(6,5)(7,5)(6,6)(7,6)四个点发生故障
    for resource in resources:
        if resource["location"] in [(6,5), (7,5), (6,6), (7,6)]:
            resource["status"] = "unavailable"
    return resources

def init_trucks(nums=8):
    """初始化集卡车队，返回车辆列表，每辆车包含id、位置、状态"""
    trucks = []
    for i in range(nums):
        trucks.append({
            "id": f"Truck_{i+1}",
            "location": (random.randint(0, 20), random.randint(0, 20)),
            "status": "idle",
        })
    return trucks

def init_yard_blocks(nums=6):
    """初始化堆场区块，返回区块列表，每个区块包含id、容量、当前占用"""
    yard_blocks = []
    for i in range(nums):
        yard_blocks.append({
            "id": f"Block_{i+1}",
            "capacity": 100,
            "occupied": random.randint(0, 60),
        })
    return yard_blocks

def init_berths(nums=4):
    """初始化泊位，返回泊位列表，每个泊位包含id、位置、状态"""
    berths = []
    for i in range(nums):
        berths.append({
            "id": f"Berth_{i+1}",
            "location": (i * 10, 0),
            "status": "available",
        })
    # 修改：id为5的资源不可用
    for berth in berths:
        if berth["id"] == "Berth_5":
            berth["status"] = "unavailable"
    return berths

def init_containers(nums=12):
    """初始化集装箱，返回集装箱列表，每个集装箱包含id、位置、类型"""
    containers = []
    for i in range(nums):
        containers.append({
            "id": f"Container_{i+1}",
            "location": (random.randint(0, 10), random.randint(0, 10)),
            "type": "general",
        })
    return containers

def init_loading_tasks(nums=10):
    """初始化装卸任务，返回任务列表，每个任务包含id、目标资源、状态"""
    loading_tasks = []
    for i in range(nums):
        loading_tasks.append({
            "id": f"Task_{i+1}",
            "target": f"Container_{(i % 12) + 1}",
            "status": "waiting",
        })
    # 修改：id为3的船舶任务时长延长至20分钟
    for task in loading_tasks:
        if task["target"].startswith("Container_3"):
            task["duration"] = 20
    return loading_tasks
