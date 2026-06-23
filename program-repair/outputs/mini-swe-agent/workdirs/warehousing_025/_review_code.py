"""验证代码是否解决相应突发事件 (warehousing)"""

import re
import time
import importlib.util


class DynamicVerifier:
    def __init__(self, module):
        self.module = module

    def _tuple_path(self, path):
        return [
            (int(point[0]), int(point[1]))
            for point in (path or [])
            if isinstance(point, (list, tuple)) and len(point) == 2
        ]

    def check_truck_interval(self, text):
        match = re.search(r"从第(\d+)辆货车开始间隔改为(\d+)分钟", text)
        if not match:
            return False, "事件格式无法解析：缺少货车序号或新间隔。"
        start_idx = int(match.group(1)) - 1 if int(match.group(1)) > 0 else 0
        new_interval = int(match.group(2))
        try:
            trucks = self.module.init_truck_arrival_time(15)
        except Exception as exc:
            return False, f"调用 init_truck_arrival_time(15) 失败：{exc}"
        if start_idx + 1 >= len(trucks):
            return False, f"init_truck_arrival_time(15) 只返回 {len(trucks)} 辆货车，无法检查第 {start_idx + 1} 辆后的间隔。"
        t1 = time.mktime(time.strptime(trucks[start_idx]["arrival_time"], "%H:%M:%S"))
        t2 = time.mktime(time.strptime(trucks[start_idx + 1]["arrival_time"], "%H:%M:%S"))
        actual_interval = int((t2 - t1) / 60)
        if abs((t2 - t1) - new_interval * 60) < 1:
            return True, ""
        return False, f"第 {start_idx + 1} 辆到下一辆的间隔应为 {new_interval} 分钟，实际为 {actual_interval} 分钟。"

    def check_zone_stock_increase(self, text):
        match = re.search(r"(Zone_\d+)堆积区当前库存增加(\d+)", text)
        if not match:
            return False, "事件格式无法解析：缺少堆积区 id 或库存增量。"
        target_id = match.group(1)
        expected_stock = int(match.group(2))
        try:
            zones = self.module.init_stacking_zones()
        except Exception as exc:
            return False, f"调用 init_stacking_zones() 失败：{exc}"
        target = next((zone for zone in zones if zone.get("id") == target_id), None)
        if target is None:
            return False, f"init_stacking_zones() 未返回 {target_id}，无法检查库存。"
        actual_stock = target.get("current_stock", 0)
        if actual_stock == expected_stock:
            return True, ""
        return False, f"{target_id}.current_stock 应为 {expected_stock}，实际为 {actual_stock}。"

    def check_zone_capacity_reduce(self, text):
        match = re.search(r"(Zone_\d+)堆积区最大容量缩减至(\d+)", text)
        if not match:
            return False, "事件格式无法解析：缺少堆积区 id 或新容量。"
        target_id = match.group(1)
        expected_capacity = int(match.group(2))
        try:
            zones = self.module.init_stacking_zones()
        except Exception as exc:
            return False, f"调用 init_stacking_zones() 失败：{exc}"
        target = next((zone for zone in zones if zone.get("id") == target_id), None)
        if target is None:
            return False, f"init_stacking_zones() 未返回 {target_id}，无法检查容量。"
        actual_capacity = target.get("max_capacity")
        if actual_capacity == expected_capacity:
            return True, ""
        return False, f"{target_id}.max_capacity 应为 {expected_capacity}，实际为 {actual_capacity}。"

    def check_zone_unavailable(self, text):
        match = re.search(r"(Zone_\d+)堆积区发生故障不可用", text)
        if not match:
            return False, "事件格式无法解析：缺少堆积区 id。"
        target_id = match.group(1)
        try:
            zones = self.module.init_stacking_zones()
        except Exception as exc:
            return False, f"调用 init_stacking_zones() 失败：{exc}"
        ids = [zone.get("id") for zone in zones]
        if target_id not in ids:
            return True, ""
        return False, f"init_stacking_zones() 返回的堆积区 id 仍包含故障堆积区 {target_id}；当前 ids={ids}。"

    def check_forklift_unavailable(self, text):
        match = re.search(r"(Forklift_\d+)叉车发生故障不可用", text)
        if not match:
            return False, "事件格式无法解析：缺少叉车 id。"
        target_id = match.group(1)
        try:
            forklifts = self.module.init_forklifts()
        except Exception as exc:
            return False, f"调用 init_forklifts() 失败：{exc}"
        ids = [forklift.get("id") for forklift in forklifts]
        if target_id not in ids:
            return True, ""
        return False, f"init_forklifts() 返回的叉车 id 仍包含故障叉车 {target_id}；当前 ids={ids}。"

    def check_forklift_location(self, text):
        match = re.search(r"(Forklift_\d+)叉车初始位置调整为\((\d+),(\d+)\)", text)
        if not match:
            return False, "事件格式无法解析：缺少叉车 id 或新位置。"
        target_id = match.group(1)
        expected_location = (int(match.group(2)), int(match.group(3)))
        try:
            forklifts = self.module.init_forklifts()
        except Exception as exc:
            return False, f"调用 init_forklifts() 失败：{exc}"
        target = next((forklift for forklift in forklifts if forklift.get("id") == target_id), None)
        if target is None:
            return False, f"init_forklifts() 未返回 {target_id}，无法检查位置。"
        actual_location = target.get("location")
        if actual_location == expected_location or actual_location == list(expected_location):
            return True, ""
        return False, f"{target_id}.location 应为 {expected_location}，实际为 {actual_location}。"

    def check_route_fault(self, text):
        matches = re.findall(r"\((\d+),(\d+)\)", text)
        if len(matches) < 4:
            return False, "事件格式无法解析：没有找到四个故障站位。"
        fault_points = [(int(x), int(y)) for x, y in matches[:4]]
        reachable = []
        for point in fault_points:
            try:
                path = self.module.route_planning((0, 0), point)
            except Exception as exc:
                return False, f"调用 route_planning((0, 0), {point}) 失败：{exc}"
            if path is not None:
                reachable.append(point)
        try:
            normal_path = self._tuple_path(self.module.route_planning((0, 0), (10, 10)))
        except Exception as exc:
            return False, f"调用 route_planning((0, 0), (10, 10)) 失败：{exc}"
        blocked_on_path = [point for point in fault_points if point in set(normal_path)]
        if not reachable and not blocked_on_path:
            return True, ""
        pieces = []
        if reachable:
            pieces.append(f"故障站位仍可作为终点到达：{reachable}")
        if blocked_on_path:
            pieces.append(f"正常路径仍经过故障站位：{blocked_on_path}")
        return False, "；".join(pieces) + "。"

    def check_endpoint_change(self, text):
        match = re.search(r"站位\((\d+),(\d+)\).*调整为\((\d+),(\d+)\)", text)
        if not match:
            return False, "事件格式无法解析：缺少旧终点或新终点。"
        old_end = (int(match.group(1)), int(match.group(2)))
        new_end = (int(match.group(3)), int(match.group(4)))
        try:
            path = self._tuple_path(self.module.route_planning((0, 0), old_end))
        except Exception as exc:
            return False, f"调用 route_planning((0, 0), {old_end}) 失败：{exc}"
        actual_end = path[-1] if path else None
        if actual_end == new_end:
            return True, ""
        return False, f"以故障站位 {old_end} 为终点时，路径应重定向到 {new_end}，实际终点为 {actual_end}。"


def verify_single_event(verifier, event):
    if "间隔改为" in event:
        solved, reason = verifier.check_truck_interval(event)
        return solved, "init_truck_arrival_time", reason
    if "库存增加" in event:
        solved, reason = verifier.check_zone_stock_increase(event)
        return solved, "init_stacking_zones", reason
    if "容量缩减" in event:
        solved, reason = verifier.check_zone_capacity_reduce(event)
        return solved, "init_stacking_zones", reason
    if "堆积区发生故障不可用" in event:
        solved, reason = verifier.check_zone_unavailable(event)
        return solved, "init_stacking_zones", reason
    if "叉车发生故障不可用" in event:
        solved, reason = verifier.check_forklift_unavailable(event)
        return solved, "init_forklifts", reason
    if "叉车初始位置调整" in event:
        solved, reason = verifier.check_forklift_location(event)
        return solved, "init_forklifts", reason
    if "四个点发生故障" in event:
        solved, reason = verifier.check_route_fault(event)
        return solved, "route_planning", reason
    if "终点" in event:
        solved, reason = verifier.check_endpoint_change(event)
        return solved, "route_planning", reason
    return False, "unknown", "review 不认识该突发事件类型。"


def build_feedback(solved_count, total, unsolved):
    if not unsolved:
        return f"review 通过 {solved_count}/{total}，所有突发事件均已解决。"
    lines = [f"review 通过 {solved_count}/{total}，仍未解决："]
    for item in unsolved:
        lines.append(f"- {item['function']}: {item['event']}\n  原因: {item['reason']}")
    return "\n".join(lines)


def run_verify_case(file_path, emergency_list, return_dict):
    try:
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
    except Exception as exc:
        return_dict["error"] = str(exc)
