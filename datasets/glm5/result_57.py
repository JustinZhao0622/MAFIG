import heapq
import time
def init_forklifts(nums=3):
    """
    初始化叉车队。
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        if i == 0:
            location = (31, 36)
        else:
            location = (0, 25)
        forklifts.append({
            "id": f"Forklift_{i+1}",
            "location": location,
        })
    return forklifts