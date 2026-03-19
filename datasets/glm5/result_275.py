import heapq
import time
import random 
def init_cranes(nums=5,start_time="8:00:00"):
    """每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        current_duration = 10
        if i == 1:
            current_duration = 20
        
        arrival_delay = 3 * 60 * i
        if i == 2:
            arrival_delay += 10 * 60

        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + arrival_delay))
        vessels.append({"time": vessel_time, "id": i, "duration": current_duration, "location": (i,10)})
    return vessels