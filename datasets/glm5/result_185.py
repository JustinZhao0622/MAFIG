import heapq
import time
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    start_ts = time.mktime(start_time)
    for i in range(nums):
        if i < 5:
            offset = 3 * i
        else:
            offset = 12 + 5 * (i - 4)
        arrival_time = time.strftime("%H:%M:%S", time.localtime(start_ts + offset * 60))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks