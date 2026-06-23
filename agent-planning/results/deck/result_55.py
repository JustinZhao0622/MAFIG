```python
import heapq
import time
import random


def init_planes(nums=5, start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        plane_time = time.strftime(
            "%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i)
        )
        planes.append(
            {"time": plane_time, "id": i, "duration": 10, "location": (i, 10)}
        )
    return planes


def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        if (i // 2, i % 2) not in [(8, 7), (9, 7), (8, 8), (9, 8)]:
            fixed_resources.append(
                {
                    "id": i,
                    "type": "crane",
                    "location": (i // 2, i % 2),
                }
            )
    return fixed_resources


def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        if (i // 2, i % 2) not in [(8, 7), (9, 7), (8, 8), (9, 8)]:
            mobile_resources.append(
                {
                    "id": i,
                    "type": "crane",
                    "location": (i // 2, i % 2),
                }
            )
    return mobile_resources


def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if (i // 2, i % 2) not in [(8,
