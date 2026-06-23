"""验证代码是否解决相应突发事件 (deck)"""

import re
import time
import importlib.util


class DynamicVerifier:
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
        return items[target_idx] if 0 <= target_idx < len(items) else None

    def _is_unavailable(self, item):
        if item is None:
            return True
        status = str(item.get("status", "")).lower()
        if item.get("available") is False:
            return True
        return status in {"unavailable", "disabled", "offline", "closed", "blocked", "fault", "broken"}

    def _tuple_path(self, path):
        return [
            (int(p[0]), int(p[1]))
            for p in (path or [])
            if isinstance(p, (list, tuple)) and len(p) == 2
        ]

    def _check_resource_location(self, text, pattern, func_name):
        match = re.search(pattern, text)
        if not match:
            return False
        target_idx = int(match.group(1)) - 1
        new_loc = (int(match.group(2)), int(match.group(3)))
        items = self._call(func_name)
        target = self._find_by_index(items, target_idx)
        return target is not None and tuple(target.get("location", ())) == new_loc

    def _check_resource_unavailable(self, text, pattern, func_name):
        match = re.search(pattern, text)
        if not match:
            return False
        target_idx = int(match.group(1)) - 1
        items = self._call(func_name)
        target = self._find_by_index(items, target_idx)
        return self._is_unavailable(target)

    def _check_task_location(self, text, pattern, func_name):
        match = re.search(pattern, text)
        if not match:
            return False
        target_idx = int(match.group(1)) - 1
        new_loc = (int(match.group(2)), int(match.group(3)))
        items = self._call(func_name)
        target = self._find_by_index(items, target_idx)
        return target is not None and tuple(target.get("location", ())) == new_loc

    def _check_task_priority(self, text, pattern, func_name):
        match = re.search(pattern, text)
        if not match:
            return False
        target_idx = int(match.group(1)) - 1
        items = self._call(func_name)
        target = self._find_by_index(items, target_idx)
        if target is None:
            return False
        if int(target.get("priority", -1)) == 1:
            return True
        return str(target.get("status", "")).lower() in {"priority", "urgent", "high", "high_priority"}

    def check_planes_interval(self, text):
        match = re.search(r"从第(\d+)架舰载机开始到达间隔改为(\d+)分钟", text)
        if not match:
            return False
        start_idx = int(match.group(1)) - 1
        interval = int(match.group(2))
        planes = self._call("init_planes", 10)
        if start_idx <= 0 or start_idx >= len(planes):
            return False
        prev_ts = time.mktime(time.strptime(planes[start_idx - 1]["time"], "%H:%M:%S"))
        curr_ts = time.mktime(time.strptime(planes[start_idx]["time"], "%H:%M:%S"))
        return int((curr_ts - prev_ts) / 60) == interval

    def check_fixed_resource_location(self, text):
        return self._check_resource_location(text, r"第(\d+)个固定保障资源初始位置调整为\((\d+),(\d+)\)", "init_fixed_resources")

    def check_mobile_resource_unavailable(self, text):
        return self._check_resource_unavailable(text, r"第(\d+)个通用移动资源发生故障不可用", "init_mobile_resources")

    def check_tractor_location(self, text):
        return self._check_resource_location(text, r"第(\d+)辆牵引车初始位置调整为\((\d+),(\d+)\)", "init_tractor_resources")

    def check_fuel_truck_unavailable(self, text):
        return self._check_resource_unavailable(text, r"第(\d+)辆加油车发生故障不可用", "init_fuel_truck_resources")

    def check_nitrogen_truck_location(self, text):
        return self._check_resource_location(text, r"第(\d+)辆加氮车初始位置调整为\((\d+),(\d+)\)", "init_nitrogen_truck_resources")

    def check_oxygen_truck_unavailable(self, text):
        return self._check_resource_unavailable(text, r"第(\d+)辆充氧车发生故障不可用", "init_oxygen_truck_resources")

    def check_power_cart_location(self, text):
        return self._check_resource_location(text, r"第(\d+)辆供电车初始位置调整为\((\d+),(\d+)\)", "init_power_cart_resources")

    def check_air_source_car_unavailable(self, text):
        return self._check_resource_unavailable(text, r"第(\d+)辆气源车发生故障不可用", "init_air_source_car_resources")

    def check_hydraulic_cart_location(self, text):
        return self._check_resource_location(text, r"第(\d+)辆液压车初始位置调整为\((\d+),(\d+)\)", "init_hydraulic_cart_resources")

    def check_maintenance_vehicle_unavailable(self, text):
        return self._check_resource_unavailable(text, r"第(\d+)辆维修车发生故障不可用", "init_maintenance_vehicle_resources")

    def check_fire_vehicle_location(self, text):
        return self._check_resource_location(text, r"第(\d+)辆消防车初始位置调整为\((\d+),(\d+)\)", "init_fire_vehicle_resources")

    def check_towing_task_location(self, text):
        return self._check_task_location(text, r"第(\d+)个牵引任务目标站位调整为\((\d+),(\d+)\)", "init_towing_tasks")

    def check_refueling_task_priority(self, text):
        return self._check_task_priority(text, r"第(\d+)个加油任务改为优先执行", "init_refueling_tasks")

    def check_nitrogen_task_location(self, text):
        return self._check_task_location(text, r"第(\d+)个加氮任务目标站位调整为\((\d+),(\d+)\)", "init_nitrogen_filling_tasks")

    def check_oxygen_task_location(self, text):
        return self._check_task_location(text, r"第(\d+)个充氧任务改派至站位\((\d+),(\d+)\)", "init_oxygen_filling_tasks")

    def check_power_task_location(self, text):
        return self._check_task_location(text, r"第(\d+)个供电任务目标站位调整为\((\d+),(\d+)\)", "init_power_supply_tasks")

    def check_air_task_location(self, text):
        return self._check_task_location(text, r"第(\d+)个供气任务改派至站位\((\d+),(\d+)\)", "init_air_supply_tasks")

    def check_hydraulic_task_location(self, text):
        return self._check_task_location(text, r"第(\d+)个液压保障任务目标站位调整为\((\d+),(\d+)\)", "init_hydraulic_support_tasks")

    def check_maintenance_task_priority(self, text):
        return self._check_task_priority(text, r"第(\d+)个维修保障任务改为优先执行", "init_maintenance_tasks")

    def check_inspection_task_location(self, text):
        return self._check_task_location(text, r"第(\d+)个检查任务目标站位调整为\((\d+),(\d+)\)", "init_inspection_tasks")

    def check_fire_watch_task_location(self, text):
        return self._check_task_location(text, r"第(\d+)个消防监护任务改派至站位\((\d+),(\d+)\)", "init_fire_watch_tasks")

    def check_ammo_task_location(self, text):
        return self._check_task_location(text, r"第(\d+)个挂载弹药任务目标站位调整为\((\d+),(\d+)\)", "init_tasks")

    def check_route_reroute(self, text):
        matches = re.findall(r"\((\d+),(\d+)\)", text)
        if len(matches) < 4:
            return False
        blocked = {tuple(map(int, item)) for item in matches[:4]}
        for point in blocked:
            if self._call("route_planning", (0, 0), point) is not None:
                return False
        path = self._tuple_path(self._call("route_planning", (0, 0), (10, 10)))
        return bool(path) and blocked.isdisjoint(set(path))

    def check_route_endpoint_change(self, text):
        match = re.search(r"站位\((\d+),(\d+)\)发生故障,以该点为终点的调整为\((\d+),(\d+)\)", text)
        if not match:
            return False
        old_end = (int(match.group(1)), int(match.group(2)))
        new_end = (int(match.group(3)), int(match.group(4)))
        path = self._tuple_path(self._call("route_planning", (0, 0), old_end))
        return bool(path) and path[-1] == new_end


def verify_single_event(verifier, event):
    checks = [
        (
            "架舰载机开始到达间隔改为",
            verifier.check_planes_interval,
            "init_planes",
            "init_planes 未把指定序号舰载机的到达间隔改成事件要求。",
        ),
        (
            "固定保障资源初始位置调整为",
            verifier.check_fixed_resource_location,
            "init_fixed_resources",
            "init_fixed_resources 中指定固定保障资源的位置未调整到事件给定坐标。",
        ),
        (
            "通用移动资源发生故障不可用",
            verifier.check_mobile_resource_unavailable,
            "init_mobile_resources",
            "init_mobile_resources 中指定通用移动资源仍可用或仍保留在可用资源列表中。",
        ),
        (
            "牵引车初始位置调整为",
            verifier.check_tractor_location,
            "init_tractor_resources",
            "init_tractor_resources 中指定牵引车的位置未调整到事件给定坐标。",
        ),
        (
            "加油车发生故障不可用",
            verifier.check_fuel_truck_unavailable,
            "init_fuel_truck_resources",
            "init_fuel_truck_resources 中指定加油车仍可用或仍保留在可用资源列表中。",
        ),
        (
            "加氮车初始位置调整为",
            verifier.check_nitrogen_truck_location,
            "init_nitrogen_truck_resources",
            "init_nitrogen_truck_resources 中指定加氮车的位置未调整到事件给定坐标。",
        ),
        (
            "充氧车发生故障不可用",
            verifier.check_oxygen_truck_unavailable,
            "init_oxygen_truck_resources",
            "init_oxygen_truck_resources 中指定充氧车仍可用或仍保留在可用资源列表中。",
        ),
        (
            "供电车初始位置调整为",
            verifier.check_power_cart_location,
            "init_power_cart_resources",
            "init_power_cart_resources 中指定供电车的位置未调整到事件给定坐标。",
        ),
        (
            "气源车发生故障不可用",
            verifier.check_air_source_car_unavailable,
            "init_air_source_car_resources",
            "init_air_source_car_resources 中指定气源车仍可用或仍保留在可用资源列表中。",
        ),
        (
            "液压车初始位置调整为",
            verifier.check_hydraulic_cart_location,
            "init_hydraulic_cart_resources",
            "init_hydraulic_cart_resources 中指定液压车的位置未调整到事件给定坐标。",
        ),
        (
            "维修车发生故障不可用",
            verifier.check_maintenance_vehicle_unavailable,
            "init_maintenance_vehicle_resources",
            "init_maintenance_vehicle_resources 中指定维修车仍可用或仍保留在可用资源列表中。",
        ),
        (
            "消防车初始位置调整为",
            verifier.check_fire_vehicle_location,
            "init_fire_vehicle_resources",
            "init_fire_vehicle_resources 中指定消防车的位置未调整到事件给定坐标。",
        ),
        (
            "牵引任务目标站位调整为",
            verifier.check_towing_task_location,
            "init_towing_tasks",
            "init_towing_tasks 中指定牵引任务目标站位未调整到事件给定坐标。",
        ),
        (
            "加油任务改为优先执行",
            verifier.check_refueling_task_priority,
            "init_refueling_tasks",
            "init_refueling_tasks 中指定加油任务未标记为优先执行。",
        ),
        (
            "加氮任务目标站位调整为",
            verifier.check_nitrogen_task_location,
            "init_nitrogen_filling_tasks",
            "init_nitrogen_filling_tasks 中指定加氮任务目标站位未调整到事件给定坐标。",
        ),
        (
            "充氧任务改派至站位",
            verifier.check_oxygen_task_location,
            "init_oxygen_filling_tasks",
            "init_oxygen_filling_tasks 中指定充氧任务目标站位未调整到事件给定坐标。",
        ),
        (
            "供电任务目标站位调整为",
            verifier.check_power_task_location,
            "init_power_supply_tasks",
            "init_power_supply_tasks 中指定供电任务目标站位未调整到事件给定坐标。",
        ),
        (
            "供气任务改派至站位",
            verifier.check_air_task_location,
            "init_air_supply_tasks",
            "init_air_supply_tasks 中指定供气任务目标站位未调整到事件给定坐标。",
        ),
        (
            "液压保障任务目标站位调整为",
            verifier.check_hydraulic_task_location,
            "init_hydraulic_support_tasks",
            "init_hydraulic_support_tasks 中指定液压保障任务目标站位未调整到事件给定坐标。",
        ),
        (
            "维修保障任务改为优先执行",
            verifier.check_maintenance_task_priority,
            "init_maintenance_tasks",
            "init_maintenance_tasks 中指定维修保障任务未标记为优先执行。",
        ),
        (
            "检查任务目标站位调整为",
            verifier.check_inspection_task_location,
            "init_inspection_tasks",
            "init_inspection_tasks 中指定检查任务目标站位未调整到事件给定坐标。",
        ),
        (
            "消防监护任务改派至站位",
            verifier.check_fire_watch_task_location,
            "init_fire_watch_tasks",
            "init_fire_watch_tasks 中指定消防监护任务目标站位未调整到事件给定坐标。",
        ),
        (
            "挂载弹药任务目标站位调整为",
            verifier.check_ammo_task_location,
            "init_tasks",
            "init_tasks 中指定挂载弹药任务目标站位未调整到事件给定坐标。",
        ),
        (
            "四个点发生故障",
            verifier.check_route_reroute,
            "route_planning",
            "route_planning 仍会经过故障站位，或没有正确绕开四个故障点。",
        ),
        (
            "以该点为终点的调整为",
            verifier.check_route_endpoint_change,
            "route_planning",
            "route_planning 以故障站位为终点时，没有重定向到事件给定的新终点。",
        ),
    ]
    for marker, check, function_name, reason in checks:
        if marker in event:
            try:
                return check(event), function_name, reason
            except Exception as exc:
                return False, function_name, f"{reason} 检查调用失败：{exc}"
    return False, "unknown", "review 不认识该突发事件类型。"


def build_feedback(solved_count, total, unsolved):
    if not unsolved:
        return f"review 通过 {solved_count}/{total}，所有突发事件均已解决。"
    lines = [f"review 通过 {solved_count}/{total}，仍未解决："]
    for item in unsolved:
        lines.append(f"- {item['function']}: {item['event']}\n  原因: {item['reason']}")
    return "\n".join(lines)


def run_verify_case(file_path, emergency_list, return_dict):
    spec = importlib.util.spec_from_file_location("test_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    verifier = DynamicVerifier(module)
    solved_count = 0
    solved_events = []
    unsolved = []

    for event in emergency_list:
        is_solved, function_name, reason = verify_single_event(verifier, event)
        event_result = {"event": event, "function": function_name}
        if is_solved:
            solved_count += 1
            solved_events.append(event_result)
        else:
            event_result["reason"] = reason
            unsolved.append(event_result)

    return_dict["result"] = {
        "total": len(emergency_list),
        "solved": solved_count,
        "solved_events": solved_events,
        "unsolved": unsolved,
        "feedback": build_feedback(solved_count, len(emergency_list), unsolved),
    }
