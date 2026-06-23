import heapq
import time
import random

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        towing_tasks.append({"id": i, "type": "towing", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 根据突发事件，将第2个牵引任务的目标站位调整为(2,3)
    towing_tasks[1]["location"] = (2, 3)
    return towing_tasks