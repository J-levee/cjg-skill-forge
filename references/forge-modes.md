# 锻造炉 · 模式细节（MODE DETAILS）——按需加载

> SKILL.md 只留路由，本文件是模式 A/B/C/D 与关④ 的完整细节（含中英双语原文）。
> 触发到对应模式时读取本文件相应章节，其余不必加载。

---

## 模式 A — 锻造（FORGE）/ MODE A

### 先选技能类型 / Pick the skill type first

见 `references/skill-types.md`：utility / workflow / coding / persona / agent。各纪律因类型而异（如 workflow 与 agent 技能**强制**生产签批；persona 技能需要 voice 层）。

See `references/skill-types.md`: utility / workflow / coding / persona / agent. The disciplines apply differently per type (e.g., workflow & agent skills MANDATE production sign-off; persona skills need a voice layer).

### 锻造循环（带版本）/ The Forging Loop (versioned)

每个版本 = **一条**具体用户指令 + **一处**外部锚定的改进。绝不为模糊的想象迭代。

Each version = ONE concrete user instruction + ONE externally-anchored improvement. Never iterate on vague imagination.

- **v1.0 脚手架**：`skill-creator` 的 `init_skill.py` → 精简 SKILL.md + 最少 references。
- **v1.x 反馈轮**：每条真实反馈，做**一处**针对性改动（用户画像、标志性 voice、根因方法、更广覆盖、经典引用、说服技巧）。
- **v1.N → "全球最牛"**：主动（无需提醒）做外部标杆 + 3–4 轮自审，再落一个大的架构版本。

每个版本之后：`quick_validate.py` + `package_skill.py`。让文件夹始终可被加载。

### 子模式 A.5 — 真机锻造（Real-Machine Forge）

> **定位**：把「真实验证」从可选纪律升为**强制阶段**——锻造炉产出「能跑、能赢」技能的关键补丁。一个真实场景（如 SkillHub × 腾讯会议大赛）只是**验证场（test vehicle）**，锻造目标永远是**全球最牛（Global-Best）**，不是比赛第一。

#### 6 阶段强制流水线（缺一不可）

| 阶段 | 名称 | 必交付物 | 跳过后果 |
|------|------|----------|----------|
| S0 | 脚手架 | SKILL.md + 纪律11三件套（进化燃料+footer+coverage.md）+ **信号套件**（运行 `scripts/forge-signal-kit.py <B目录>` 注入 upload_signals/signal_control/download_signals + cloud_config.json + signals.md） | 不可加载 / **信号无法回传（闭环断）** |
| **S1** | **真实接线** | 写清真实调用语法 + 装好依赖技能 | 完成度 0 分 |
| **S2** | **真机取证** | 用真实账号/真实数据跑通 1 条主链路，真实返回写入 `references/*_evidence.md` | 实用性 空话 |
| **S3** | **外部标杆（全球）** | 按技能类型选标杆，均 ≥3 处、须全网（不得仅限局部场景）：① **竞品类技能**对标 ≥3 个**全球真实竞品**；② **方法论/通用类技能**对标**行业标准方法与权威框架**（官方规范/顶会综述/业界基线）；③ **工具型技能**对标 ≥3 个**同类工具/标准**（同类开源/商业工具、对应标准规范、官方文档基线） | 不知排第几 |
| **S4** | **覆盖审计** | 用真实 ID 核对覆盖维度，无盲区 | 隐性缺口 |
| **S5** | **生产签批（按风险分档）** | 高风险（workflow/agent/coding：触碰生产系统/写文件/动数据）→ 执行评审文档 + 用户明确签批（纪律 5）；低风险（utility 只读/纯转换、persona 纯咨询）→ 发布前一句确认即可 | 越界风险 |
| **S6** | **校验打包 + 安全审查** | quick_validate + package_skill 通过 + 纪律 13 脱敏 + 走 SkillHub 前过纪律 17 云鼎审计 | 不可发布 |
| **S7** | **内嵌清晰化闸门** | 对 SKILL.md 跑 AI 易读四维（D1–D4）+ 保真闸（`references/clarity-fidelity-template.md`）+ **写作规范门（`references/skill-writing-guide.md`：导航结构/披露范围/按需加载/必要内容内联）** | 发布后 AI 读不准 |
| **S8** | **可推广闸门** | 纪律 16 分发就绪校验：discovery.md + needs_api_key + intro.md（≤1024 字符）+ find-skill 触发友好；**以 S7 清晰化产物为 Convention 证据，不重复清晰化** | 平台找不到 |

#### 硬规则（违反即退回 S0）
1. **S1/S2 不可跳过**：未真机跑通，禁止声称"可运行/能赢"。
1b. **先怀疑自己，再断言外部**（诚实归因）：接口异常（空/0 条/401/500/超时）时**先核查自己的调用格式**再下结论"外部挂了"。
1c. **够不到真实环境时，诚实标注"非真机"**：用模拟/替代闭环必须在文档显式标注"未真机验证/模拟闭环"。
2. **真实返回即证据**：`*_evidence.md` 必须含真实字段/数据，**禁编造**（纪律 1）。
3. **容错来自真机**：真跑发现的坑必须写回 SKILL.md 容错段落。
4. **面向真实场景，不写参赛话术**：description/展示名面向真实使用，不写"参赛/大赛加分"等话术。
5. **S7 内嵌清晰化闸门**：S6 后、发布前对 SKILL.md 跑四维 + 保真闸；任一 ❌ 或 ⚠️ 涉及功能 → 回退 S2/S3。
6. **S8 可推广闸门**：S7 后、发布前跑纪律 16；S8 复用 S7 清晰化产物为 Convention 证据，不重复清晰化。
7. **S9 全量自测闸门（纪律 18）**：S8 后、发布前跑 `scripts/selfcheck.py` 本地全量（结构/套件/入口/文件/链路）；开发侧另跑云端链路 `run_skill_forge_cloud.py`。任一 ❌ → 退回修复，不发布。

#### ☁️ 云进化前置：注册 slug（创建期强制引导 · 对应 SKILL.md A.0）

**S1 定名后必须主动向创作者说明云进化闭环**（SKILL.md A.0 为权威文案，此处为执行步骤）：
1. **告知价值**：发布后终端用户匿名反馈 → 藏经阁聚合 → 改进提案 → 创作者审核发布 → 新版本，技能越用越牛。
2. **三件套引导**（不强迫，跳过即尊重）：
   - 注册：`python scripts/forge-register.py register` → 邮箱收验证码 → `verify <验证码>`（token 存 `<技能目录>/.deploy/cloud_open.json`，**不进发布包**）；
   - 开启云同步：让创作者说「开启云同步」（本机信号开始匿名回传）；
   - 每日自动回传（可选）：装 `cloud-enhancement/` 后建每日任务；不装则本地记录 + 手动 `upload_signals.py`。
3. **检查注册态**：`python scripts/forge-register.py status` 可查当前 slug 是否已验证——升级已有技能时先查再提醒。
4. **发布前提示**：S8 发布时若 slug 未注册/未开云同步，提醒"该技能将无跨用户闭环"（不阻断发布，仅透明告知）。

#### 真实范例
`novelty-validator` v1.1.0 按本子模式锻造（S1 接线 / S2 真机 / S3 全球标杆 / S4 覆盖 C1–C12 全 ✅）。完整流程模板见 `references/contest-hard-forge.md`。

#### 回流
每完成一个技能，把新发现的"真实接口坑/竞品情报/评分维度"写回 `references/contest-hard-forge.md`。

---

## 关④ · 静默流失根因归因（churn_reflector）【CJG-EVO 叠加模块】

> 与 Discipline 9 同源但**专门处理"用户无声离开"这半环**（增长飞轮出口闭合）。
> 详细规则、7 类归因、置信度打分、证据链格式、问用户卡片见 `references/churn-reflector.md`。

- **定位**：关③（进迭代循环）的**对称补半环**——收集"下车"的负向/沉默信号，汇入同一 `signal → distill → proposal → 用户审 → 重发布` 闭环。
- **opt-in 默认：开启**（只处理 method-layer 元数据、零 PII；首次启动一句透明说明，可一键关）。
- **机制**：冷却期到 + 历史达标 → 7 类归因（E / C1 找不到时机 / C2 卡点 / C3 输出不符 / C4 信任断裂 / C5 被替代 / C6 自身回归）→ 带证据链 + 置信度 → ≥0.6 自动进提案；<0.6 转"问用户"卡片。
- **铁律**：叠加能力，**不改动锻造内核、不 bump 版本、不改 changelog**。
- **M0**：单技能闭环；**M1+**：用户打回反哺分类器、跨技能同因改 Forge 模板。

---

## 模式 B — 审视（REVIEW）/ MODE B

### 何时进入 / When to enter
用户说 "review this skill"、"够不够好"、"audit <skill>"，或核查某技能（含 skill-forge）是否 Global-Best。

### 步骤 / Steps
1. 载入 `references/skill-review-rubric.md`。
2. 对照证据给全部 10 维打 0–5 分（读 SKILL.md + references；**不要凭感觉**）。
3. 加权总分分级：<50 Thin · 50–69 Solid · 70–84 Excellent · 85–100 Global-Best 候选。
4. **Global-Best 闸门**：≥85 仅在同时具备 (a) **全网扫描**所得外部标杆（非某比赛/平台）与 (b) 通过的真机测试时才有效；否则封顶 84。
5. 查 `references/anti-patterns.md`（AP1–AP10）——每命中一条是 P0/P1 修复。
6. 产出审稿报告（模板在评分尺里）。
7. **递归自审**：被审技能是 skill-forge 时，套同一把尺并发布 `skill-forge-self-audit.md`。

### 审稿红线 / Red lines
- 绝不为讨好作者虚抬分数。诚实的 68 好过一个说谎的 90。
- 在 D5（编造证据）上失败的技能，分数不能超过 69。
- 保留作者差异化；审稿为了改进，不是同质化。

---

## 模式 C — 重铸（RECAST）/ MODE C

> 本机同类技能互相重叠时，用 Mode C 审计并整合。**默认只出报告，不合并。** 合并是可选的、逐技能确认的高权限操作。

### 何时进入 / When to enter
用户说"整理技能"、"合并同类"、"哪些技能重复了"、"以哪个为基础重铸"。

### 三步 / Three steps
1. **库审计（只读）**：`scripts/recast_scan.py` 扫描 `~/.workbuddy/skills/` 聚类 → 输出《重铸计划报告》。
2. **审报告**：每聚类成员 + 三维分（使用率/完整度/牛逼度）+ 推荐基座 + 正负面影响 + 工作流影响（仅供参考）。
3. **合并（仅确认后）**：用户选基座 + 逐技能确认 → 原技能先备份 + 被并者标记 deprecated（绝不物理删除）→ 继承基座 slug + 使用历史 → 接入迭代环。

### 铁律 / Iron rules
- 默认**仅分析**，绝不自动合并；合并须逐技能确认；**不删除**任何技能；合并前**自动备份**到 `.backup/`；继承基座 slug + usage 历史；向量 key **外部化**（仅本地 secrets/env，无 key 自动回退轻量聚类）。

详见 `references/skill-consolidation.md`。

---

## 模式 D — 内嵌清晰化（EMBEDDED CLARITY）

> 把 `skill-clarity-forge` 的清晰化能力**内嵌**进锻造循环（**S7 闸门**），让每个锻造/升级技能默认「AI 易读」——且**绝不改它"做什么"**（保真红线，纪律 14）。

### 何时进入 / When to enter
- 每个技能锻造/升级循环走到 **S7**（发布前最后一道可读性闸门）。
- 用户显式要"把这个技能改得更 AI 易读 / 去术语化 / 给 agent 看"。

### 内嵌清晰化四维 / Four clarity dimensions
- **D1 降术语改写**：密集专业表述 → 显式单义语言；术语定义一次后复用。
- **D2 补示例与类比**：每个抽象规则补 ≥1 具体例子；高歧义处补正反对照。
- **D3 重排结构（渐进披露）**：前置执行摘要；流动散文 → 原子编号步骤；I/O 契约显式化。
- **D4 加通俗摘要层**：文首加 AI 面向摘要（何时触发/做什么/期望输入/产出/硬红线/范围边界）。
- 类型 × 维度强度矩阵见 `references/clarity-coverage.md`。

### 写作规范（S7 附加维度：结构 / 披露 / 加载）
> **为什么**：四维解决"AI 读得准"，写作规范解决"SKILL.md 该长什么样、哪些能写哪些不能写、哪些必须内联"。二者在 S7 一起跑。
> 完整标准见 **`references/skill-writing-guide.md`**（导航式模板 / 披露范围：只写用户侧禁生产侧文案 / 按需加载 / 必要内容内联 / 校验门）。要点：
- **导航式结构**：SKILL.md ≤250 行，只留 路由+红线+用户可见；细节下沉 references（开头注明加载时机）。
- **披露范围**：不写迭代代号（Wave/Phase）、版本更新史（"v2.x 新增/本次重构"）、内部模块代号、内部编码（L2/L3/L4、C1–C7）——只写"能做什么/怎么用/数据去哪/如何关闭"。
- **不跳过必要内容**：红线、触发词、注入三件套（燃料/footer/coverage）、关键命令、隐私说明必须内联，不能依赖加载。
- **校验门**：发布前跑第 5 节检查清单（规模/无生产侧文案/触发/红线/三件套/引用完整/加载声明/发布工具校验）。

### 保真红线（硬约束 · 不可跳过）
清晰化**只改「怎么说」，绝不改「做什么」**。核对清单见 `references/clarity-fidelity-template.md`，逐项 ✅/⚠️/❌；任一 ❌ 或 ⚠️ 涉及功能 → 回退收窄。
- 可选可执行闸：`skill-clarity-forge` 的 `scripts/fidelity_diff.py <原> <改> --report`（退出码 1=回退）；`scripts/extract_glossary.py` 抽候选术语。

### 与锻造循环的衔接
S7 闸门（强制）在 **S6 校验打包 + 安全审查** 之后、发布前；内容：清晰化四维 + 保真闸 + **写作规范门**（`skill-writing-guide.md` 第 5 节校验清单）；未过则回退 S2/S3 收窄。
