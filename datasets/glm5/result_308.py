import heapq
import time
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    current_ts = time.mktime(start_time)
    for i in range(nums):
        arrival_time = time.strftime("%H:%M:%S", time.localtime(current_ts))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
        if i >= 1:
            current_ts += 6 * 60
        else:
            current_ts += 3 * 60
    return trucks