#!/usr/bin/env python3
"""会话钩子（Session Hook）——把「Agent 没打收尾标签」这件事变成可见信号（G4 · no_signoff）。

设计背景（为何需要）：
  收尾信号块依赖 Agent 在会话结束时输出并记录。若 Agent 没执行，数据上就像会话没
  发生过——「没记」本身是不可见的。no_signoff 缺失检测把沉默变成信号：会话开始钩子
  检查上一次会话是否留了收尾标记，没留则追加一行 L0·no_signoff 信号，让监控端能
  客观量化「Agent 执行率」，从而判断是 SKILL.md 措辞失效还是用户关了采集。

用法（SKILL.md A.2 会话钩子，均为静默执行、失败不阻塞、不打扰用户）：
  python scripts/session_hook.py begin [--dir <技能目录>]   # 会话开始：检测 + 更新状态
  python scripts/session_hook.py end   [--dir <技能目录>]   # 会话结束：标记已收尾（收尾块之后调用）

状态文件：<技能目录>/.session_state.json（运行时产物，发布时排除）：
  {"last_start_ts": "...", "last_signoff": false}

边界（防误报）：
  - 首次运行（无状态文件）：只建状态，不记 no_signoff（没有历史可判）。
  - `.optin=off`：本地记录关闭，跳过检测与记录。
  - 非信号技能（无 references/signals.md）：跳过。
  - begin 未结束又 begin（上次未收尾）：记一条 no_signoff。

零 PII：只写方法层标签 + 事件名；不读对话内容、不读用户文件。
"""
import json
import os
import sys
import uuid
from datetime import datetime, timezone

STATE_NAME = ".session_state.json"
LOCK_NAME = ".session_hook.lock"
SIGNALS_MD = os.path.join("references", "signals.md")


def _utcnow_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _optin_on(skill_dir):
    """本地记录开关：.optin 不存在 = 默认 on（安装即开）；存在则以内容为准。"""
    p = os.path.join(skill_dir, ".optin")
    try:
        if os.path.exists(p):
            return open(p, encoding="utf-8").read().strip().lower() in ("1", "on", "true", "yes")
        return True
    except Exception:
        return True


def _read_anon_id(skill_dir):
    try:
        p = os.path.join(skill_dir, ".anon_id")
        if os.path.exists(p):
            return open(p, encoding="utf-8").read().strip()
    except Exception:
        pass
    return None


def _read_skill_version(skill_dir):
    try:
        md = open(os.path.join(skill_dir, "SKILL.md"), encoding="utf-8").read()
        import re
        m = re.search(r"^version:\s*([\d.]+)", md, re.M)
        return m.group(1) if m else None
    except Exception:
        return None


def _append_signal(skill_dir, sig):
    path = os.path.join(skill_dir, "signals-log.jsonl")
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(sig, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        return True
    except Exception:
        return False


def _read_state(skill_dir):
    p = os.path.join(skill_dir, STATE_NAME)
    try:
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8"))
    except Exception:
        pass
    return None


def _write_state(skill_dir, state):
    p = os.path.join(skill_dir, STATE_NAME)
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
            f.flush()
    except Exception:
        pass


def cmd_begin(skill_dir):
    """会话开始钩子：检测上次未收尾 → 记 no_signoff；更新状态（本次开始=未收尾）。"""
    name = os.path.basename(skill_dir.rstrip("/\\"))
    if not os.path.exists(os.path.join(skill_dir, SIGNALS_MD)):
        print(f"[session] [{name}] 非信号技能，跳过")
        return 0
    if not _optin_on(skill_dir):
        print(f"[session] [{name}] 本地记录关闭（.optin=off），跳过")
        return 0

    prev = _read_state(skill_dir)
    if prev is None:
        # 首次：只建状态，不记（防误报——没有历史可判）
        _write_state(skill_dir, {"last_start_ts": _utcnow_iso(), "last_signoff": False})
        print(f"[session] [{name}] 首跑：仅建会话状态，不检测")
        return 0

    if prev.get("last_signoff") is False:
        # 上次会话开始了但未留收尾标记 → 把「没记」变成可见信号
        sig = {
            "ts": _utcnow_iso(),
            "signal_id": str(uuid.uuid4()),
            "client_signal_id": str(uuid.uuid4()),
            "skill_slug": name,
            "skill_version": _read_skill_version(skill_dir),
            "method_layer": "L0",
            "event": "no_signoff",
            "weight": 1,
            "note": "",
            "anon_id": _read_anon_id(skill_dir) or "",
        }
        ok = _append_signal(skill_dir, sig)
        print(f"[session] [{name}] 检测到上次会话未收尾 → 记录 L0·no_signoff（{'✓' if ok else '✗ 写入失败'}）")
    else:
        print(f"[session] [{name}] 上次会话已收尾，无需检测")

    _write_state(skill_dir, {"last_start_ts": _utcnow_iso(), "last_signoff": False})
    return 0


def cmd_end(skill_dir):
    """会话结束钩子：标记已收尾（在输出收尾块、写收尾信号之后调用）。"""
    name = os.path.basename(skill_dir.rstrip("/\\"))
    if not os.path.exists(os.path.join(skill_dir, SIGNALS_MD)):
        print(f"[session] [{name}] 非信号技能，跳过")
        return 0
    if not _optin_on(skill_dir):
        print(f"[session] [{name}] 本地记录关闭，跳过")
        return 0
    _write_state(skill_dir, {"last_start_ts": _utcnow_iso(), "last_signoff": True})
    print(f"[session] [{name}] 会话已标记收尾")
    return 0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = [a for a in sys.argv[1:] if a.startswith("--")]
    if not args or args[0] not in ("begin", "end") or "--help" in opts or "-h" in opts:
        print(__doc__)
        return 2
    cmd = args[0]
    skill_dir = "."
    for i, a in enumerate(sys.argv[1:]):
        if a == "--dir" and i + 1 < len(sys.argv[1:]):
            skill_dir = sys.argv[i + 2]
    return cmd_begin(skill_dir) if cmd == "begin" else cmd_end(skill_dir)


if __name__ == "__main__":
    sys.exit(main())
