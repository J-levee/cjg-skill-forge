#!/usr/bin/env python3
"""forge-signal-kit.py — 信号套件注入器（模板渲染器版 v3.0.2）。

锻造炉（A）产出的技能（B）必须自带信号回传能力，否则用户用 B 的信号到不了藏经阁（C），
闭环断裂。本工具把 A 的信号套件**按目标技能定制**注入 B：
  - scripts/upload_signals.py     回传（幂等/白名单/云上传默认关）
  - scripts/signal_control.py     用户透明控制（查看/导出/删除）
  - scripts/download_signals.py   跨设备同步（拉回合并）
  - scripts/session_hook.py       会话钩子（start/signal/usage/end，信号采集核心入口）
  - scripts/capture_skill_edits.py 被动改动捕获（与 signals.md 引用一致）
  - cloud_config.json             藏经阁端点（仅公网 URL，零密钥）
  - references/signals.md         信号规范（**按目标技能渲染**：slug/version/示例全部替换）
  - 状态文件 bootstrap：.optin=on（本地记录安装即开）、.cloud_optin=off（云端默认关）
  - SKILL.md 注入 A.1（交互指令表）+ A.2（会话钩子）段落（按目标技能生成）

用法：
  python forge-signal-kit.py inject <目标技能目录> [--force]   # 注入（模板渲染）
  python forge-signal-kit.py --check <目标技能目录>            # 闭环完整性校验
退出码：0=完整；2=缺件/不完整
"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_SKILL = os.path.dirname(HERE)  # 本技能（锻造炉）根目录

# 信号套件清单：相对路径 -> 源文件位置
KIT = [
    ("scripts/upload_signals.py", "scripts/upload_signals.py"),
    ("scripts/signal_control.py", "scripts/signal_control.py"),
    ("scripts/download_signals.py", "scripts/download_signals.py"),
    ("scripts/session_hook.py", "scripts/session_hook.py"),
    ("scripts/capture_skill_edits.py", "scripts/capture_skill_edits.py"),
    ("cloud_config.json", "cloud_config.json"),
    ("references/signals.md", "references/signals.md"),
]

A1A2_TEMPLATE = """## A.1 交互指令响应（强制 · 不可忽略）

用户说出下列任一指令，**必须立即执行对应动作**，不得当作闲聊：

| 用户指令 | 必须执行 |
|---|---|
| 「开启云同步」 | 写 `.cloud_optin` = `on` |
| 「别传了」 | 写 `.cloud_optin` = `off` |
| 「别记了」/「再开」 | 写 `.optin` = `off` / `on` |
| 「查看我的信号」 | 跑 `python scripts/signal_control.py view` |
| 「删除我的信号」 | 跑 `python scripts/signal_control.py delete`（需用户确认） |
| 「同步我的信号」 | 跑 `python scripts/download_signals.py pull` |

> **命令执行约定**：运行任何 `scripts/*.py` 前，先定位本技能目录并进入（形如 `~/.workbuddy/skills/@<用户名>/{slug}/`，用 `ls -d ~/.workbuddy/skills/*/{slug}` 找到后 `cd` 进去），再执行。

## A.2 会话钩子 + 收尾信号块（强制 · 本地记录默认开可随时关）

**会话开始（首次交互时静默执行，一条命令）**：`python scripts/session_hook.py start`
（内部自动：补传上次积累 + 拉回云端历史 + 缺失检测；失败不阻塞、不打扰用户。）

**会话结束（必须执行；结束时记录方法层信号——这是会话完成的标志）**：
1. 输出收尾信号块（给用户看，严格格式）：`[信号] L<层>·<事件>`——**只写标签，不加括号解释**（如 `[信号] L3·helpful`）；本地记录关闭时输出 `[信号] off`；
2. 写 signals-log 由脚本完成（**禁止手写 JSON**）：`python scripts/session_hook.py end --event L3:helpful`；
3. 本次调用过外部服务才做客观汇报：对用户说 `[使用] <服务>×N 成功M 失败K 耗时Xms`，并跑 `python scripts/session_hook.py usage --calls N --success M`；
4. 若已开云同步：`python scripts/upload_signals.py` 即时回传。

仅方法层标签，零对话内容、零身份，只写本技能目录内的运行时文件。用户说「别记了」即关、「再开」恢复。
"""


def _read_frontmatter(skill_dir):
    """读目标技能 frontmatter：slug/name/version。返回 dict。"""
    out = {"slug": None, "name": None, "version": None}
    p = os.path.join(skill_dir, "SKILL.md")
    try:
        md = open(p, encoding="utf-8").read()
    except Exception:
        return out
    fm = md.split("---", 2)[1] if md.startswith("---") else md
    for key in out:
        m = re.search(rf"^{key}:\s*([^\n]+)", fm, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"').strip("'")
    return out


def _render_signals_md(skill_dir, force=False):
    """把锻造炉的 signals.md 渲染为目标技能版：slug/version 示例全部替换 + 适配头。"""
    src = os.path.join(SRC_SKILL, "references", "signals.md")
    if not os.path.exists(src):
        return False
    meta = _read_frontmatter(skill_dir)
    slug = meta["slug"] or meta["name"] or os.path.basename(skill_dir.rstrip("/\\"))
    version = meta["version"] or "0.0.0"
    text = open(src, encoding="utf-8").read()
    # 1) 示例值替换：锻造炉 slug/version → 目标技能（signals.md 内所有示例与 one-liner）
    text = text.replace("cjg-skill-forge", slug)
    text = re.sub(r"2\.9\.\d+", version, text)
    # 2) 头部注入适配说明（说明本文件已按目标技能渲染）
    adapter = (f"> 本文件由「技能锻造炉」为 **{slug} v{version}** 定制注入（{__file__.split(chr(92))[-1]}）：\n"
               f"> 全文示例的 skill_slug / skill_version 已按本技能替换；层码 L1–L7 语义可按本技能的实际能力层调整。\n\n")
    if not text.startswith("> 本文件由"):
        text = adapter + text
    dst = os.path.join(skill_dir, "references", "signals.md")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)
    return True


def _bootstrap_state(skill_dir, force=False):
    """状态文件 bootstrap：.optin=on（安装即开）、.cloud_optin=off（云端默认关）。
    .anon_id 不预建——首次上传时服务端签发并回写。"""
    optin = os.path.join(skill_dir, ".optin")
    if not os.path.exists(optin) or force:
        with open(optin, "w", encoding="utf-8") as f:
            f.write("on")
    cloud = os.path.join(skill_dir, ".cloud_optin")
    if not os.path.exists(cloud) or force:
        with open(cloud, "w", encoding="utf-8") as f:
            f.write("off")
    return True


def _inject_a1a2(skill_dir, force=False):
    """在产出技能 SKILL.md 注入 A.1/A.2 段落（按目标技能 slug 渲染；已含则跳过）。"""
    p = os.path.join(skill_dir, "SKILL.md")
    md = open(p, encoding="utf-8").read()
    if "## A.1 交互指令响应" in md and not force:
        return True  # 已有，不重复
    slug = (_read_frontmatter(skill_dir)["slug"] or "本技能")
    section = A1A2_TEMPLATE.format(slug=slug)
    # 追加到 §零（进化燃料）之后；找不到就追加到文末
    anchor = None
    m = re.search(r"(## 零、进化燃料.*?)(?=\n## |\Z)", md, re.S)
    if m:
        anchor = m.end(0)
    if anchor:
        md = md[:anchor] + "\n" + section + md[anchor:]
    else:
        md = md.rstrip() + "\n\n---\n\n" + section
    with open(p, "w", encoding="utf-8") as f:
        f.write(md)
    return True


def _missing(skill_dir):
    miss = []
    for rel, _ in KIT:
        if not os.path.exists(os.path.join(skill_dir, rel)):
            miss.append(rel)
    return miss


def _check_loop_integrity(skill_dir):
    """闭环完整性校验（P0-5）。返回 (ok, problems[])。"""
    problems = []
    meta = _read_frontmatter(skill_dir)
    slug = meta["slug"] or meta["name"] or os.path.basename(skill_dir.rstrip("/\\"))
    # ① KIT 全部存在
    miss = _missing(skill_dir)
    if miss:
        problems.append(f"缺套件件: {miss}")
    # ② signals.md 引用一致性：引用的 scripts/ 都存在于目标技能
    sig_p = os.path.join(skill_dir, "references", "signals.md")
    if os.path.exists(sig_p):
        sig = open(sig_p, encoding="utf-8").read()
        refs = sorted(set(re.findall(r"scripts/([a-z_]+\.py)", sig)))
        for ref in refs:
            if not os.path.exists(os.path.join(skill_dir, "scripts", ref)):
                problems.append(f"signals.md 引用不存在脚本: scripts/{ref}")
        # ③ slug 一致：产出技能不应残留锻造炉 slug；应含目标技能 slug
        #   （锻造炉自身 slug=cjg-skill-forge 时跳过"残留"检查——自身含自己 slug 是正常的）
        if slug != "cjg-skill-forge" and "cjg-skill-forge" in sig:
            problems.append("signals.md 仍含锻造炉 slug（未渲染）: cjg-skill-forge")
        if slug not in sig:
            problems.append(f"signals.md 未含目标技能 slug: {slug}")
    # ④ 状态文件已 bootstrap
    for st in (".optin", ".cloud_optin"):
        if not os.path.exists(os.path.join(skill_dir, st)):
            problems.append(f"状态文件缺失: {st}")
    # ⑤ SKILL.md 信号段
    sk = open(os.path.join(skill_dir, "SKILL.md"), encoding="utf-8").read()
    if "## A.1 交互指令响应" not in sk or "## A.2 会话钩子" not in sk:
        problems.append("SKILL.md 缺 A.1/A.2 信号段")
    return (not problems), problems


def inject(skill_dir, force=False):
    skill_dir = os.path.abspath(skill_dir)
    if not os.path.isdir(skill_dir) or not os.path.exists(os.path.join(skill_dir, "SKILL.md")):
        print(f"✗ 目标不是技能目录（缺 SKILL.md）: {skill_dir}")
        return False
    meta = _read_frontmatter(skill_dir)
    slug = meta["slug"] or meta["name"] or os.path.basename(skill_dir.rstrip("/\\"))
    print(f"== 注入信号套件到 {slug} v{meta['version'] or '?'} ==")
    for rel, src_rel in KIT:
        src = os.path.join(SRC_SKILL, src_rel)
        dst = os.path.join(skill_dir, rel)
        if not os.path.exists(src):
            print(f"⚠ 源缺失（锻造炉自身不完整）: {src_rel}")
            continue
        if rel == "references/signals.md":
            # signals.md 走模板渲染（不复制）
            ok = _render_signals_md(skill_dir, force)
            print(f"  {'✓' if ok else '✗'} 渲染: references/signals.md（slug→{slug}, v{meta['version'] or '0.0.0'}）")
            continue
        if os.path.exists(dst) and not force:
            print(f"  - 已存在（跳过）: {rel}")
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  ✓ 注入: {rel}")
    # 状态文件 bootstrap（断点3）
    _bootstrap_state(skill_dir, force)
    print(f"  ✓ bootstrap 状态文件: .optin=on（本地记录安装即开）· .cloud_optin=off（云端默认关）")
    # A.1/A.2 段落注入（断点4）
    _inject_a1a2(skill_dir, force)
    print(f"  ✓ SKILL.md 注入 A.1 交互指令表 + A.2 会话钩子段")
    # 闭环完整性自检（注入后立即验证）
    ok, problems = _check_loop_integrity(skill_dir)
    if not ok:
        print(f"✗ 注入后闭环完整性未通过: {problems}")
        return False
    print(f"✓ 信号套件完整且闭环就绪: {skill_dir}")
    print(f"  下一步：发布前跑 writing_gate（W10 校验信号套件）——B 的终端用户开启云同步后即可参与进化闭环。")
    return True


def check_only(skill_dir):
    skill_dir = os.path.abspath(skill_dir)
    ok, problems = _check_loop_integrity(skill_dir)
    if not ok:
        print(f"✗ 闭环完整性未通过（{len(problems)} 项）:")
        for p in problems:
            print(f"   - {p}")
        print(f"  修复: python scripts/forge-signal-kit.py inject {skill_dir} --force")
        return False
    print(f"✓ 信号闭环完整（套件/引用/slug/状态/信号段）: {skill_dir}")
    return True


def main():
    args = sys.argv[1:]
    if len(args) < 2 or "--help" in args or "-h" in args:
        print(__doc__)
        sys.exit(0 if "--help" in args else 2)
    if args[0] == "--check":
        sys.exit(0 if check_only(args[1]) else 2)
    if args[0] == "inject":
        force = "--force" in args
        target = args[1]
        sys.exit(0 if inject(target, force) else 2)
    print(__doc__)
    sys.exit(2)


if __name__ == "__main__":
    main()
