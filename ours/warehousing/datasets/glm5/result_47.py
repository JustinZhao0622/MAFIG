import heapq
import time
def init_forklifts(nums=3):
    """
    初始化叉车队。
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        forklift_id = f"Forklift_{i+1}"
        location = (0, 25)
        
        if forklift_id == "Forklift_1":
            location = (18, 25)
            continue
            
        forklifts.append({
            "id": forklift_id,
            "location": location,
        })
    return forklifts