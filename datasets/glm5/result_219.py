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
        
        # 突发事件：Forklift_1故障不可用，跳过初始化
        if forklift_id == "Forklift_1":
            continue
            
        location = (0, 25)
        
        # 突发事件：Forklift_3初始位置调整为(44,36)
        if forklift_id == "Forklift_3":
            location = (44, 36)
            
        forklifts.append({
            "id": forklift_id,
            "location": location,
        })
    return forklifts