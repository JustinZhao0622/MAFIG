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
        # 突发事件处理: Forklift_3故障不可用，跳过创建
        if fid == "Forklift_3":
            continue
        
        # 突发事件处理: Forklift_1初始位置调整为(21,16)
        if fid == "Forklift_1":
            location = (21, 16)
        else:
            location = (0, 25)
            
        forklifts.append({
            "id": fid,
            "location": location,
        })
    return forklifts