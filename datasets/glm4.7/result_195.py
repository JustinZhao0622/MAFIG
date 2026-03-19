import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，前6架每隔三分钟到达，之后每6分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        if i < 6:
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        else:
            # 前6架总耗时为 3*60*5 = 900秒 (因为索引0不增加时间)
            # 然后每架增加6分钟
            plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * 6 + 6 * 60 * (i - 6)))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes