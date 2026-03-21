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
        # 突发事件处理：Forklift_1发生故障不可用，不加入可用列表
        if fid == "Forklift_1":
            continue
        
        forklifts.append({
            "id": fid,
            "location": (0, 25),
        })
    return forklifts