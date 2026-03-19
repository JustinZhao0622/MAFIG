import heapq
import time
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    for i in range(nums):
        if i < 4:
            offset = 3 * 60 * i
        else:
            offset = 9 * 60 + (i - 3) * 5 * 60
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + offset))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks