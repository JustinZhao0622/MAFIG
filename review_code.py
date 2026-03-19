"""
验证代码是否真正解决相应突发事件
"""

import importlib.util
import json
import multiprocessing
import os
import re
import time

try:
    from tqdm import tqdm
except Exception:
    def tqdm(iterable):
        return iterable

TIMEOUT = 5


class DynamicVerifier:
    """按事件类型对生成代码做动态行为验证。"""

    def __init__(self, module):
        self.module = module

    def _call(self, func_name, *args, **kwargs):
        func = getattr(self.module, func_name, None)
        if not callable(func):
            raise AttributeError(f"missing function: {func_name}")
        return func(*args, **kwargs)

    def _find_by_index(self, items, target_idx):
        if not isinstance(items, list):
            return None
        if 0 <= target_idx < len(items):
            return items[target_idx]
        return None

    def _is_unavailable(self, item):
        if item is None:
            return True
        status = str(item.get("status", "")).lower()
        available = item.get("available")
        if available is False:
            return True
        return status in {"unavailable", "disabled", "offline", "closed", "blocked", "fault", "broken"}

    def _tuple_path(self, path):
        normalized = []
        for point in path or []:
            if isinstance(point, (list, tuple)) and len(point) == 2:
                normalized.append((int(point[0]), int(point[1])))
        return normalized

    def _parse_location(self, text):
        match = re.search(r"\((\d+),(\d+)\)", text)
        if not match:
            return None
        return (int(match.group(1)), int(match.group(2)))

    def _check_resource_location(self, text, pattern, func_name):
        match = re.search(pattern, text)
        if not match:
            return False
        target_idx = int(match.group(1)) - 1
        new_loc = (int(match.group(2)), int(match.group(3)))
        try:
            items = self._call(func_name)
            target = self._find_by_index(items, target_idx)
            return target is not None and tuple(target.get("location", ())) == new_loc
        except Exception:
            return False

    def _check_resource_unavailable(self, text, pattern, func_name):
        match = re.search(pattern, text)
        if not match:
            return False
        target_idx = int(match.group(1)) - 1
        try:
            items = self._call(func_name)
            target = self._find_by_index(items, target_idx)
            return self._is_unavailable(target)
        except Exception:
            return False

    def _check_task_location(self, text, pattern, func_name):
        match = re.search(pattern, text)
        if not match:
            return False
        target_idx = int(match.group(1)) - 1
        new_loc = (int(match.group(2)), int(match.group(3)))
        try:
            items = self._call(func_name)
            target = self._find_by_index(items, target_idx)
            return target is not None and tuple(target.get("location", ())) == new_loc
        except Exception:
            return False

    def _check_task_priority(self, text, pattern, func_name):
        match = re.search(pattern, text)
        if not match:
            return False
        target_idx = int(match.group(1)) - 1
        try:
            items = self._call(func_name)
            target = self._find_by_index(items, target_idx)
            if target is None:
                return False
            if int(target.get("priority", -1)) == 1:
                return True
            return str(target.get("status", "")).lower() in {"priority", "urgent", "high", "high_priority"}
        except Exception:
            return False

    def check_planes_interval(self, text):
        match = re.search(r"从第(\d+)架舰载机开始到达间隔改为(\d+)分钟", text)
        if not match:
            return False
        start_idx = int(match.group(1)) - 1
        interval = int(match.group(2))
        try:
            planes = self._call("init_planes", 10)
            if start_idx <= 0 or start_idx >= len(planes):
                return False
            prev_time = time.strptime(planes[start_idx - 1]["time"], "%H:%M:%S")
            curr_time = time.strptime(planes[start_idx]["time"], "%H:%M:%S")
            prev_ts = time.mktime(prev_time)
            curr_ts = time.mktime(curr_time)
            return int((curr_ts - prev_ts) / 60) == interval
        except Exception:
            return False

    def check_fixed_resource_location(self, text):
        return self._check_resource_location(
            text,
            r"第(\d+)个固定保障资源初始位置调整为\((\d+),(\d+)\)",
            "init_fixed_resources",
        )

    def check_mobile_resource_unavailable(self, text):
        return self._check_resource_unavailable(
            text,
            r"第(\d+)个通用移动资源发生故障不可用",
            "init_mobile_resources",
        )

    def check_tractor_location(self, text):
        return self._check_resource_location(
            text,
            r"第(\d+)辆牵引车初始位置调整为\((\d+),(\d+)\)",
            "init_tractor_resources",
        )

    def check_fuel_truck_unavailable(self, text):
        return self._check_resource_unavailable(
            text,
            r"第(\d+)辆加油车发生故障不可用",
            "init_fuel_truck_resources",
        )

    def check_nitrogen_truck_location(self, text):
        return self._check_resource_location(
            text,
            r"第(\d+)辆加氮车初始位置调整为\((\d+),(\d+)\)",
            "init_nitrogen_truck_resources",
        )

    def check_oxygen_truck_unavailable(self, text):
        return self._check_resource_unavailable(
            text,
            r"第(\d+)辆充氧车发生故障不可用",
            "init_oxygen_truck_resources",
        )

    def check_power_cart_location(self, text):
        return self._check_resource_location(
            text,
            r"第(\d+)辆供电车初始位置调整为\((\d+),(\d+)\)",
            "init_power_cart_resources",
        )

    def check_air_source_car_unavailable(self, text):
        return self._check_resource_unavailable(
            text,
            r"第(\d+)辆气源车发生故障不可用",
            "init_air_source_car_resources",
        )

    def check_hydraulic_cart_location(self, text):
        return self._check_resource_location(
            text,
            r"第(\d+)辆液压车初始位置调整为\((\d+),(\d+)\)",
            "init_hydraulic_cart_resources",
        )

    def check_maintenance_vehicle_unavailable(self, text):
        return self._check_resource_unavailable(
            text,
            r"第(\d+)辆维修车发生故障不可用",
            "init_maintenance_vehicle_resources",
        )

    def check_fire_vehicle_location(self, text):
        return self._check_resource_location(
            text,
            r"第(\d+)辆消防车初始位置调整为\((\d+),(\d+)\)",
            "init_fire_vehicle_resources",
        )

    def check_towing_task_location(self, text):
        return self._check_task_location(
            text,
            r"第(\d+)个牵引任务目标站位调整为\((\d+),(\d+)\)",
            "init_towing_tasks",
        )

    def check_refueling_task_priority(self, text):
        return self._check_task_priority(
            text,
            r"第(\d+)个加油任务改为优先执行",
            "init_refueling_tasks",
        )

    def check_nitrogen_task_location(self, text):
        return self._check_task_location(
            text,
            r"第(\d+)个加氮任务目标站位调整为\((\d+),(\d+)\)",
            "init_nitrogen_filling_tasks",
        )

    def check_oxygen_task_location(self, text):
        return self._check_task_location(
            text,
            r"第(\d+)个充氧任务改派至站位\((\d+),(\d+)\)",
            "init_oxygen_filling_tasks",
        )

    def check_power_task_location(self, text):
        return self._check_task_location(
            text,
            r"第(\d+)个供电任务目标站位调整为\((\d+),(\d+)\)",
            "init_power_supply_tasks",
        )

    def check_air_task_location(self, text):
        return self._check_task_location(
            text,
            r"第(\d+)个供气任务改派至站位\((\d+),(\d+)\)",
            "init_air_supply_tasks",
        )

    def check_hydraulic_task_location(self, text):
        return self._check_task_location(
            text,
            r"第(\d+)个液压保障任务目标站位调整为\((\d+),(\d+)\)",
            "init_hydraulic_support_tasks",
        )

    def check_maintenance_task_priority(self, text):
        return self._check_task_priority(
            text,
            r"第(\d+)个维修保障任务改为优先执行",
            "init_maintenance_tasks",
        )

    def check_inspection_task_location(self, text):
        return self._check_task_location(
            text,
            r"第(\d+)个检查任务目标站位调整为\((\d+),(\d+)\)",
            "init_inspection_tasks",
        )

    def check_fire_watch_task_location(self, text):
        return self._check_task_location(
            text,
            r"第(\d+)个消防监护任务改派至站位\((\d+),(\d+)\)",
            "init_fire_watch_tasks",
        )

    def check_ammo_task_location(self, text):
        return self._check_task_location(
            text,
            r"第(\d+)个挂载弹药任务目标站位调整为\((\d+),(\d+)\)",
            "init_tasks",
        )

    def check_route_reroute(self, text):
        matches = re.findall(r"\((\d+),(\d+)\)", text)
        if len(matches) < 4:
            return False
        blocked = {tuple(map(int, item)) for item in matches[:4]}
        try:
            path = self._tuple_path(self._call("route_planning", (0, 0), (10, 10)))
            if not path:
                return False
            return blocked.isdisjoint(set(path))
        except Exception:
            return False

    def check_route_endpoint_change(self, text):
        match = re.search(r"站位\((\d+),(\d+)\)发生故障,以该点为终点的调整为\((\d+),(\d+)\)", text)
        if not match:
            return False
        old_end = (int(match.group(1)), int(match.group(2)))
        new_end = (int(match.group(3)), int(match.group(4)))
        try:
            path = self._tuple_path(self._call("route_planning", (0, 0), old_end))
            return bool(path) and path[-1] == new_end
        except Exception:
            return False


def verify_single_event(verifier, event):
    """返回 (是否解决, 事件类型名)。"""
    if "架舰载机开始到达间隔改为" in event:
        return verifier.check_planes_interval(event), "init_planes"
    if "固定保障资源初始位置调整为" in event:
        return verifier.check_fixed_resource_location(event), "init_fixed_resources"
    if "通用移动资源发生故障不可用" in event:
        return verifier.check_mobile_resource_unavailable(event), "init_mobile_resources"
    if "牵引车初始位置调整为" in event:
        return verifier.check_tractor_location(event), "init_tractor_resources"
    if "加油车发生故障不可用" in event:
        return verifier.check_fuel_truck_unavailable(event), "init_fuel_truck_resources"
    if "加氮车初始位置调整为" in event:
        return verifier.check_nitrogen_truck_location(event), "init_nitrogen_truck_resources"
    if "充氧车发生故障不可用" in event:
        return verifier.check_oxygen_truck_unavailable(event), "init_oxygen_truck_resources"
    if "供电车初始位置调整为" in event:
        return verifier.check_power_cart_location(event), "init_power_cart_resources"
    if "气源车发生故障不可用" in event:
        return verifier.check_air_source_car_unavailable(event), "init_air_source_car_resources"
    if "液压车初始位置调整为" in event:
        return verifier.check_hydraulic_cart_location(event), "init_hydraulic_cart_resources"
    if "维修车发生故障不可用" in event:
        return verifier.check_maintenance_vehicle_unavailable(event), "init_maintenance_vehicle_resources"
    if "消防车初始位置调整为" in event:
        return verifier.check_fire_vehicle_location(event), "init_fire_vehicle_resources"
    if "牵引任务目标站位调整为" in event:
        return verifier.check_towing_task_location(event), "init_towing_tasks"
    if "加油任务改为优先执行" in event:
        return verifier.check_refueling_task_priority(event), "init_refueling_tasks"
    if "加氮任务目标站位调整为" in event:
        return verifier.check_nitrogen_task_location(event), "init_nitrogen_filling_tasks"
    if "充氧任务改派至站位" in event:
        return verifier.check_oxygen_task_location(event), "init_oxygen_filling_tasks"
    if "供电任务目标站位调整为" in event:
        return verifier.check_power_task_location(event), "init_power_supply_tasks"
    if "供气任务改派至站位" in event:
        return verifier.check_air_task_location(event), "init_air_supply_tasks"
    if "液压保障任务目标站位调整为" in event:
        return verifier.check_hydraulic_task_location(event), "init_hydraulic_support_tasks"
    if "维修保障任务改为优先执行" in event:
        return verifier.check_maintenance_task_priority(event), "init_maintenance_tasks"
    if "检查任务目标站位调整为" in event:
        return verifier.check_inspection_task_location(event), "init_inspection_tasks"
    if "消防监护任务改派至站位" in event:
        return verifier.check_fire_watch_task_location(event), "init_fire_watch_tasks"
    if "挂载弹药任务目标站位调整为" in event:
        return verifier.check_ammo_task_location(event), "init_tasks"
    if "四个点发生故障" in event:
        return verifier.check_route_reroute(event), "route_planning"
    if "以该点为终点的调整为" in event:
        return verifier.check_route_endpoint_change(event), "route_planning"
    return False, "unknown"


def run_verify_case(file_path, emergency_list, return_dict):
    """单个进程运行：加载模块并验证该文件对应的特情列表"""
    try:
        spec = importlib.util.spec_from_file_location("test_module", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        verifier = DynamicVerifier(module)
        solved_count = 0
        unsolved = []

        for event in emergency_list:
            is_solved, function_name = verify_single_event(verifier, event)
            if is_solved:
                solved_count += 1
            else:
                unsolved.append({
                    "event": event,
                    "function": function_name,
                })

        return_dict["result"] = {
            "total": len(emergency_list),
            "solved": solved_count,
            "unsolved": unsolved,
        }
    except Exception as exc:
        return_dict["error"] = str(exc)


def _verify_worker(file_path, events, queue):
    result = {}
    run_verify_case(file_path, events, result)
    queue.put(result)


def verify_file_with_timeout(file_path, events, timeout=TIMEOUT):
    """带超时的文件验证，返回与 run_verify_case 相同结构。"""
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=_verify_worker, args=(file_path, events, queue))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        return {"timeout": True, "result": {"total": len(events), "solved": 0, "unsolved": []}}

    if queue.empty():
        return {"error": "子进程未返回结果"}

    return queue.get()


def main(DATASET_FILE, RESULT_DIR):
    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    files = sorted(
        [name for name in os.listdir(RESULT_DIR) if name.startswith("result_") and name.endswith(".py")],
        key=lambda x: int(x.split("_")[1].split(".")[0]),
    )

    total_emergencies_all = 0
    total_solved_all = 0
    file_stats = []

    print(f"开始测试 {len(files)} 个文件，对照 {len(dataset)} 条生成的特情数据...")
    print("-" * 60)

    for filename in tqdm(files):
        dataset_idx = int(filename.split("_")[1].split(".")[0]) - 1
        if dataset_idx < 0 or dataset_idx >= len(dataset):
            continue

        situation_str = dataset[dataset_idx].get("emergency_situation", "")
        events = [event.strip() for event in situation_str.split(";") if event.strip()]
        file_path = os.path.join(RESULT_DIR, filename)

        return_dict = verify_file_with_timeout(file_path, events, TIMEOUT)

        if return_dict.get("timeout"):
            res = {"total": len(events), "solved": 0, "status": "超时"}
            print(f"[超时] {filename}")
        elif "error" in return_dict:
            res = {"total": len(events), "solved": 0, "status": "报错"}
            print(f"[报错] {filename}: {return_dict['error']}")
        else:
            data = return_dict.get("result", {"total": 0, "solved": 0, "unsolved": []})
            res = {"total": data["total"], "solved": data["solved"], "status": "正常"}
            if data["unsolved"]:
                print(f"[未完全解决] {filename}: {data['solved']}/{data['total']}")
                for item in data["unsolved"]:
                    print(f"  未解决({item['function']}): {item['event']}")

        total_emergencies_all += res["total"]
        total_solved_all += res["solved"]
        file_stats.append({
            "文件名": filename,
            "特情总数": res["total"],
            "解决数量": res["solved"],
            "状态": res["status"],
        })

    print("\n" + "=" * 30 + " 最终统计结果 " + "=" * 30)
    print(f"测试文件数量: {len(file_stats)}")
    print(f"一共生成的特情总数: {total_emergencies_all}")
    print(f"一共解决的特情总数: {total_solved_all}")
    if total_emergencies_all > 0:
        print(f"整体解决率: {total_solved_all / total_emergencies_all:.2%}")
        print("=" * 76)
        return total_solved_all / total_emergencies_all

    print("整体解决率: 0%")
    print("=" * 76)
    return 0
