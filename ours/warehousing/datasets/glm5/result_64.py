import heapq
import time
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    base_timestamp = time.mktime(start_time)
    current_timestamp = base_timestamp
    
    for i in range(nums):
        if i == 0:
            interval_minutes = 0
        elif i < 6:
            interval_minutes = 3
        else:
            interval_minutes = 5
            
        current_timestamp += interval_minutes * 60
        arrival_time = time.strftime("%H:%M:%S", time.localtime(current_timestamp))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks