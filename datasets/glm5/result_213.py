import heapq
import time
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。前5辆车间隔3分钟，从第6辆开始间隔8分钟。
    返回货车列表，每个货车包含id和到达时间
    """
    parsed_start_time = time.strptime(start_time, "%H:%M:%S")
    current_timestamp = time.mktime(parsed_start_time)
    trucks = []
    for i in range(nums):
        if i > 0:
            if i >= 5:
                current_timestamp += 8 * 60
            else:
                current_timestamp += 3 * 60
        arrival_time = time.strftime("%H:%M:%S", time.localtime(current_timestamp))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks