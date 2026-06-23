import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，前3架每隔三分钟到达一架，从第4架开始间隔改为8分钟，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i < 3:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        else:
            # 第4架及以后的飞机，使用8分钟间隔
            # 前三架的总时间是3*3=9分钟
            # 第4架飞机的时间是start_time + 9分钟 + 8分钟*(i-3)
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 9 * 60 + 8 * 60 * (i-3)))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes