import heapq
import time
def init_forklifts(nums=3):
    """
    初始化叉车队。
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        fid = f"Forklift_{i+1}"
        location = (0, 25)
        
        forklift_info = {
            "id": fid,
            "location": location
        }
        
        if fid == "Forklift_3":
            forklift_info["location"] = (29, 14)
            forklift_info["status"] = "unavailable"
            
        forklifts.append(forklift_info)
        
    return forklifts