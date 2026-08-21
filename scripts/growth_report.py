#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""技能成长报告（本地可见化"越用越牛"）。

读本机 signals-log.jsonl，输出用户自身用法的轻量成长摘要：
  - 时间窗（默认 30 天）内信号条数
  - 覆盖的方法层（L1–L7）数
  - 建设性事件占比（helpful / suggestion vs 其余）
  - 熟练度等级 Lv.1–5（覆盖层数 + 信号总数 + 连续使用天数）

仅陈述用户自身行为，不谎称"已自动优化"（那属创作者侧云端动作）。
--with-cloud 钩子预留（默认不调，待 Wave B 聚合后端就绪后接入互惠回执）。
"""
import os
import sys
import json
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DIR = os.path.dirname(HERE)
LAYER_KEYS = ["L1", "L2", "L3", "L4", "L5", "L6", "L7"]
POSITIVE = ("helpful", "suggestion")
NEGATIVE = ("unhelpful", "confusion", "misdiagnosis", "abandoned")


def _read_lines(dir_):
    path = os.path.join(dir_, "signals-log.jsonl")
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [json.loads(l) for l in f if l.strip()]
    except Exception:
        return []


def _parse_ts(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def cmd_report(dir_, days=30, with_cloud=False):
    lines = _read_lines(dir_)
    if not lines:
        print("[growth] 本机暂无信号记录。用一阵子后，说\"我的技能成长\"就能看到你的用法沉淀。")
        return
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    recent = [l for l in lines if (_parse_ts(l.get("ts")) or now) >= cutoff]
    if not recent:
        print(f"[growth] 最近 {days} 天没有新信号（历史共 {len(lines)} 条）。")
        return
    layers = {l.get("method_layer") for l in recent if l.get("method_layer")}
    positive = sum(1 for l in recent if l.get("event") in POSITIVE)
    negative = sum(1 for l in recent if l.get("event") in NEGATIVE)
    days_used = {
        (_parse_ts(l.get("ts")).date().isoformat() if _parse_ts(l.get("ts")) else "?")
        for l in recent
    }
    cov = len(layers & set(LAYER_KEYS))
    total = len(recent)
    distinct_days = len(days_used - {"?"})
    score = cov * 3 + min(total, 50) // 10 + min(distinct_days, 14) // 3
    lv = max(1, min(5, score // 6 + 1))
    print(f"[growth] 过去 {days} 天，你为本技能贡献了 {total} 条方法层反馈，")
    print(f"         覆盖了 {cov} 个能力层（L1–L7），熟练度 Lv.{lv}。")
    if positive or negative:
        ratio = positive / (positive + negative) * 100 if (positive + negative) else 0
        tone = "建设性为主" if ratio >= 50 else "探索为主"
        print(f"         其中建设性反馈占 {ratio:.0f}%（采纳/建议 vs 纠正/卡住/误判/放弃）——你的用法以{tone}。")
    print("         这些线索让本技能更懂你的用法（本地记录，零原文零身份）。")
    if with_cloud:
        print("[growth] （--with-cloud 暂未接入：待藏经阁·易筋聚合后端就绪后，可追加\"社区因你这类用户本周改进 N 处\"）")


def main():
    args = sys.argv[1:]
    dir_ = DEFAULT_DIR
    with_cloud = "--with-cloud" in args
    rest = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--dir":
            if i + 1 < len(args):
                dir_ = args[i + 1]
            i += 2
        else:
            rest.append(a)
            i += 1
    days = 30
    if "--days" in rest:
        try:
            days = int(rest[rest.index("--days") + 1])
        except Exception:
            pass
    if not rest or rest[0] in ("report", "growth"):
        cmd_report(dir_, days=days, with_cloud=with_cloud)
    else:
        print(__doc__)
        print("用法：python growth_report.py [report] [--days 30] [--with-cloud] [--dir <技能目录>]")


if __name__ == "__main__":
    main()
