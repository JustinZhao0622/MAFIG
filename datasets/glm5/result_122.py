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
        if fid == "Forklift_1":
            continue
        loc = (0, 25)
        if fid == "Forklift_3":
            loc = (45, 27)
        forklifts.append({
            "id": fid,
            "location": loc,
        })
    return forklifts