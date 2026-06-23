import heapq
import time
import random

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        if i == 3:
            fixed_resources.append({"id": i, "type": "crane", "location": (2, 4)})
        else:
            fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources

def schedule_task(task, mobile_resources):
    """调度任务到可用的移动资源"""
    available_resources = [resource for resource in mobile_resources if resource["type"] == task["resource_type"] and resource["id"] != 3]
    if available_resources:
        selected_resource = heapq.heappop(available_resources)
        task["assigned_resource"] = selected_resource["id"]
        return task
    else:
        task["status"] = "failed"
        return task

def main():
    task = {"id": 1, "resource_type": "crane", "status": "pending"}
    mobile_resources = init_mobile_resources()
    scheduled_task = schedule_task(task, mobile_resources)
    print(scheduled_task)

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i == 3:
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (0, 0)})
        else:
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_vehicle_resources

