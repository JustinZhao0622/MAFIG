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
        if i < 3:
            # 前3辆货车（Truck_0, Truck_1, Truck_2）保持3分钟间隔
            arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        else:
            # 从第4辆货车（Truck_3）开始，间隔改为8分钟
            # Truck_2 (i=2) 的到达时间是 start + 3*2 = start + 6min
            # Truck_3 (i=3) 的到达时间是 Truck_2 + 8min = start + 6 + 8*(3-2)
            # Truck_i 的到达时间是 start + 6 + 8*(i-2)
            arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * 2 + 8 * 60 * (i - 2)))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks