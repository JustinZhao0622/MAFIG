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
        
        # 突发事件处理：Forklift_2故障不可用，跳过添加
        if fid == "Forklift_2":
            continue
            
        # 突发事件处理：Forklift_1初始位置调整为(22,46)
        if fid == "Forklift_1":
            forklifts.append({
                "id": fid,
                "location": (22, 46),
            })
        else:
            forklifts.append({
                "id": fid,
                "location": (0, 25),
            })
    return forklifts