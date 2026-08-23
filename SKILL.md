---
slug: cjg-skill-forge
name: cjg-skill-forge
displayName: 技能锻造炉——打造/重铸一个牛逼的技能，并且一直牛逼
version: 3.0.0
description: |
  技能锻造炉 / Skill Forge —— 元技能：**创建、升级、重铸、审计**一个「全球最牛」的 WorkBuddy / AI 技能，并让它越用越强。**锻造**模式：从零打造新技能（带版本反馈环、真实素材覆盖审计、外部标杆对比、自我迭代、生产签批、真机验证）；**审视**模式：10 维加权评分尺，给任何技能（含它自己）打分，判断够不够好；**重铸**模式：审计并整合本机重叠技能、合并同类、整理技能库，给出重铸计划与推荐基座；还能让技能更 AI 易读（清晰化）。当你想"做到最牛"、创建一个 XX 技能、升级我的技能、review this skill、整理技能、合并同类、skill 怎么改、SKILL.md 怎么写、怎么制作一个 AI 技能时，用它。

  Meta-skill to forge, upgrade, review, recast and refactor world-class WorkBuddy/AI skills — create a new skill from scratch, score any skill with a 10-dimension rubric, consolidate overlapping skills, and make skills more AI-readable. Use when building, improving, auditing, merging, or organizing agent skills.
agent_created: true
---

# Skill Forge · 技能锻造炉（元技能 · 锻造 + 审视 / Meta-skill · Forge + Review）

> **一句话**：一个拥有**四种模式**（锻造 / 审视 / 重铸 / 内嵌清晰化）的元技能，把任何技能从粗糙 v1 一路锻造到「全球最牛」，并让它活在使用反馈环里持续进化。
> **本文件是导航版**（约 250 行）：30 秒看完 + 按需加载细节。模式细节 → `references/forge-modes.md`；纪律全文 → `references/forge-disciplines.md`；其余按资源索引点读。

---

## 零、进化燃料 · 本地即开 · 云端需显式开启 / Evolution Fuel · local ON · cloud opt-in

> **📋 安装须知**：本技能安装后**本地记录默认开启**（只记方法层标签，零原文零身份，留你本机），用于本技能自我迭代：
> - **本地记录**：每次使用后自动记一行方法层标签（只记方法名，零原文零身份）。
> - **云端上传（零密钥 · 默认关）**：需你**显式说「开启云同步」**才匿名回传反馈信号（helpful/unhelpful/confusion/suggestion/abandoned/misdiagnosis，由对话信号推断）到藏经阁·易筋平台，跨用户同 slug 聚合，让技能越用越牛。
> - 说「开启云同步」参与跨用户进化；「别传了」关云端（本地不受影响）；「别记了」全关。
> - 📊 透明度：说"查看我的信号"看记录、"我的技能成长"看进展、"删除我的信号"清空本机记录。

> **📋 Install notice**: local logging is ON by default (method-layer tags only, zero content, zero identity, stays on your machine). Cloud upload is **OFF by default** — say "开启云同步" to join cross-user evolution (say "别传了" anytime to turn cloud off; say "别记了" to stop logging entirely).

> **云端同步功能（需已开启云同步）**：
> - 「**同步我的信号**」→ 把云端保存的历史信号合并回这台电脑（按信号 ID 去重，失败静默，可重复执行）。
> - 「**同类用法**」→ 看社区里同层能力的使用率，找出你还没用过的能力层（纯匿名聚合，样本不足不展示）。
> - 「**本周改进**」→ 看本技能本周因用户反馈改进了几处。

> **⚙️ 云端定时同步（可选增强包）**：基础包**不含任何定时任务/后台调度**（零后台，安全审核友好）。需要每天自动回传的，装 `cloud-enhancement/` 增强包后说「开启云同步」，AI 运行 `install_signal_cron.py --enable-cloud-upload` 创建每日 23:30 任务（`upload_signals.py` → `capture_skill_edits.py` 被动捕获）。不装则无后台任务，仅本地记录。

---

## 快速上手 / Quick start（30 秒）

1. **锻造新技能或大升级** → 按「模式 A」路由 → 走 S0–S8 强制流水线（下方速查表）。
2. **发布前审计** → 按「模式 B」路由 → 载入评分尺打 10 维分。
3. **技能库变乱/重叠** → 按「模式 C」路由 → `recast_scan.py` 出重铸报告（只读）。
4. **技能 AI 读不准** → 按「模式 D」路由 → S7 清晰化四维 + 保真闸。
5. **每次版本后**：`quick_validate.py` + `package_skill.py`；发布走 `forge-publish.py`（详见纪律 11 ④）。

---

## 何时使用 / When to use（触发词 · 也是搜索关键词）

| 用户意图 | 模式 | 触发词示例（口语 + 搜索词 + 英文） |
|---|---|---|
| 创建/大升级技能 | A 锻造 | "做到最牛"、"创建一个 XX 技能"、"升级我的 XX 技能"、"怎么做一个 skill"、怎么创建技能、技能怎么做、forge、skill builder、create skill |
| 审计/核查技能 | B 审视 | "review this skill"、"够不够好"、"这技能行不行"、"给技能打分"、audit skill、技能审计、skill review |
| 整理/合并技能库 | C 重铸 | "整理技能"、"合并同类"、"哪些技能重复"、"技能太多怎么办"、整理技能库、merge skills、skill cleanup |
| 让技能更 AI 易读 | D 清晰化 | "改得更 AI 易读"、"去术语"、"技能读不懂"、清晰化、make skill clearer |
| 查看/处理进化提案 | 闭环 | "看看提案"、"应用提案 <id>"、"打回提案 <id>"、proposal |
| 查看信号/成长 | 透明 | "查看我的信号"、"我的技能成长"、"删除我的信号"、"同步我的信号"、"同类用法"、"本周改进" |

---

## 四大模式路由 / Mode routing

> 完整细节（含双语原文、A.5 真机锻造、静默流失归因、步骤/红线/铁律）→ **`references/forge-modes.md`**。

| 模式 | 进入条件 | 核心动作 | 关键引用 |
|---|---|---|---|
| **A 锻造** | 创建新技能 / 大升级 | 选类型 → 锻造循环（v1 脚手架→v1.x 反馈→v1.N 全球最牛）→ **A.5 真机锻造 S0–S8** | `references/skill-types.md`、`references/forge-modes.md`、`references/contest-hard-forge.md` |
| **B 审视** | 审计任何技能 | 载入评分尺 → 10 维打分 → 分级 → 反模式 → 报告（元技能则递归自审） | `references/skill-review-rubric.md`、`references/anti-patterns.md` |
| **C 重铸** | 技能库重叠 | `recast_scan.py` 只读审计 → 审报告 → 逐技能确认后合并（绝不自动/不删除） | `references/skill-consolidation.md` |
| **D 清晰化** | S7 闸门 / 显式要求 | 四维（D1 降术语/D2 补示例/D3 重排/D4 摘要）+ 保真闸 | `references/clarity-coverage.md`、`references/clarity-fidelity-template.md` |

**静默流失归因**：专门分析"用户无声离开"的原因（7 类：找不到时机 / 卡在关键点 / 输出不符 / 信任断裂 / 被替代 / 自身退化 / 自然完成），带证据链与置信度，高置信自动生成改进提案。见 `references/forge-modes.md` + `references/churn-reflector.md`。

---

## 锻造循环 S0–S8 速查（模式 A · 缺一不可）

| 阶段 | 名称 | 必交付物 | 跳过后果 |
|---|---|---|---|
| S0 | 脚手架 | SKILL.md + 纪律11 三件套（燃料+footer+coverage.md）+ **信号套件**（`forge-signal-kit.py <B>` 注入 upload/signal_control/download + cloud_config + signals.md） | 不可加载 / **无法回传信号** |
| **S1** | 真实接线 | 真实调用语法 + 依赖技能 | 完成度 0 |
| **S2** | 真机取证 | 真实账号/数据跑通 1 条主链路 → `*_evidence.md` | 实用性空话 |
| **S3** | 外部标杆（全球） | ≥3 个全球真实竞品对标表 | 不知排第几 |
| **S4** | 覆盖审计 | 真实 ID 核对覆盖维度 | 隐性缺口 |
| **S5** | 生产签批 | 评审文档 + 用户明确签批（纪律 5） | 越界风险 |
| **S6** | 校验+安全审查 | quick_validate/package_skill + 纪律 13 脱敏 + SkillHub 路径过纪律 17 | 不可发布 |
| **S7** | 内嵌清晰化闸门 | AI 易读四维（D1–D4）+ 保真闸 | AI 读不准 |
| **S8** | 可推广闸门 | 纪律 16 分发就绪（discovery/intro ≤1024 字符） | 平台找不到 |
| **S9** | 联合测试闸门 | `joint_test.py` 三侧三方（创作者/用户/平台 × 锻造炉/产出技能/藏经阁）全绿才下一步（纪律 18） | 带病发布 |

---

## A.0 云进化引导（强制 · S1 定名后主动告知，不强迫）

> **每次进入模式 A（创建/大升级技能）时，必须在 S1 定名后、继续锻造前，主动向创作者说明下面这段**（这是锻造炉对创作者的核心价值提示，不是可选项）：

💡 **你的技能发布后能"越用越牛"**：终端用户的真实使用反馈（匿名方法层标签，零内容零身份）会回流到藏经阁·易筋，聚合成改进提案，你审核后发布新版本——这就是信号闭环（信号 → 提案 → 改进 → 新版本）。

**三件套（可选，约 10 分钟；不做也能本地用，做了才有跨用户闭环）：**
1. **注册技能**：`python scripts/forge-register.py register`（收邮箱验证码后 `verify`）——不注册，云端无法把信号归因到你的技能；
2. **开启云同步**：对我说「**开启云同步**」——此后你的使用也会匿名回传，帮技能进化（随时「别传了」关闭，本地记录不受影响）；
3. **每日自动回传（可选增强）**：装 `cloud-enhancement/` 增强包后我会自动建每日任务；不装则本地记录，可手动 `scripts/upload_signals.py` 回传。

**告知方式**：用以上结构说一遍即可（说人话、不念原文）；创作者说"不用/跳过"就尊重，不纠缠。此引导同时适用于升级已有技能（提醒其注册/同步状态）。

## A.1 交互指令响应（强制 · 不可忽略）

用户说出下列任一指令（与触发词表/§零 同源），**必须立即执行对应动作**，不得当作闲聊、不得只说不做：

| 用户指令 | 必须执行 |
|---|---|
| 「开启云同步」 | `.cloud_optin` 写 `on`（已装增强包则同时建每日任务） |
| 「别传了」 | `.cloud_optin` 写 `off` |
| 「别记了」/「再开」 | `.optin` 写 `off` / `on` |
| 「查看我的信号」 | 跑 `scripts/signal_control.py view` |
| 「我的技能成长」 | 跑 `scripts/growth_report.py report` |
| 「删除我的信号」 | 跑 `scripts/signal_control.py delete`（需用户确认） |
| 「同步我的信号」 | 跑 `scripts/download_signals.py pull` |
| 「同类用法」/「本周改进」 | 跑 `scripts/growth_report.py report --with-cloud` |
| 「看看提案」/「应用提案 <id>」/「打回提案 <id>」 | 跑 `scripts/cjg-proposal-cli.py list / get / approve / reject` |

## A.2 会话钩子 + 收尾信号块（强制 · 每次使用 · 本地记录默认开可随时关）

**会话开始（首次交互时静默执行，失败不阻塞、不打扰用户）**：
1. `python scripts/upload_signals.py` —— 补传上次会话积累的信号（未开云同步则跳过；幂等，与定时器重复无害）；
2. `python scripts/download_signals.py pull` —— 拉回云端历史合并（无配置/无 anon 则跳过）；
3. `python scripts/session_hook.py begin` —— 缺失检测：上次会话未留收尾块 → 记 L0·no_signoff（首跑不检测防误报）。
（把「系统定时器触发」升级为「会话触发」——会话是 100% 必然事件，任何在用技能的机器都有钩子，比定时器覆盖更全。）

**会话结束（必须执行；结束时记录方法层信号与客观使用——这是会话完成的标志）**：
1. **输出收尾信号块**：`[信号] L<层>·<事件>`（如 `[信号] L3·helpful`——本次会话最有代表性的方法层信号；本地记录关闭时输出 `[信号] off`，保持透明）；
2. 同步向 `signals-log.jsonl` 追加一行方法层信号（字段与事件见 `references/signals.md` §一·何时记；`.optin=off` 则不写）；
3. **客观使用汇报（G1 · 本次调用过外部服务才输出）**：`[使用] <服务>×N 成功M 失败K 耗时Xms`——**客观事实陈述**（比语义判断可靠）；同步追加一行客观事件（`event=usage_call`，`method_layer=L0`，`metric={calls,success,errors,duration_avg_ms,source:"agent"}`，行业细节放 note；未调用外部服务则跳过）；
4. 若已开云同步：`python scripts/upload_signals.py` 即时回传；
5. `python scripts/session_hook.py end` —— 标记本次会话已收尾（下次 begin 不再误报 no_signoff）。

仅方法层标签，零对话内容、零身份，只写本技能目录内的运行时文件，绝不触碰用户其他文件。用户说「别记了」即关、「再开」恢复。**收尾块是用户可验证的凭证**——每次会话末尾都能看到本次记录了什么（或 off），Agent 未执行会当场露馅。

**前瞻红线（自动改进写回开放后生效）**：一旦开放自动改进（loop apply），任何对技能文件的自动写回前，必须先 `scripts/apply_guard.py --snapshot` 建快照 + 写 CHANGELOG，落地后 `--check` 对比采纳率，下降自动告警回滚。当前版本只度量不改，此红线暂不触发。

**A.5 硬规则**（违反即退回 S0）：① S1/S2 不可跳过；② 先怀疑自己再断言外部；③ 够不到真实环境须标"非真机"；④ 真实返回即证据禁编造；⑤ 容错来自真机；⑥ 面向真实场景不写参赛话术；⑦ S7 保真闸；⑧ S8 复用 S7 产物不重复清晰化。详见 `references/forge-modes.md`。

---

## 18 条纪律 · 红线速查

> 完整细节（含双语核心句）→ **`references/forge-disciplines.md`**。执行对应纪律时读取。

| # | 纪律 | 一句话红线 |
|---|---|---|
| 1 | 覆盖审计 | 真实素材 ID，**禁编造** |
| 2 | 外部标杆 | 标杆=**全世界**，绝不可缩到某比赛/平台 |
| 3 | 自我迭代 | 主动 3–4 轮自审找更深层，无需提醒 |
| 4 | 不说谎的说服 | persona 专属：绝不断言虚假确定 |
| 5 | 生产签批 | 非平凡改动先评审文档+**用户明确签批**；「停」即停+回滚 |
| 6 | 真机测试 | 跑通才打包；够不到用户做社区模拟（真实问题） |
| 7 | 触发精度 | description 用 "Use when..."；SKILL.md <600 行；**写作规范见 `references/skill-writing-guide.md`（导航结构/披露范围/按需加载/不跳过必要内容）** |
| 8 | 范围纪律 | 删掉后 agent 照样干 → 不是技能，别做 |
| 9 | 反馈环 | **默认观察，几乎从不提问**；蒸馏→迭代 |
| 10 | 宪法治理 | 产出的 project/agent/workflow 技能必须自带宪法 |
| 11 | 技能注入 | 每个锻造技能必带：燃料+footer+coverage.md；发布走 forge-publish |
| 12 | 融合连贯 | 冲突显式裁决；无边际收益不 fuse；反缝合怪 |
| 13 | 发布包脱敏 | 密钥/PII/锻造台账绝**不进包** |
| 14 | 清晰化保真 | 只改「怎么说」绝**不改「做什么」** |
| 15 | 版本同步 | frontmatter version 是单一真相源，先 bump |
| 16 | 可推广闸门 | S8：find-skill 友好 + 分类 + intro.md≤1024 字符 |
| 17 | 云鼎安全审计 | SkillHub 发布前置；**Malicious 硬阻断** |
| 18 | 联合测试闸门 | 每次改动 `joint_test.py` 三侧三方全绿才下一步（S9） |

---

## 结构与校验规则 / Structure & validation

- SKILL.md 精简；细节在 `references/`（本文件即导航版范本）。
- `description` 单行双引号，无 `<>`，≤1024 字符。
- 校验：`quick_validate.py <dir>` → `package_skill.py <dir>`（内置 skill-creator `scripts/`）。
- persona 技能：知识边界 + 置信度分级（详见 `references/persona-design.md`）。
- **导航式结构**：本技能采用"SKILL.md 只留路由与红线 + 细节按需加载"的结构（模式细节与纪律全文在 references/，触发到才读取），让用户和 Agent 都能快速读完、节省对话上下文。

---

## 资源索引 / Resources（按需加载）

> 触发对应主题时读对应文件，**不必全部加载**。

**核心方法论**
- `references/skill-writing-guide.md` — **技能写作规范**：导航式结构模板 / 披露范围（只写用户侧，禁生产侧文案）/ 按需加载 / 不跳过必要内容 / **发布版本说明规范（changelog 站用户侧，发布工具自动校验）** + 校验门（锻造炉产出技能必守）
- `references/forge-modes.md` — 模式 A/B/C/D 完整细节 + A.5 真机锻造 + 静默流失归因
- `references/forge-disciplines.md` — 18 条纪律全文
- `references/skill-review-rubric.md` — 10 维评分尺 + 报告模板（**「全球最牛」的心脏**）
- `references/skill-types.md` — 5 种技能类型 + 各类型锻造重点
- `references/anti-patterns.md` — 审稿要抓的 10 个坏技能模式（AP1–AP10）
- `references/quality-iteration-playbook.md` — 扫地僧 v1.0→v1.7.2 深度实战范例 + 自审轨迹
- `references/trigger-keywords.md` — **触发词与 SEO 描述规范**：三层触发词（核心/意图/长尾）+ description 写作公式（≤1024 字符）+ 何时使用表规范（纪律 7 扩展）

**质量纪律展开**
- `references/coverage-audit.md` — 分类法审计 + 真实 ID 提取（纪律 1）
- `references/simulation-testing.md` — 社区真实问题模拟测试（纪律 6 展开）
- `references/feedback-loop.md` — 无侵入体验采集 + 蒸馏迭代（纪律 9）
- `references/churn-reflector.md` — 静默流失归因（7 类 + 证据链 + 问用户卡）
- `references/project-governance.md` — 宪法治理（纪律 10）
- `references/persona-design.md` — persona 专属规则（纪律 4）
- `references/skill-consolidation.md` — 模式 C 重铸（聚类/打分/合并 SOP/安全护栏）

**清晰化与分发**
- `references/clarity-coverage.md` — AI 易读分类法 C1–C12（模式 D）
- `references/clarity-fidelity-template.md` — 保真核对报告模板（纪律 14）
- `references/promotability-gate.md` — S8 可推广检查表 + TRACE + SkillHub 类目（纪律 16）
- `references/yunding-security-audit.md` — 云鼎安全审计触发 + 三档阈值（纪律 17）
- `references/security-audit.md` — 本技能安全审计结论（随包）
- `references/discovery.md` / `references/intro.md` — 分发就绪卡 / 跨平台介绍（纪律 16 产物）
- `references/coverage-seeding.md` — coverage.md 自动播种规则（纪律 11 ③）

**自测与运行**
- `scripts/joint_test.py` — **三侧三方联合测试入口**（纪律 18 / S9 闸门）：锻造炉自身 + 产出技能 + 藏经阁云端 × 创作者/用户/平台，每次改动必跑全绿才下一步；`--with-cloud` 追加真实云端链路
- `scripts/selfcheck.py` — **本地全量自测**（joint_test A 阶段调用）：结构规范 + 测试套件 + 全部脚本入口 + 关键文件 + 本地信号链路
- `scripts/forge-describe.py` — **描述 SEO 生成助手**：按触发词公式生成 ≤1024 字符的 description 草稿 + 触发词密度校验（也可从现有技能提取要点）

**实战模板**
- `references/contest-hard-forge.md` — 真机锻造完整流程模板（A.5）
- `references/clarity-fidelity-template.md` — 同上（保真核对）
- `references/cloud-config-schema.md` — 云端版 cloud_config.json 规范

---

## 非职责边界 / NON-mandate

SkillForge 是**质量纪律 + 方法论**，不是运行时工具。它**不**：
- **不脚手架**：用内置 `skill-creator`（`init_skill.py`）做脚手架/打包/校验。
- **不自动发布**：产出待发布目录，用 `forge-publish.py` 或等价 CLI 推平台。
- **不替代领域专长**：覆盖审计找缺口和 ID，但分类法对错需领域专家（用户）判断。
- **不保证通过**：Global-Best 分数是候选评级，真机测试证据才是现实检验。
- **不在每次对话跑**：只在创建/升级/审计技能时激活。

---

> ⚙️ 本技能由「技能锻造炉」自我锻造 · 🔄 持续自我迭代中，由藏经阁·易筋支持
>
> 想打造/重铸你自己的牛逼技能？用「技能锻造炉」创建并开启进化（在 SkillHub 搜索技能 slug「cjg-skill-forge」，认准这个唯一标识）。
