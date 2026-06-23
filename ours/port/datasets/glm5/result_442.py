import heapq
import time
import random 
def init_cranes(nums=5,start_time="8:00:00"):
    """每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    base_time = time.mktime(start_time)
    for i in range(nums):
        if i == 0:
            vessel_time_stamp = base_time + 10 * 60
        else:
            vessel_time_stamp = base_time + 3 * 60 * i
        vessel_time = time.strftime("%H:%M:%S", time.localtime(vessel_time_stamp))
        vessels.append({"time": vessel_time, "id": i, "duration": 10, "location": (i,10)})
    return vessels