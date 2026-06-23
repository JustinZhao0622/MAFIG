import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，前4架舰载机每隔三分钟到达，从第5架开始改为每6分钟到达，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i < 4:
            # 前4架保持3分钟间隔
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        else:
            # 从第5架开始改为6分钟间隔
            # 先计算前4架的总时间累积
            base_time = time.mktime(start_time) + 3 * 60 * 4
            # 然后加上6分钟的间隔
            plane_time = time.strftime("%H:%M:%S", time.localtime(base_time + 6 * 60 * (i - 4)))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes