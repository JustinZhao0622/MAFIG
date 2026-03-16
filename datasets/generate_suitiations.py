"""
生成 50 组突发事件
JSON 格式：
{
  "emergency_situation": "事件1,事件2,事件3",
  "functions": ["func1", "func2", "func3"]
}
"""

import random
import json


def generate_emergency_candidates():
    "生成突发事件"
    x = random.randint(3, 6)
    y = random.randint(3, 6)

    end_point_x = random.randint(7, 9)
    end_point_y = random.randint(7, 9)

    return [
        (
            f"id为{random.randint(0,9)}的资源不可用",
            "init_resources"
        ),
        (
            f"第{random.randint(0,4)}艘到达的船舶延迟10分钟到达",
            "init_cranes"
        ),
        (
            f"站位({x},{y})({x+1},{y})({x},{y+1})({x+1},{y+1})四个点发生故障",
            "route_planning"
        ),
        (
            f"站位({end_point_x},{end_point_y})发生故障,以该点为终点的调整为({end_point_x+1},{end_point_y})",
            "route_planning"
        ),
        (
            f"id为{random.randint(0,4)}的船舶任务时长延长至20分钟",
            "init_cranes"
        )
    ]


def generate_dataset(num_samples=50, save_path="emergency_events.json"):
    "生成50个突发事件并保存"
    dataset = []

    for _ in range(num_samples):
        pool = generate_emergency_candidates()
        k = random.randint(3, 5)
        selected = random.sample(pool, k)

        emergency_texts = [item[0] for item in selected]
        functions = [item[1] for item in selected]

        dataset.append({
            "emergency_situation": ";".join(emergency_texts),
            "functions": functions
        })

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"✅ 已生成 {num_samples} 条数据，保存至 {save_path}")


if __name__ == "__main__":
    generate_dataset()
    