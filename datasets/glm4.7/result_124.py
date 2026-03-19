import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，前3架每隔三分钟到达一架，第4架开始每隔六分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i < 3:
            interval = 3 * 60
        else:
            interval = 6 * 60
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + interval * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes