import heapq
import time
import random

def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})

    # 应对突发事件：第2辆维修车发生故障不可用
    # 假设第2辆对应id为2的车辆
    for vehicle in maintenance_vehicle_resources:
        if vehicle["id"] == 2:
            vehicle["status"] = "unavailable"
            break

    return maintenance_vehicle_resources

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        if i == 1:
            location = (0, 5)
        else:
            location = (random.randint(0, 3), random.randint(0, 10))
        power_cart_resources.append({"id": i, "type": "power_cart", "location": location})
    return power_cart_resources

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        # 突发事件：从第5架舰载机（索引4）开始，到达间隔改为6分钟
        # 前4架（索引0-3）保持3分钟间隔
        if i < 4:
            offset_seconds = i * 3 * 60
        else:
            # 第4架（索引3）的时间点为 3*3*60 = 540秒 (9分钟)
            # 从第5架（索引4）开始，间隔变为6分钟
            offset_seconds = (3 * 3 * 60) + ((i - 3) * 6 * 60)

        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + offset_seconds))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        if i == 1:
            nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (3, 9)})
        else:
            nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_truck_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        if i == 1:
            continue
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        # 第2辆气源车（索引为1）发生故障不可用，跳过初始化
        if i == 1:
            continue
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources
