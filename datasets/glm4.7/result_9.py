import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，前5架每隔三分钟到达一架，从第6架开始每隔8分钟到达一架，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i < 5:
            interval = 3
        else:
            interval = 8
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + interval * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes