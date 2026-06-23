"""验证代码是否解决相应突发事件 (port)"""

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

    def check_resource_unavailable(self, text):
        match = re.search(r"id为(\d+)的资源", text)
        if not match:
            return False, "事件格式无法解析：缺少资源 id。"
        target_id = int(match.group(1))
        try:
            resources = self.module.init_resources(15)
        except Exception as exc:
            return False, f"调用 init_resources(15) 失败：{exc}"
        ids = [resource.get("id") for resource in resources]
        if target_id not in ids:
            return True, ""
        return False, f"init_resources(15) 返回的资源 id 仍包含不可用资源 {target_id}；当前 ids={ids}。"

    def check_vessel_delay(self, text):
        match = re.search(r"第(\d+)艘", text)
        if not match:
            return False, "事件格式无法解析：缺少船舶序号。"
        idx = int(match.group(1)) - 1 if int(match.group(1)) != 0 else 0
        try:
            vessels = self.module.init_cranes(10)
        except Exception as exc:
            return False, f"调用 init_cranes(10) 失败：{exc}"
        if idx >= len(vessels):
            return False, f"init_cranes(10) 只返回 {len(vessels)} 艘船，无法检查第 {idx + 1} 艘。"
        expected_time = time.strftime(
            "%H:%M:%S",
            time.localtime(
                time.mktime(time.strptime("8:00:00", "%H:%M:%S"))
                + 3 * 60 * idx
                + 10 * 60
            ),
        )
        actual_time = vessels[idx].get("time")
        if actual_time == expected_time:
            return True, ""
        return False, f"第 {idx + 1} 艘船 time 应为 {expected_time}，实际为 {actual_time}。"

    def check_duration_extension(self, text):
        match = re.search(r"id为(\d+)的船舶", text)
        if not match:
            return False, "事件格式无法解析：缺少船舶 id。"
        target_id = int(match.group(1))
        try:
            vessels = self.module.init_cranes(10)
        except Exception as exc:
            return False, f"调用 init_cranes(10) 失败：{exc}"
        target = next((vessel for vessel in vessels if vessel.get("id") == target_id), None)
        if target is None:
            return False, f"init_cranes(10) 未返回 id={target_id} 的船舶。"
        actual_duration = target.get("duration")
        if str(actual_duration) == "20" or actual_duration == 20:
            return True, ""
        return False, f"id={target_id} 的船舶 duration 应为 20，实际为 {actual_duration}。"

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
    if "资源不可用" in event:
        solved, reason = verifier.check_resource_unavailable(event)
        return solved, "init_resources", reason
    if "延迟" in event:
        solved, reason = verifier.check_vessel_delay(event)
        return solved, "init_cranes", reason
    if "四个点发生故障" in event:
        solved, reason = verifier.check_route_fault(event)
        return solved, "route_planning", reason
    if "时长延长" in event:
        solved, reason = verifier.check_duration_extension(event)
        return solved, "init_cranes", reason
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
