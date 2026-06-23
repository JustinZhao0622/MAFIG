import heapq
import time
def init_forklifts(nums=3):
    """
    初始化叉车队。
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        current_id = f"Forklift_{i+1}"
        if current_id == "Forklift_1":
            continue
        current_location = (0, 25)
        if current_id == "Forklift_3":
            current_location = (34, 49)
        forklifts.append({
            "id": current_id,
            "location": current_location,
        })
    return forklifts