"""
生成突发事件数据集
JSON 格式：
{
  "emergency_situation": "事件1;事件2;事件3",
  "functions": ["func1", "func2", "func3"]
}
"""

import json
import random


def generate_emergency_candidates():
    """生成与当前原子函数库一一对应的突发事件候选池。"""

    plane_id = random.randint(3, 7)
    resource_id = random.randint(1, 5)
    task_id = random.randint(1, 6)

    x = random.randint(3, 8)
    y = random.randint(3, 8)
    end_x = random.randint(7, 12)
    end_y = random.randint(7, 12)

    candidates = [
        (
            f"从第{plane_id}架舰载机开始到达间隔改为{random.choice([5, 6, 8])}分钟",
            "init_planes",
        ),
        (
            f"第{resource_id}个固定保障资源初始位置调整为({random.randint(0, 3)},{random.randint(0, 10)})",
            "init_fixed_resources",
        ),
        (
            f"第{resource_id}个通用移动资源发生故障不可用",
            "init_mobile_resources",
        ),
        (
            f"第{resource_id}辆牵引车初始位置调整为({random.randint(0, 3)},{random.randint(0, 10)})",
            "init_tractor_resources",
        ),
        (
            f"第{resource_id}辆加油车发生故障不可用",
            "init_fuel_truck_resources",
        ),
        (
            f"第{resource_id}辆加氮车初始位置调整为({random.randint(0, 3)},{random.randint(0, 10)})",
            "init_nitrogen_truck_resources",
        ),
        (
            f"第{resource_id}辆充氧车发生故障不可用",
            "init_oxygen_truck_resources",
        ),
        (
            f"第{resource_id}辆供电车初始位置调整为({random.randint(0, 3)},{random.randint(0, 10)})",
            "init_power_cart_resources",
        ),
        (
            f"第{resource_id}辆气源车发生故障不可用",
            "init_air_source_car_resources",
        ),
        (
            f"第{resource_id}辆液压车初始位置调整为({random.randint(0, 3)},{random.randint(0, 10)})",
            "init_hydraulic_cart_resources",
        ),
        (
            f"第{resource_id}辆维修车发生故障不可用",
            "init_maintenance_vehicle_resources",
        ),
        (
            f"第{resource_id}辆消防车初始位置调整为({random.randint(0, 3)},{random.randint(0, 10)})",
            "init_fire_vehicle_resources",
        ),
        (
            f"第{task_id}个牵引任务目标站位调整为({random.randint(0, 3)},{random.randint(0, 10)})",
            "init_towing_tasks",
        ),
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
        k = random.randint(5, 8)
        selected = random.sample(pool, k)
        dataset.append({
            "emergency_situation": ";".join(item[0] for item in selected),
            "functions": [item[1] for item in selected],
        })

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"已生成 {num_samples} 条数据，保存至 {save_path}")


if __name__ == "__main__":
    generate_dataset()
