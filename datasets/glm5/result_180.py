import heapq
import time
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    start_timestamp = time.mktime(start_time)
    trucks = []
    current_timestamp = start_timestamp
    for i in range(nums):
        arrival_time = time.strftime("%H:%M:%S", time.localtime(current_timestamp))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
        if i == 0:
            current_timestamp += 3 * 60
        else:
            current_timestamp += 6 * 60
    return trucks