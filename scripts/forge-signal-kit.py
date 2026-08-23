#!/usr/bin/env python3
"""forge-signal-kit.py — 信号套件注入器（闭环断点修复：A→B 信号链路打通）。

锻造炉（A）产出的技能（B）必须自带信号回传能力，否则用户用 B 的信号到不了藏经阁（C），
闭环断裂。本工具把 A 的信号套件一键注入 B：
  - scripts/upload_signals.py   用户/创作者回传（幂等/白名单/默认关云上传）
  - scripts/signal_control.py   用户透明控制（查看/导出/删除）
  - scripts/download_signals.py 跨设备同步（L2 拉回合并）
  - cloud_config.json           藏经阁端点（仅公网 URL，零密钥）
  - references/signals.md       信号字段与事件规范
套件脚本均以自身 __file__ 推导技能目录（scripts/ 上一级），天然适配任何技能，无需改代码。

用法：
  python forge-signal-kit.py <目标技能目录> [--force]
  python forge-signal-kit.py --check <目标技能目录>   # 只校验不缺什么
退出码：0=完整；2=缺件（注入后返回 0）
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_SKILL = os.path.dirname(HERE)  # 本技能（锻造炉）根目录

# 信号套件清单：相对路径 -> 源文件位置
KIT = [
    ("scripts/upload_signals.py", "scripts/upload_signals.py"),
    ("scripts/signal_control.py", "scripts/signal_control.py"),
    ("scripts/download_signals.py", "scripts/download_signals.py"),
    ("cloud_config.json", "cloud_config.json"),
    ("references/signals.md", "references/signals.md"),
]


def _missing(skill_dir):
    miss = []
    for rel, _ in KIT:
        if not os.path.exists(os.path.join(skill_dir, rel)):
            miss.append(rel)
    return miss


def inject(skill_dir, force=False):
    skill_dir = os.path.abspath(skill_dir)
    if not os.path.isdir(skill_dir) or not os.path.exists(os.path.join(skill_dir, "SKILL.md")):
        print(f"✗ 目标不是技能目录（缺 SKILL.md）: {skill_dir}")
        return False
    for rel, src_rel in KIT:
        src = os.path.join(SRC_SKILL, src_rel)
        dst = os.path.join(skill_dir, rel)
        if not os.path.exists(src):
            print(f"⚠ 源缺失（锻造炉自身不完整）: {src_rel}")
            continue
        if os.path.exists(dst) and not force:
            print(f"  - 已存在（跳过）: {rel}")
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  ✓ 注入: {rel}")
    miss = _missing(skill_dir)
    if miss:
        print(f"✗ 注入后仍缺: {miss}")
        return False
    print(f"✓ 信号套件完整: {skill_dir}（{len(KIT)} 件）")
    print("  下一步：在 B 的 SKILL.md §零 确认信号说明已存在（writing_gate W5/W10 会校验）")
    return True


def check_only(skill_dir):
    miss = _missing(os.path.abspath(skill_dir))
    if miss:
        print(f"✗ 缺信号套件 {len(miss)} 件: {miss}")
        print("  运行: python scripts/forge-signal-kit.py <技能目录> 注入")
        return False
    print(f"✓ 信号套件完整（{len(KIT)} 件）: {os.path.abspath(skill_dir)}")
    return True


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        sys.exit(2)
    mode, target = args[0], args[1]
    if mode == "--check":
        sys.exit(0 if check_only(target) else 2)
    if mode == "inject" or mode == "--force" or not mode.startswith("-"):
        ok = inject(target, force=(mode == "--force" or "--force" in args))
        sys.exit(0 if ok else 2)
    print(__doc__)
    sys.exit(2)


if __name__ == "__main__":
    main()
