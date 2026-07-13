#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能锻造炉 (SkillForge) — 自带发布器 forge-publish.py

让「技能锻造炉」锻造出的技能，能由创作者本人在本地一键发布到多个技能平台，
无需记住各平台繁杂的发布命令。本脚本随「技能锻造炉」技能包分发，纯标准库、
零第三方依赖，任何装了 Python 的机器都能跑。

支持平台:
    - skillhub  (现支持)   https://skillhub.cn
    - clawhub   (现支持)
    - github    (roadmap, 接口已预留)
    - gitee     (roadmap, 接口已预留)

首次使用:
    1. 进入你锻造好的技能目录（含 SKILL.md）
    2. 运行:  python forge-publish.py --check           # 本地校验
    3. 运行:  python forge-publish.py --platform both --changelog "你的更新说明"
    4. 若提示某平台 CLI 未安装/未登录，按脚本打印的引导完成一次性准备即可

零密钥云端（方案C）:
    本脚本沿用藏经阁·易筋单版本双模态模型。技能包分发时 cloud_config.json 仅含
    公网 URL（零密钥），终端用户零配置即可匿名回传（/ingest/anon）；创作者审核
    提案所需 token 存本地开发环境（.deploy/cloud_open.json），绝不进包。

安全策略:
    - 净化 config.json 中的 email 字段为 null（其余凭据原样保留）
    - 发布后自动从备份恢复本地技能目录（含 .gitignore）
    - 若技能无 config.json 但有 config.example.json，临时生成净化版用于发布，
      发布后删除，绝不在本地留痕
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Optional

# ============================================================
# 路径与常量
# ============================================================
SKILLS_BASE = Path.home() / ".workbuddy" / "skills"
# 云端接入配置（方案C·零密钥）：cloud_config.json 仅含公网 URL，不含 token（SkillHub 拒绝点号隐藏文件）
CLOUD_CONFIG_FILE = "cloud_config.json"
DEFAULT_INGEST_URL = "https://1318491188-fpwsv5k3eh.ap-guangzhou.tencentscf.com"
DEFAULT_REGISTER_URL = "https://1318491188-1yxx8sqtw1.ap-guangzhou.tencentscf.com"
DEFAULT_PROPOSAL_URL = None  # 部署 cjg-proposal 后由 --proposal-url 注入；旧包留空兼容
SKILLHUB_API_HOST = "https://api.skillhub.cn"
SKILLHUB_CREDENTIALS = Path.home() / ".skillhub" / "credentials.json"
SKILLHUB_PYTHON = "python"
SKILLHUB_EXCLUDE_FILES = [".gitignore", ".cloud_token", ".cloud_config",
                          ".cloud_optin", ".optin"]
EMAIL_FIELD_HINTS = ("email", "mail", "_email", "contact_email")
_GENERATED = "__GENERATED__"

# 跨 agent 适配（roadmap，接口预留，暂不实现转换）
# 未来 --format {workbuddy, claude, codex} 会把 SKILL.md 转成目标 agent 格式再发
SUPPORTED_FORMATS = ["workbuddy"]


# ============================================================
# 工具函数
# ============================================================
def _read_frontmatter(skill_md: Path) -> dict:
    """读取 SKILL.md frontmatter 为 dict（简单 YAML 解析，仅支持平铺 key: value）"""
    if not skill_md.exists():
        return {}
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    data = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
                val = val[1:-1]
            data[key] = val
    return data


def read_version(skill_dir: Path) -> Optional[str]:
    v = _read_frontmatter(skill_dir / "SKILL.md").get("version")
    if v and re.match(r"^\d+(\.\d+){0,2}$", v):
        return v
    return None


def read_field(skill_dir: Path, field: str) -> Optional[str]:
    return _read_frontmatter(skill_dir / "SKILL.md").get(field)


def to_semver(version: str) -> str:
    parts = version.split(".")
    if len(parts) == 2:
        return f"{version}.0"
    return version


def ensure_frontmatter(skill_dir: Path, slug: str, display_name: str) -> bool:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False
    content = skill_md.read_text(encoding="utf-8")
    modified = False
    if not re.search(r"^slug:\s*\S+", content, re.MULTILINE):
        content = re.sub(r"(^---\n)", f"\\1slug: {slug}\n", content, count=1,
                         flags=re.MULTILINE)
        modified = True
    if display_name and not re.search(r"^displayName:\s*\S+", content, re.MULTILINE):
        content = re.sub(r"(^slug:.*\n)", f"\\1displayName: {display_name}\n",
                         content, count=1, flags=re.MULTILINE)
        modified = True
    if modified:
        skill_md.write_text(content, encoding="utf-8")
    return modified


def _is_email_field(key: str) -> bool:
    kl = key.lower()
    return any(hint in kl for hint in EMAIL_FIELD_HINTS)


def generic_sanitize_config(skill_dir: Path) -> dict:
    """净化 config.json：email 字段置 null；无 config 但有 example 则临时生成。"""
    src = skill_dir / "config.json"
    example = skill_dir / "config.example.json"
    backup: dict = {}
    if src.exists():
        dst = Path(tempfile.gettempdir()) / f"_forgepub_{skill_dir.name}_config.json"
        shutil.copy2(src, dst)
        backup["config.json"] = dst
        try:
            data = json.loads(src.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        changed = False
        for k in list(data.keys()):
            if _is_email_field(k) and data.get(k) is not None:
                data[k] = None
                changed = True
        if changed:
            src.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return backup
    if example.exists():
        try:
            data = json.loads(example.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        for k in list(data.keys()):
            if _is_email_field(k):
                data[k] = None
        src.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        backup["config.json"] = _GENERATED
        return backup
    return backup


def backup_and_remove(skill_dir: Path, filenames: list) -> dict:
    backups = {}
    for fname in filenames:
        src = skill_dir / fname
        if src.exists():
            dst = Path(tempfile.gettempdir()) / f"_forgepub_{skill_dir.name}_{fname}"
            shutil.copy2(src, dst)
            src.unlink()
            backups[fname] = dst
    return backups


def restore_files(skill_dir: Path, backups: dict):
    for fname, backup_path in backups.items():
        dst = skill_dir / fname
        if backup_path == _GENERATED:
            dst.unlink(missing_ok=True)
        else:
            shutil.copy2(backup_path, dst)
            backup_path.unlink(missing_ok=True)


def get_skillhub_token() -> Optional[str]:
    try:
        creds = json.loads(SKILLHUB_CREDENTIALS.read_text(encoding="utf-8"))
        return creds.get("user", {}).get("token")
    except Exception:
        return None


# ============================================================
# 平台 CLI 定位
# ============================================================
def _find_skillhub_cli() -> Optional[Path]:
    p = shutil.which("skills_store_cli.py")
    if p:
        return Path(p)
    c = Path.home() / ".skillhub" / "skills_store_cli.py"
    return c if c.exists() else None


def _find_clawhub_cli() -> Optional[Path]:
    for cand in ("clawhub", "clawhub.cmd"):
        p = shutil.which(cand)
        if p:
            return Path(p)
    ws = Path.home() / ".workbuddy" / "binaries" / "node" / "workspace" / "node_modules" / ".bin" / "clawhub.cmd"
    if ws.exists():
        return ws
    base = Path.home() / ".workbuddy" / "binaries" / "node" / "versions"
    if base.exists():
        for d in sorted(base.iterdir(), reverse=True):
            c = d / "clawhub.cmd"
            if c.exists():
                return c
    return None


# ============================================================
# 平台发布函数
# ============================================================
def publish_skillhub(skill_dir: Path, slug: str, version: str,
                     changelog: str, dry_run: bool = False) -> bool:
    print(f"  [SkillHub] Publishing {skill_dir.name} v{version} ...")
    ensure_frontmatter(skill_dir, slug, "")
    backups: dict = {}
    backups.update(backup_and_remove(skill_dir, SKILLHUB_EXCLUDE_FILES))
    backups.update(generic_sanitize_config(skill_dir))
    try:
        cmd = [
            SKILLHUB_PYTHON, str(_find_skillhub_cli()), "publish", str(skill_dir),
            "--version", version, "--changelog", changelog,
            "--host", SKILLHUB_API_HOST,
        ]
        if dry_run:
            cmd.append("--dry-run")
        token = get_skillhub_token()
        if token:
            cmd.extend(["--token", token])
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                                timeout=120, env=env)
        if result.returncode == 0:
            out = (result.stdout or result.stderr).strip().lstrip("✓ ").lstrip("✗ ")
            print(f"    ✓ {out}")
            return True
        else:
            stderr = result.stderr.strip() or result.stdout.strip()
            if "已被 clawhub 来源占用" in stderr:
                print(f"    ✗ slug 被 ClawHub 第三方占用（非本账号，无法覆盖）：{stderr}")
                print(f"       → 请换一个不冲突的 slug（默认从 SKILL.md frontmatter 读取）")
                return False
            elif "频率过高" in stderr or "过于频繁" in stderr:
                print(f"    ⚠ 触发限流，请稍后重试")
                return False
            else:
                print(f"    ✗ {stderr}")
                return False
    finally:
        restore_files(skill_dir, backups)


def publish_clawhub(skill_dir: Path, slug: str, version: str,
                   changelog: str, dry_run: bool = False) -> bool:
    print(f"  [ClawHub] Publishing {slug} v{version} ...")
    ensure_frontmatter(skill_dir, slug, "")
    backups = generic_sanitize_config(skill_dir)
    try:
        cmd = [
            str(_find_clawhub_cli()), "skill", "publish", str(skill_dir),
            "--slug", slug, "--version", version, "--changelog", changelog,
        ]
        if dry_run:
            print(f"    (dry-run) 将执行: {' '.join(cmd)}")
            return True
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                                timeout=120, env=env)
        if result.returncode == 0:
            print(f"    ✓ {(result.stdout or result.stderr).strip()}")
            return True
        else:
            stderr = result.stderr.strip() or result.stdout.strip()
            if "已被" in stderr and "占用" in stderr:
                print(f"    ✗ slug 被占用：{stderr}")
                return False
            print(f"    ✗ {stderr}")
            return False
    finally:
        restore_files(skill_dir, backups)


# ============================================================
# 平台注册表（可扩展：github/gitee 接口预留）
# ============================================================
PLATFORMS = {
    "skillhub": {
        "status": "ready",
        "cli_resolver": _find_skillhub_cli,
        "publish": publish_skillhub,
        "setup_help": (
            "  SkillHub 首次准备:\n"
            "    1. 安装 SkillHub CLI（见 https://skillhub.cn 文档，或从 WorkBuddy 技能市场获取）\n"
            "    2. 登录后凭证自动写入 ~/.skillhub/credentials.json（含 user.token）\n"
            "    3. 验证: python ~/.skillhub/skills_store_cli.py --help"
        ),
    },
    "clawhub": {
        "status": "ready",
        "cli_resolver": _find_clawhub_cli,
        "publish": publish_clawhub,
        "setup_help": (
            "  ClawHub 首次准备:\n"
            "    1. 安装 ClawHub CLI: npm i -g clawhub  (或 WorkBuddy 内置)\n"
            "    2. 登录: clawhub login   （clawhub whoami 验证登录状态）\n"
            "    3. 注意 slug 全局唯一，发布前先确认未被他人占用"
        ),
    },
    "github": {
        "status": "planned",
        "setup_help": (
            "  GitHub 发布 (roadmap): 计划把技能仓库推送到 GitHub 并自动生成 Release。\n"
            "  接口已预留，敬请期待。当前可用 clawhub/skillhub 分发后，在 GitHub 镜像仓库。"
        ),
    },
    "gitee": {
        "status": "planned",
        "setup_help": (
            "  Gitee 发布 (roadmap): 计划把技能仓库推送到 Gitee 并自动生成 Release。\n"
            "  接口已预留，敬请期待。"
        ),
    },
}


# ============================================================
# 首次准备引导
# ============================================================
def preflight_platform(name: str) -> list:
    """返回某平台的准备告警；空列表=就绪"""
    info = PLATFORMS.get(name, {})
    if info.get("status") != "ready":
        return [f"平台 {name} 尚未支持（roadmap）"]
    warns = []
    cli = info["cli_resolver"]()
    if not cli or not cli.exists():
        warns.append(f"{name} CLI 未找到")
    else:
        if name == "skillhub" and not SKILLHUB_CREDENTIALS.exists():
            warns.append(f"SkillHub 凭证缺失: {SKILLHUB_CREDENTIALS}")
    return warns


def print_setup_help(name: str):
    info = PLATFORMS.get(name, {})
    help_text = info.get("setup_help", f"  {name} 准备引导未提供")
    print(f"\n--- {name} 首次准备引导 ---")
    print(help_text)
    print()


# ============================================================
# 本地校验（--check，不触网）
# ============================================================
def check_only(skill_dir: Path, slug_hint: str) -> int:
    print(f"\n{'='*60}")
    print(f"本地校验 (--check): {skill_dir}")
    print(f"{'='*60}")

    if not (skill_dir / "SKILL.md").exists():
        print(f"  ✗ 缺失 SKILL.md")
        return 1

    fm = _read_frontmatter(skill_dir / "SKILL.md")
    slug = fm.get("slug") or slug_hint
    display = fm.get("displayName") or "(无)"
    version = fm.get("version") or "(无)"

    print(f"  slug        : {slug}")
    print(f"  displayName : {display}")
    print(f"  version     : {version}")

    ok = True
    if not slug:
        print("  ✗ frontmatter 缺 slug（将无法通过 ClawHub --slug）")
        ok = False
    if version == "(无)" or not re.match(r"^\d+(\.\d+){0,2}$", str(version)):
        print("  ✗ frontmatter 缺合法 version")
        ok = False

    print(f"\n  双模态校验 (单版本双模态模型):")
    try:
        md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    except Exception:
        md = ""
    has_local = ("本地" in md) and ("记录" in md or "信号" in md)
    has_cloud = ("云端" in md) and ("上传" in md or "回传" in md)
    if has_local and has_cloud:
        print("    ✓ §零 含双模态说明（本地记录 + 云端上传）")
    elif has_local:
        print("    ℹ §零 仅本地记录（Tier 1 / 纯本地进化，无云端说明）")
    else:
        print("    ⚠ §零 未检出明确本地/云端信号说明")
    has_tier2 = ("🔄" in md) and ("⚙️" in md)
    if has_tier2:
        print("    ✓ footer Tier 2（⚙️ + 🔄 持续迭代）")
    else:
        print("    ℹ footer 未含 Tier 2 标记（⚙️+🔄），视为 Tier 1")
    if has_tier2:
        tok = skill_dir / CLOUD_CONFIG_FILE
        if not tok.exists():
            print("    ⚠ Tier 2 但 cloud_config.json 缺失 → 云端上传将降级失效（终端用户说『别传了』即纯本地）")
        else:
            try:
                cc = json.loads(tok.read_text(encoding="utf-8"))
            except Exception:
                cc = {}
            # 方案C 回归校验：零密钥包，cloud_config.json 不得含 token
            if "token" in cc:
                print("    ✗ cloud_config.json 含 token 字段（方案C 已禁止包内明文 token，包零密钥）")
                ok = False
            else:
                print("    ✓ cloud_config.json 存在且仅含公网 URL（零密钥，符合方案C）")

    src = skill_dir / "config.json"
    example = skill_dir / "config.example.json"
    print(f"  config.json : {'存在' if src.exists() else '缺失'}")
    if src.exists():
        try:
            data = json.loads(src.read_text(encoding="utf-8"))
            emails = [k for k in data if _is_email_field(k) and data.get(k) is not None]
            print(f"    将清空 email 字段: {emails if emails else '无'}")
        except Exception as e:
            print(f"    ⚠ config.json 解析失败: {e}")
    elif example.exists():
        print("    将从 config.example.json 临时生成净化版（发布后删除）")
    else:
        print("    无 config 文件，跳过净化")

    print(f"\n  CLI 可用性:")
    any_warn = False
    for name in ("skillhub", "clawhub"):
        for w in preflight_platform(name):
            print(f"    ⚠ [{name}] {w}")
            any_warn = True
    if not any_warn:
        print("    ✓ SkillHub / ClawHub CLI 均可用")

    print(f"\n{'='*60}")
    print(f"{'✅ 校验通过，可发布' if ok else '⚠️ 校验有缺失，请先补全 frontmatter'}")
    print(f"{'='*60}\n")
    return 0 if ok else 1


# ============================================================
# 主流程
# ============================================================
def resolve_skill_dir(args) -> Optional[Path]:
    if args.path:
        p = Path(args.path).expanduser().resolve()
        return p if p.exists() else None
    if args.skill:
        p = SKILLS_BASE / args.skill
        return p if p.exists() else None
    # 默认：当前工作目录（用户 cd 进自己锻造的技能目录后直接运行）
    cwd = Path.cwd()
    if (cwd / "SKILL.md").exists():
        return cwd
    return None


def main():
    parser = argparse.ArgumentParser(
        description="技能锻造炉自带发布器：一键发布到 SkillHub / ClawHub（GitHub/Gitee 规划中）")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--skill", help="技能 slug（从 ~/.workbuddy/skills/<slug> 读取）")
    g.add_argument("--path", help="技能目录绝对路径（默认：当前目录，需含 SKILL.md）")
    parser.add_argument("--platform", default="both",
                        choices=["skillhub", "clawhub", "both", "github", "gitee"],
                        help="目标平台 (default: both)")
    parser.add_argument("--changelog", default=None, help="发布 changelog（用户侧体验变化）")
    parser.add_argument("--version", default=None, help="覆盖版本号（默认读 frontmatter）")
    parser.add_argument("--dry-run", action="store_true", help="试运行，不真正上线")
    parser.add_argument("--check", action="store_true",
                        help="仅本地校验（不调用网络/CLI）")
    parser.add_argument("--slug", default=None, help="覆盖 slug（默认读 frontmatter）")
    # 方案C：--token 已移除，发布工具不再向包内注入任何 token（包零密钥）
    parser.add_argument("--ingest-url", default=None,
                        help="signal-ingest 公网地址（默认内置藏经阁固定地址）")
    parser.add_argument("--proposal-url", default=None,
                        help="cjg-proposal 公网地址（查看/审核进化提案；默认不写，旧包兼容）")
    parser.add_argument("--format", default="workbuddy", choices=SUPPORTED_FORMATS,
                        help="目标 agent 格式 (default: workbuddy; claude/codex 规划中)")
    args = parser.parse_args()

    skill_dir = resolve_skill_dir(args)
    if not skill_dir:
        target = args.path or (args.skill and (SKILLS_BASE / args.skill)) or Path.cwd()
        print(f"✗ 技能目录不存在或不含 SKILL.md: {target}")
        print("  用法: cd 进你的技能目录后运行  python forge-publish.py --check")
        sys.exit(1)

    slug = args.slug or read_field(skill_dir, "slug") or (args.skill or "")
    version = args.version or read_version(skill_dir)
    if not version and not args.check:
        print(f"✗ 无法解析版本号（frontmatter 无 version 且未用 --version 指定）")
        sys.exit(1)
    if version:
        version = to_semver(version)
    changelog = args.changelog or f"v{version}: 技能锻造炉自动化发布"

    if args.check:
        sys.exit(check_only(skill_dir, slug))

    # 方案C：cloud_config.json 由技能目录自带（仅 URL，无 token）；发布工具不注入任何凭据。

    # 解析目标平台列表
    if args.platform == "both":
        platforms = ["skillhub", "clawhub"]
    else:
        platforms = [args.platform]

    print(f"\n{'='*60}")
    print(f"技能锻造炉 · 自带发布器")
    print(f"  技能: {skill_dir.name}")
    print(f"  slug: {slug}")
    print(f"  平台: {', '.join(platforms)}")
    print(f"  模式: {'DRY-RUN' if args.dry_run else 'LIVE'}")
    print(f"{'='*60}\n")

    # 准备引导：对就绪平台做 preflight，缺失则打印引导并跳过
    ready_platforms = []
    for name in platforms:
        info = PLATFORMS.get(name, {})
        if info.get("status") != "ready":
            print(f"  ℹ 平台 {name} 规划中，本次跳过（接口已预留）")
            print_setup_help(name)
            continue
        warns = preflight_platform(name)
        if warns:
            print(f"  ⚠ [{name}] 准备未完成，跳过本次发布：")
            for w in warns:
                print(f"      - {w}")
            print_setup_help(name)
            continue
        ready_platforms.append(name)

    if not ready_platforms:
        print("⚠️ 无就绪平台，未执行发布。请按上方引导完成首次准备后重试。")
        sys.exit(1)

    results = {}
    for name in ready_platforms:
        ok = PLATFORMS[name]["publish"](skill_dir, slug, version, changelog, args.dry_run)
        results[name] = ok

    print(f"{'='*60}")
    success = sum(results.values())
    total = len(results)
    status = "✅" if success == total else "⚠️"
    print(f"{status} {success}/{total} 平台发布完成")
    if args.dry_run:
        print("  (dry-run 模式，未真正上线)")
    print(f"{'='*60}\n")
    sys.exit(0 if success == total else 1)


if __name__ == "__main__":
    main()
