import heapq
import time
def init_forklifts(nums=3):
    """
    初始化叉车队。
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        loc = (0, 25)
        fork_id = f"Forklift_{i+1}"
        if fork_id == "Forklift_3":
            loc = (39, 26)
        forklifts.append({
            "id": fork_id,
            "location": loc,
        })
    return forklifts