#!/usr/bin/env python3
"""三侧三方联合测试（joint_test.py）—— 每次改动必跑，全绿才进入下一步（纪律 18 联合测试闸门）。

三个被测对象 × 三个视角：
  对象：① 锻造炉技能（skill-forge 自身） ② 锻造炉产出的技能（临时样例） ③ 藏经阁云端
  视角：创作者侧（发布全流程）/ 用户侧（安装使用+隐私）/ 平台侧（合规验收）
每个用例标注视角：`[创作者] [用户] [平台]`。

阶段：
  A 锻造炉自身：selfcheck 本地全量（结构/套件/入口/文件/本地信号链路）+ 发布前校验
  B 产出技能验收：临时样例技能全流程——写作门/发布 check/描述 SEO/信号链路/zip 合规
  C 藏经阁云端：8 SCF health + 公网端点 + 真实链路（--with-cloud 需凭据，调 run_skill_forge_cloud.py）

用法：
  python joint_test.py              # A + B + C(本地探测，无凭据)
  python joint_test.py --with-cloud # A + B + C(含真实云端链路，需 SCF 凭据)
  python joint_test.py --verbose
退出码：0=全绿；2=有失败（禁止下一步）
"""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
PY = sys.executable
VERBOSE = "--verbose" in sys.argv
WITH_CLOUD = "--with-cloud" in sys.argv

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append(cond)
    mark = "✅" if cond else "❌"
    print(f"  {mark} {name}" + (f"  — {detail}" if detail and not cond else ""))
    return cond


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def section(t):
    print(f"\n== {t} ==", flush=True)


# ---------- 阶段 A：锻造炉自身 ----------
def stage_a_self():
    section("A 锻造炉自身 · [创作者][用户][平台] 本地全量")
    r = run([PY, os.path.join(HERE, "selfcheck.py")])
    check("[用户] selfcheck 本地全量（33 项：结构/套件/入口/文件/信号链路）",
          r.returncode == 0, r.stdout[-300:] if not VERBOSE else r.stdout)
    r2 = run([PY, os.path.join(HERE, "forge-publish.py"), "--path", SKILL_DIR, "--check"])
    check("[平台] forge-publish --check 发布前校验（含 SEO）",
          r2.returncode == 0 and "校验通过" in r2.stdout, r2.stdout[-200:])


# ---------- 阶段 B：产出技能验收 ----------
MINI_SKILL = """---
slug: joint-sample
name: joint-sample
displayName: 联合测试样例技能
version: 9.9.9
description: |
  联合测试样例技能 —— 用于验证锻造炉产出技能的三侧三方联合测试。可以创建、升级、审计一个示例技能，并整理、合并、review 技能文件。Use when testing a sample skill.
agent_created: true
---

# Joint Sample

## 零、进化燃料

本技能会记录方法层信号（本地记录，默认开启；**每次会话结束输出收尾信号块并记录一条方法层标签**，若本次调用了外部服务则追加一条**客观使用汇报**（`[使用] 服务×N 成功M 失败K`，字段见 `references/signals.md` §二·七）；会话开始自动补传与拉回；字段与事件规范见 `references/signals.md`）；云端上传默认关闭，说"开启云同步"才开启；说"别传了"关闭；说"删除我的信号"清空。

## 何时使用 / When to use（触发词）

| 用户意图 | 模式 | 触发词示例 |
|---|---|---|
| 测试样例 | 样例 | "创建样例"、"升级样例"、sample、test |
| 审计 | 审视 | "review"、审计 |

## 红线

- 绝不写入用户文件（只读红线）。

## 结构与校验

- 发布校验：forge-publish.py --check；写作规范门：writing_gate.py（10 项）。
- 覆盖维度（能力说明书）见 `references/coverage.md`；进化信号规范见 `references/signals.md`。

⚙️ 由技能锻造炉锻造 · 🔄 持续迭代
"""


def _write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def stage_b_produced():
    section("B 产出技能验收 · [创作者] 锻造炉产出的技能全流程")
    tmp = tempfile.mkdtemp(prefix="joint-prod-")
    try:
        skill = os.path.join(tmp, "joint-sample")
        os.makedirs(os.path.join(skill, "references"))
        _write(os.path.join(skill, "SKILL.md"), MINI_SKILL)
        # 覆盖说明书（W7 需加载声明）；signals.md/cloud_config/脚本由信号套件注入
        _write(os.path.join(skill, "references", "coverage.md"),
               "# 覆盖维度\n> 触发到覆盖审计时加载。\n\n- **能力**: 样例\n- **类型**: 测试\n")

        # B0 [创作者] 信号套件注入（闭环断点防线：产出技能必须有回传能力）
        r = run([PY, os.path.join(HERE, "forge-signal-kit.py"), "inject", skill])
        check("[创作者] 信号套件注入（upload/control/download + cloud_config + signals.md）",
              r.returncode == 0, r.stdout[-200:])

        # B1 [创作者] 写作规范门：产出技能必须通过 W1–W8+W3a/W3b+W10
        r = run([PY, os.path.join(HERE, "writing_gate.py"), skill])
        check("[创作者] 产出技能过写作规范门（W1–W8+W3a/W3b+W10 信号套件）",
              r.returncode == 0, r.stdout[-300:])

        # B2 [平台] 发布前校验（forge-publish --check，含 SEO 描述长度）
        r = run([PY, os.path.join(HERE, "forge-publish.py"), "--path", skill, "--check"])
        check("[平台] 产出技能 forge-publish --check 通过", r.returncode == 0, r.stdout[-250:])

        # B3 [平台] 描述 ≤1024（zip 安装兼容）+ 触发词命中
        desc = re.search(r"^description:.*?\n((?:  .*\n?)+)", open(os.path.join(skill, "SKILL.md"), encoding="utf-8").read(), re.M)
        dlen = len(re.sub(r"^  ", "", desc.group(1), flags=re.M).strip()) if desc else 0
        check("[平台] 产出技能 description ≤1024 字符", dlen <= 1024, f"当前 {dlen}")

        # B5 [平台] 发布包合规：干净目录检查（在造信号产物之前——净化视角）
        exclude = {".optin", ".anon_id", ".cloud_optin", ".cloud_token", ".skill_edit_baseline.json",
                   ".capture.lock", ".uploaded_ids.txt", "signals-log.jsonl", ".apply-snapshots"}
        tops = {f for f in os.listdir(skill)}
        leaked = tops & exclude
        check("[平台] 产出技能发布包无运行时产物泄露", not leaked, f"泄露 {leaked}")

        # B4 [用户] 信号链路：用 B 自己的套件（闭环核心——B 能独立回传）
        sig = {"ts": "2026-08-22T10:00:00", "signal_id": "js-001", "client_signal_id": "js-001",
               "skill_slug": "joint-sample", "skill_version": "9.9.9", "method_layer": "L3",
               "event": "helpful", "weight": 1, "note": "joint", "anon_id": "joint-anon"}
        _write(os.path.join(skill, "signals-log.jsonl"),
               json.dumps(sig, ensure_ascii=False) + "\n")
        _write(os.path.join(skill, ".cloud_optin"), "on")
        r = run([PY, os.path.join(skill, "scripts", "upload_signals.py"), "--base", tmp, "--dry-run"])
        check("[用户] B 自己的 upload 脚本 dry-run 统计待传（on）",
              r.returncode == 0 and "本应上传 1 条" in r.stdout, r.stdout[-180:])
        r = run([PY, os.path.join(skill, "scripts", "signal_control.py"), "status", "--dir", skill])
        check("[用户] B 自己的 signal_control status", r.returncode == 0 and "Traceback" not in r.stderr)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


# ---------- 阶段 C：藏经阁云端 ----------
def stage_c_cloud():
    section("C 藏经阁云端 · [创作者][用户][平台]")
    cc_path = os.path.join(SKILL_DIR, "cloud_config.json")
    if os.path.exists(cc_path):
        try:
            cc = json.load(open(cc_path, encoding="utf-8"))
        except Exception:
            cc = {}
        need = {"ingest_url", "register_url", "proposal_url", "aggregate_url"}
        missing = need - set(cc)
        check("[用户] cloud_config.json 含 4 个端点", not missing, f"缺 {missing}")
        for name, key in (("ingest", "ingest_url"), ("register", "register_url"),
                          ("proposal", "proposal_url"), ("aggregate", "aggregate_url")):
            if key in cc:
                check(f"[用户] 端点配置 {name}", bool(cc[key].startswith("https://")), cc[key])
    if WITH_CLOUD:
        import time as _time
        # 云端链路脚本路径：环境变量优先，其次按常见开发目录相对推导（不硬编码用户名/机器路径）
        alt = (os.environ.get("CJG_CLOUD_TEST_SCRIPT") or
               os.path.join(os.path.expanduser("~"), "WorkBuddy", "2026-07-10-22-37-49",
                            "cjg-evo", "backend", "local_test", "run_skill_forge_cloud.py"))
        r = run([PY, "-u", alt]) if os.path.exists(alt) else None
        # 云端链路偶发限流/网络抖动：失败自动重试一次（真故障会持续失败）
        if r is not None and r.returncode != 0:
            print("  ℹ 云端链路首轮失败（可能限流/网络抖动），5 秒后重试一次…", flush=True)
            _time.sleep(5)
            r = run([PY, "-u", alt])
        if r is not None:
            check("[创作者][用户][平台] 云端真实链路（8 SCF health + 上传/拉回/幂等/零残留）",
                  r.returncode == 0, r.stdout[-400:] if not VERBOSE else r.stdout)
        else:
            check("[创作者] 云端真实链路脚本缺失", False, "未找到 run_skill_forge_cloud.py")
    else:
        print("  ℹ 未加 --with-cloud：云端真实链路跳过（本地配置探测已覆盖）；加 --with-cloud 需 SCF 凭据")


def main():
    if len(sys.argv) >= 2 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    print(f"三侧三方联合测试（joint_test.py · {SKILL_DIR}）")
    print("视角：创作者=发布全流程 用户=安装使用+隐私 平台=合规验收")
    safe(stage_a_self)
    safe(stage_b_produced)
    safe(stage_c_cloud)
    passed = sum(1 for r in RESULTS if r)
    print(f"\nJoint Test: {passed}/{len(RESULTS)} 通过"
          + (" —— ✅ 全绿，可进入下一步" if passed == len(RESULTS) else " —— ❌ 有失败，禁止下一步"))
    sys.exit(0 if passed == len(RESULTS) else 2)


def safe(fn):
    try:
        fn()
    except Exception as e:
        import traceback
        RESULTS.append(False)
        print(f"  ❌ 段内异常 {fn.__name__}: {e}", flush=True)
        if VERBOSE:
            traceback.print_exc()


if __name__ == "__main__":
    main()
