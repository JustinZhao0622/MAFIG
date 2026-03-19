import heapq
import time
import random

def init_planes(nums=5, start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i, 10)})
    # 修改第5辆液压车初始位置
    planes[4]["location"] = (2, 3)
    # 修改第2个牵引任务目标站位
    planes[1]["location"] = (1, 2)
    # 修改第5辆供电车初始位置
    planes[4]["location"] = (0, 6)
    # 修改站位(8,12)发生故障，以该点为终点的调整为(9,12)
    for plane in planes:
        if plane["location"] == (8, 12):
            plane["location"] = (9, 12)
    # 修改站位(7,5)(8,5)(7,6)(8,6)四个点发生故障
    for plane in planes:
        if plane["location"] in [(7, 5), (8, 5), (7, 6), (8, 6)]:
            plane["location"] = (plane["location"][0], plane["location"][1] + 1)
    return planes

# 其他函数保持不变
