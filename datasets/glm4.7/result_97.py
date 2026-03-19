import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，前5架每隔三分钟到达，从第6架开始每隔8分钟到达，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i < 5:
            # 前5架保持3分钟间隔
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        else:
            # 第6架及以后使用8分钟间隔
            # 计算上一架飞机的时间
            last_plane_time = time.strptime(planes[-1]["time"], "%H:%M:%S")
            # 当前飞机时间 = 上一架飞机时间 + 8分钟
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(last_plane_time) + 8 * 60))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes