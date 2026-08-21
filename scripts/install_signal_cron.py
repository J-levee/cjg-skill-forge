#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""藏经阁·易筋 信号上传定时任务安装器（闭合断点 B）。

幂等地把「每日 23:30 跑 upload_signals.py」挂到本机调度器：
  - Windows   -> Task Scheduler（schtasks），任务名 CJG-SkillForge-SignalUpload
  - macOS/Linux -> crontab（标记 # cjg-signal-upload）

设计要点：
  - 幂等：已存在同名任务则跳过（除非 --force 重建）。
  - 不读对话、不碰文件、不收集隐私；只调度 upload_signals.py（该脚本本身零密钥、断点续传）。
  - upload_signals.py 默认扫描整个技能基目录（~/.workbuddy/skills），无需 --all 参数。

用法：
  python install_signal_cron.py                              # 不安装（默认零后台，仅本地记录）
  python install_signal_cron.py --enable-cloud-upload       # 仅用户"开启云同步"后由 AI 调用，挂每日 23:30 上传任务
  python install_signal_cron.py --force                     # 重建（需配合 --enable-cloud-upload）
  python install_signal_cron.py --uninstall                 # 卸载后台任务
"""
import os
import sys
import subprocess

TASK_NAME = "CJG-SkillForge-SignalUpload"
CRON_MARK = "# cjg-signal-upload"
HERE = os.path.dirname(os.path.abspath(__file__))
UPLOAD = os.path.join(HERE, "upload_signals.py")
PY = sys.executable


def _is_win():
    return sys.platform.startswith("win")


def _run(cmd, check=True):
    # Windows schtasks 输出为本地编码（GBK/cp936），用 oem+replace 避免解码异常
    enc = {"encoding": "oem", "errors": "replace"} if _is_win() else {}
    return subprocess.run(cmd, shell=_is_win(), capture_output=True, text=True, **enc)


# ---------- Windows (Task Scheduler) ----------

def _win_exists():
    r = _run(["schtasks", "/Query", "/TN", TASK_NAME], check=False)
    return r.returncode == 0


def _win_install(force):
    if _win_exists():
        if force:
            _run(["schtasks", "/Delete", "/TN", TASK_NAME, "/F"], check=False)
        else:
            print(f"[ok] 任务已存在，跳过：{TASK_NAME}（用 --force 重建）")
            return True
    tr = f'"{PY}" "{UPLOAD}"'
    r = _run(["schtasks", "/Create", "/TN", TASK_NAME, "/SC", "DAILY",
              "/ST", "23:30", "/TR", tr, "/F"], check=False)
    if r.returncode != 0:
        print(f"[err] schtasks 创建失败：{r.stderr.strip() or r.stdout.strip()}")
        return False
    print(f"[ok] 已创建 Windows 计划任务 {TASK_NAME}：每日 23:30 跑 upload_signals.py")
    return True


def _win_uninstall():
    if not _win_exists():
        print(f"[ok] 任务不存在，无需卸载：{TASK_NAME}")
        return
    r = _run(["schtasks", "/Delete", "/TN", TASK_NAME, "/F"], check=False)
    print(f"[ok] 已卸载任务 {TASK_NAME}" if r.returncode == 0 else f"[err] 卸载失败：{r.stderr.strip()}")


# ---------- macOS / Linux (crontab) ----------

def _cron_line():
    return f'30 23 * * * "{PY}" "{UPLOAD}" {CRON_MARK}'


def _cron_install(force):
    cur = _run(["crontab", "-l"], check=False).stdout
    if CRON_MARK in cur:
        if force:
            cur = "\n".join(l for l in cur.splitlines() if CRON_MARK not in l) + "\n"
        else:
            print(f"[ok] crontab 已存在标记 {CRON_MARK}，跳过（用 --force 重建）")
            return True
    new = (cur.rstrip() + "\n" if cur.strip() else "") + _cron_line() + "\n"
    r = _run(["crontab", "-"], input_text=new) if False else _pipe_crontab(new)
    if r.returncode != 0:
        print(f"[err] crontab 写入失败：{r.stderr.strip()}")
        return False
    print(f"[ok] 已写入 crontab：{_cron_line()}")
    return True


def _pipe_crontab(new):
    p = subprocess.run(["crontab", "-"], input=new, capture_output=True, text=True)
    return p


def _cron_uninstall():
    cur = _run(["crontab", "-l"], check=False).stdout
    if CRON_MARK not in cur:
        print(f"[ok] crontab 无标记 {CRON_MARK}，无需卸载")
        return
    new = "\n".join(l for l in cur.splitlines() if CRON_MARK not in l) + "\n"
    r = _pipe_crontab(new)
    print(f"[ok] 已从 crontab 移除 {CRON_MARK}" if r.returncode == 0 else f"[err] 移除失败：{r.stderr.strip()}")


# ---------- 入口 ----------

def main():
    if not os.path.exists(UPLOAD):
        print(f"[err] 找不到上传脚本：{UPLOAD}")
        sys.exit(1)
    force = "--force" in sys.argv
    uninstall = "--uninstall" in sys.argv
    enable_cloud = "--enable-cloud-upload" in sys.argv
    if uninstall:
        _win_uninstall() if _is_win() else _cron_uninstall()
        return
    if not enable_cloud:
        # 默认零后台：不挂任何定时任务，避免静默改动用户系统。
        print("[info] 未指定 --enable-cloud-upload：默认不安装后台定时任务（保持零后台、本地仅记录）。")
        print('[info] 仅当你显式说"开启云同步"后，AI 才会运行：python install_signal_cron.py --enable-cloud-upload')
        sys.exit(0)
    ok = _win_install(force) if _is_win() else _cron_install(force)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
