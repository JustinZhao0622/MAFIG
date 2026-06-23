"""
生成 50 组突发事件
JSON 格式：
{
  "emergency_situation": "事件1;事件2;事件3",
  "functions": ["func1", "func2", "func3"]
}
"""

import random
import json


def generate_emergency_candidates():
    """根据 functions.py 中的函数生成突发事件候选池，每个候选为 (事件描述, 关联函数名)"""

    x = random.randint(3, 6)
    y = random.randint(3, 6)
    end_x = random.randint(7, 9)
    end_y = random.randint(7, 9)

    candidates = [
        # init_truck_arrival_time 相关
        (
            f"从第{random.randint(3,7)}辆货车开始间隔改为{random.choice([5,6,8])}分钟",
            "init_truck_arrival_time",
        ),
        # init_stacking_zones 相关
        (
            f"Zone_{random.randint(1,4)}堆积区当前库存增加{random.randint(20,80)}",
            "init_stacking_zones",
        ),
        (
            f"Zone_{random.randint(1,4)}堆积区最大容量缩减至{random.randint(50,150)}",
            "init_stacking_zones",
        ),
        (
            f"Zone_{random.randint(1,4)}堆积区发生故障不可用",
            "init_stacking_zones",
        ),

        # init_forklifts 相关
        (
            f"Forklift_{random.randint(1,3)}叉车发生故障不可用",
            "init_forklifts",
        ),
        (
            f"Forklift_{random.randint(1,3)}叉车初始位置调整为({random.randint(10,50)},{random.randint(10,50)})",
            "init_forklifts",
        ),
        # route_planning 相关
        (
            f"站位({x},{y})({x+1},{y})({x},{y+1})({x+1},{y+1})四个点发生故障",
            "route_planning",
        ),
        (
            f"站位({end_x},{end_y})发生故障,以该点为终点的调整为({end_x+1},{end_y})",
            "route_planning",
        ),
    ]

    return candidates


def generate_dataset(num_samples=100, save_path="datasets/test.json"):
    dataset = []

    for _ in range(num_samples):
        pool = generate_emergency_candidates()
        k = random.randint(3, 5)
        selected = random.sample(pool, min(k, len(pool)))

        dataset.append({
            "emergency_situation": ";".join(item[0] for item in selected),
            "functions": [item[1] for item in selected],
        })

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"已生成 {num_samples} 条数据，保存至 {save_path}")


if __name__ == "__main__":
    generate_dataset()
