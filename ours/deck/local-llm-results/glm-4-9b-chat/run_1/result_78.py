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
    # 修改第4架舰载机的初始位置为(0,7)
    planes[3]["location"] = (0, 7)
    # 从第5架舰载机开始到达间隔改为6分钟
    for i in range(4, nums):
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 6 * 60 * (i - 4)))
        planes[i]["time"] = plane_time
    return planes

# 其他函数保持不变
# ... (省略其他函数的代码，因为它们没有需要修改的逻辑)
