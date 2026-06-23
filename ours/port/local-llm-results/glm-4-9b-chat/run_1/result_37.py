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
    # 修改id为2的船舶任务时长延长至20分钟
    if i == 1:
        vessels[i]["duration"] = 20
    return vessels

def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    for i in range(nums):
        resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 站位(8,9)发生故障，以该点为终点的调整为(9,9)
    for resource in resources:
        if resource["location"] == (8, 9):
            resource["location"] = (9, 9)
    # 站位(6,3)(7,3)(6,4)(7,4)四个点发生故障
    for resource in resources:
        if resource["location"] in [(6, 3), (7, 3), (6, 4), (7, 4)]:
            resource["location"] = None
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
    # 第0艘到达的船舶延迟10分钟到达
    if i == 0:
        trucks[0]["location"] = (random.randint(0, 20), random.randint(0, 20))
    return trucks

def init_containers(nums=12):
    """初始化集装箱，返回集装箱列表，每个集装箱包含id、位置、类型"""
    containers = []
    for i in range(nums):
        containers.append({
            "id": f"Container_{i+1}",
            "location": (random.randint(0, 10), random.randint(0, 10)),
            "type": "general",
        })
    # id为5的资源不可用
    for container in containers:
        if container["id"] == "Container_5":
            container["location"] = None
    return containers
