import heapq
import time
import random 
def init_cranes(nums=5,start_time="8:00:00"):
    """每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        # 计算基础到达时间偏移量
        time_offset = 3 * 60 * i
        
        # 突发事件处理：第4艘到达的船舶（ID=3）延迟10分钟
        if i == 3:
            time_offset += 10 * 60
            
        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + time_offset))
        
        # 基础任务时长
        duration = 10
        
        # 突发事件处理：id为4的船舶任务时长延长至20分钟
        if i == 4:
            duration = 20
            
        vessels.append({"time": vessel_time, "id": i, "duration": duration, "location": (i,10)})
    return vessels