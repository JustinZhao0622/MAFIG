import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i < 4:
            # 前4架舰载机，间隔3分钟
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        else:
            # 从第5架舰载机开始，间隔8分钟
            # 先计算前4架的总时间
            time_for_first_4 = 3 * 60 * 4
            # 计算第5架及以后的额外时间
            extra_time = 8 * 60 * (i - 4)
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + time_for_first_4 + extra_time))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes