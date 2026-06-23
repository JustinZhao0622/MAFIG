import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，前3架每隔三分钟到达一架，从第4架开始每隔八分钟到达一架，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i < 3:  # 前3架舰载机使用3分钟间隔
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        else:  # 从第4架开始使用8分钟间隔
            # 前3架的总时间是 3 * 3 = 9分钟，之后每架增加8分钟
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * 3 + 8 * 60 * (i - 3)))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes