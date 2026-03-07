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
        loc = (0, 25)
        
        if fid == "Forklift_1":
            loc = (37, 25)
            # Forklift_1故障不可用，跳过添加
            continue
            
        forklifts.append({
            "id": fid,
            "location": loc,
        })
    return forklifts