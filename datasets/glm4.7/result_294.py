import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，前4架每隔三分钟到达一架，第5架开始每隔8分钟到达一架，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i < 4:
            # 前4架飞机，间隔3分钟
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        else:
            # 第5架及以后的飞机，间隔8分钟
            # 前4架的总时间是3*60*4秒，之后每架增加8分钟
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * 4 + 8 * 60 * (i - 4)))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes