import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，前两架每隔三分钟到达，从第三架开始每隔五分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    
    # 使用秒数来跟踪时间
    current_time = time.mktime(start_time)
    
    # 前2架舰载机，使用3分钟间隔
    for i in range(2):
        plane_time = time.strftime("%H:%M:%S", time.localtime(current_time))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
        current_time += 3 * 60
    
    # 从第3架开始，使用5分钟间隔
    for i in range(2, nums):
        plane_time = time.strftime("%H:%M:%S", time.localtime(current_time))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
        current_time += 5 * 60
    
    return planes