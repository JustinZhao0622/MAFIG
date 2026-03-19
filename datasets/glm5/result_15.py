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
        if i == 2:
            loc = (21, 19)
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": loc,
        })
    return forklifts