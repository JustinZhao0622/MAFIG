import heapq
import time
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    for i in range(nums):
        if i < 4:
            offset_seconds = i * 3 * 60
        else:
            offset_seconds = (3 * 3 + (i - 3) * 8) * 60
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + offset_seconds))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks