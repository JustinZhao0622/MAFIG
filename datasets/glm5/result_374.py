import heapq
import time
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    for i in range(nums):
        if i < 5:
            interval_seconds = 3 * 60 * i
        else:
            interval_seconds = 3 * 60 * 4 + 8 * 60 * (i - 4)
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + interval_seconds))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks