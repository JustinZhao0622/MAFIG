import heapq
import time
import random

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        towing_tasks.append({"id": i, "type": "towing", "location": (random.randint(0, 3), random.randint(0, 10))})
    # 修改第5个牵引任务的目标站位为(2,2)
    if len(towing_tasks) >= 5:
        towing_tasks[4]["location"] = (2, 2)
    return towing_tasks