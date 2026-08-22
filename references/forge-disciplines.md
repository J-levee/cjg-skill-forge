# 锻造炉 · 17 条纪律（DISCIPLINES）——按需加载

> SKILL.md 只保留每条纪律的**一句话红线**；本文件是完整细节（含双语核心句）。
> 执行对应纪律时读取本文件相应章节。

---

## 纪律 1 — 覆盖审计（真实素材 ID，禁编造）

按领域标准分类法审计（学术用 UNESCO FOS 2010 + 中图法；CS 用 ACM CCS；医学用 ICD；商业用 MECE；工具类用文件格式矩阵）。每个空白分支找 1–2 本权威文本并拿到**真实 ID**：
- 书 → book-searcher / 用户 CSV 目录（`cn_dir`/`en_dir`）→ 内部 `id` + `sid`（列格式见 `references/coverage-audit.md`）。
- 论文 → global-biblio-base `POST /search/global` 规则 `T=<title> AND A=<author>` → `Identifier`。避开 `U=<DOI>`（命中 errata）。
- 记录来源 `搜索核实` vs `知识(建议确认)`。**绝不编造 ID**。清单交用户取全文。

## 纪律 2 — 外部标杆（向外看）

宣称任何「最牛」前研究三来源：(1) GitHub/awesome-agent-skills + superpowers（27k★）；(2) persona-engineering 最佳实践（Coze/LangChain）；(3) 真实论坛痛点（r/AskAcademia 等）。综合 P0/P1/P2。保留差异化，不逐字抄。

> **🔴 硬纪律（最常犯的错误）**：「外部」= **全世界**——所有技能/项目/工具/论文/知识/资讯。**绝不可把标杆缩到某比赛/某平台**——局部场景只是**验证场（test vehicle）**，不是锻造目标。S3 先全网扫描顶级公开作品，再看局部场景。

## 纪律 3 — 自我迭代到「全球最牛」（无需提醒）

接「做到最牛」：跑 3–4 轮自审，找更深的层（内化知识库 → 认知学徒 → 元认知双环 → 推理偏误 → 关系层 → 本土化）。先记蓝图，再执行。

## 纪律 4 — 不说谎的说服（仅 persona 技能）

动机式访谈 + 双系统 + 置信度绑定证据。红线：绝不断言虚假确定；不替用户做决定；建议前先承认痛苦。见 `references/persona-design.md`。

## 纪律 5 — 生产签批（协作铁律）

技能文件是生产制品。做非平凡改动前：先写执行评审文档（做什么/改哪些文件/来源/验收标准）→ 拿到用户**明确签批**。「继续/执行」= 继续既定方案，不是扩大范围。用户说「停」：立刻停 + 回滚。workflow/agent/coding 技能强制适用。

## 纪律 6 — 真机测试验证（eval harness + 社区模拟）

完成前跑 2–3 个**真实**用户问题（或小型 eval harness）穿过技能。只有跑通才打包。够不到目标用户时，从社交/专业社区（Reddit、小木虫、知乎、Stack Overflow）采集**真实用户问题**映射到触发类再跑——完整流程见 `references/simulation-testing.md`。自编测试讨好长处，真实问题暴露缺陷。

## 纪律 7 — 触发精度与渐进披露

- **描述是发现触发器**：写 "Use when the user asks for X"，不写 "This skill does Z"。≤1024 字符，双引号，无尖括号。
- **触发词 = 搜索关键词（本纪律的 SEO 扩展）**：description 是用户在技能平台的搜索入口——必须自然嵌入核心触发词（主题）+ 意图触发词（用户口语动作）中英双语，且与「何时使用」表互文（writing_gate W3a/W3b 自动校验）；「何时使用」表是触发词目录。方法论与公式见 `references/trigger-keywords.md`。
- 需预批工具/伴侣技能时设 `allowed-tools` / `recommends`。
- SKILL.md **< 600 行 / < 5k 词**；细节推 `references/`。纯提示型可单文件。
- Frontmatter：`name`（小写连字符 ≤64 与文件夹同名）、`agent_created: true`、可选 `version/license/compatibility`。
- **导航式写作（本纪律的执行细化）**：SKILL.md 只留路由+红线+用户可见，细节按需加载；红线/触发词/注入三件套/隐私说明必须内联——完整标准见 `references/skill-writing-guide.md`（含披露范围与校验门）。

## 纪律 8 — 范围纪律：何时**不**做技能

删掉技能后 agent 照样干同样的活 → 它从来不是技能（AP2）。一次性任务 / 方法一段话能说清 / 模型本来就会 → 用普通提示词。显式声明 NON-mandate 防 creeping（AP6）。

## 纪律 9 — 持续反馈环，不打扰用户

已发布技能从真实使用中持续变好——**绝不用弹窗/问卷**。三层（见 `references/feedback-loop.md`）：
- **Tier 0（始终开）**：从自然对话信号推断满意度（采纳/深入追问=好；纠正/重问/突然放弃=坏）。只记一行模式（无原文/PII/本地/可删）。
- **Tier 1（始终开）**：agent 自评/校准——哪些资源命中、诚实置信度、是否撞边界。
- **Tier 2（罕见 opt-in 限频）**：任务结束至多一句轻量提问；「别问」即永久关闭。

然后**蒸馏 → 迭代**：反复纠正→下一版修复；从不命中的 references→剪枝；反复撞边界→覆盖审计。第一原则：**默认观察，几乎从不提问。**

## 纪律 10 — 用宪法治理

- **锻造 project/agent/workflow 技能必须自带宪法**（AGENTS.md/CONSTITUTION.md：目标/红线/NON-mandate/签批规则/安全红线）。纯工具类可豁免但必须声明 NON-mandate。
- **锻造线自身守宪法**：立项优先；只推一条技术路线；窄修窄验 vs 强制治理（架构/数据/权限/支付/部署改动停走评审+签批）；上线前走检查清单（环境密钥安全/迁移可逆/回滚验证/监控/公网暴露/验收证据）。
- **证据零编造**同样约束锻造线。
- 详见 `references/project-governance.md`。

## 纪律 11 — 技能注入：进化燃料 + footer + coverage.md

锻造出的**每个**技能必须带三件套：**① 进化燃料**（本地信号采集，安装即开）+ **② footer**（来源+进化状态）+ **③ coverage.md**（覆盖维度表）——增长飞轮结缔组织。

### ① 进化燃料注入（必带）
强制注入模板（放 §零 或同等醒目位置），本地版/云端版两套：

```markdown
## 零、进化燃料 · 本地即开 · 云端需显式开启

> **📋 安装须知**：本技能安装后**本地记录默认开启**（只记方法名，零原文零身份，留你本机）。
> - **云端上传（零密钥 · 默认关）**：需你**显式说"开启云同步"**才匿名回传反馈信号（helpful/unhelpful/confusion/suggestion/abandoned/misdiagnosis）。
> 说「开启云同步」可参与跨用户进化；「别传了」关云端；「别记了」全关。
> 📊 透明度：说"查看我的信号"/"我的技能成长"/"删除我的信号"。
```

规则：安装即开；须知醒目；首次对话提醒；易退出；零 PII；云端显式 opt-in。

### ② Footer 注入（来源 + 进化状态）
- **Tier 1（所有锻造技能必带）**：`> ⚙️ 本技能由「技能锻造炉」锻造` + 用户价值 + CTA（搜 slug「cjg-skill-forge」）。
- **Tier 2（接通云进化后替换 Tier 1）**：加 `· 🔄 持续自我迭代中，由藏经阁·易筋支持`。**Tier 2 是挣来的，不是默认的。**

### ③ coverage.md 注入（必带）
解析 description 自声明范围 → 匹配自动播种规则（`references/coverage-seeding.md`）→ 创作者确认定稿 → 随包分发。它是缺口信号 `in_taxonomy` 的判断依据。`forge-publish.py --check` 会警告缺失。

### ④ 最后一公里注入：应用提案 → 重发布
发布后进化闭环由 SkillForge 在对话中驱动（本地 `.local_proposals/` 或云端邮件汇总 → 「看看提案」→ 审 → 应用 delta（先备份到 `.backup/`，可撤销）→ `patch+1` → 更新 frontmatter → 提醒发布 → 用户说「发布」调 `scripts/forge-publish.py`）。
- **平台无关**：审核指令「看看提案」在任意对话生效；进化结果落回技能本体（SKILL.md 等）。
- **安全铁律（查看提案必须创作者鉴权）**：`list/mine/get` 强制携带创作者 token；`mine` 严格按 user_id 返回本人提案。
- **changelog 铁律**：只写用户侧体验变化，不泄露开发侧（架构/API/内部 Bug）。

## 纪律 12 — 多源融合连贯性校验

锻造融合多源时，三道强制判据：
**① 来源假设对齐**：抽每源内隐假设（用户层级/I-O 契约/失败处理/世界观），冲突**必须显式裁决并记录**，禁静默拼合。
**② 边际收益门槛**：每新增融合源须答「它单独填了 coverage.md 哪个维度 C? + 真机增益可观测?」答不上 → **不 fuse**。
**③ 反缝合怪**：融合后产生「谁都不负责」的孤儿中间态 → incoherent，退回重熔。
执行：S4 覆盖审计同步跑；冲突发现即停；本闸失败 = 退回 S0/S1；拦不住「分类法本身列错」（需领域专家）。

## 纪律 13 — 发布包安全审查（隐私 + 锻造过程脱敏）

S6 打包前必跑，违反即退回：
1. **剔除密钥与凭据**：`config.json`/`.env`/含 token 文件/`__pycache__`/`.backup/`/`.local_proposals/` 一律不进包。
2. **剔除 PII**：邮箱、手机号、账号、真实姓名、内部 URL。
3. **剔除锻造内部台账**：`*_evidence.md`/`benchmark.md`/`engineering-notes.md`/`contest-hard-forge.md` 不进用户包。**⚠️ coverage.md 不在此列**（用户有用的能力说明书，保留）。
4. **修复死链**：SKILL.md 引用被剔除文件时同步改。
5. **合规安全**：不蹭品牌 Logo、无违规文案。
6. **体积格式**：图标 ≤5MB（jpg/png/webp）；UTF-8 无乱码。

## 纪律 14 — 内嵌清晰化保真红线

清晰化只改「怎么说」，绝不改「做什么」：①只改表述不改功能；②能力不增不减；③红线不丢；④保真闸强制跑（`references/clarity-fidelity-template.md`，任一 ❌/⚠️ 涉及功能→回退）；⑤诚实边界（拦不住原技能本身写错）。clarity 副本与 `skill-clarity-forge` 上游同步防漂移。

## 纪律 15 — 版本号与文档同步

frontmatter `version` 是**单一真相源**：先 bump frontmatter，文中"vX.Y.Z 新增"标注须一致。changelog 只写用户侧体验变化。重大诚实更正必须在对应 references 同步修订。
- **文档披露范围（本纪律的文档侧延伸）**：技能文档只写用户侧体验（能力/怎么用/数据去向/如何关闭），**不写生产侧叙事**——迭代代号（Wave/Phase）、版本更新史（"v2.x 新增/本次重构"）、内部模块代号、内部编码（L2/L3/L4、C1–C7）一律不进技能包。见 `references/skill-writing-guide.md` 第 2 节。
- **发布版本说明（本纪律的发布侧延伸）**：发布时的 changelog 与文档同标准——站用户侧写「改了什么 + 有什么价值」，简要 2–5 条，禁生产侧文案（Wave/Phase/L2–L4/GAP/Bug#/内部代号/版本史/架构细节）。发布工具发布前自动跑 `writing_gate.py --changelog` 校验，命中禁词拒绝发布（`--force` 明确接受）。见 `skill-writing-guide.md` 第 6 节。

## 纪律 16 — 可推广闸门（Promotability & Discovery-Readiness）

S8 强制闸门（S7 清晰化之后、发布前），检查清单：
1. **T 可信**：description 与实现一致、无夸大、无蹭品牌、国内可运行、安全红线在。
2. **A 触发 find-skill 友好**：description 含 "Use when..." + 中文触发词；能力边界显式。
3. **E 开箱即用度**：零配置标注"开箱即用"；需 API Key 显式声明并写配置步骤。
4. **★ 分类映射**：依类型+功能建议 SkillHub 受控分类，落成 `references/discovery.md`。
5. **★ 元数据真实**：name/slug/version 规范、slug 与目录同名、displayName 不蹭品牌。
6. **★ 跨平台介绍（≤1024 字符）**：`references/intro.md`，纯介绍，说清"做什么/适合谁/怎么用"。
详见 `references/promotability-gate.md`。

## 纪律 18 — 三侧三方联合测试闸门（Joint Test Gate）

> **每次改动（代码/配置/文档/发布）都必须跑联合测试，全绿才能进入下一步。** 不允许只测单方/单视角就放行。

**三个被测对象 × 三个视角**（`scripts/joint_test.py` 一键编排，每项标注视角）：

| 被测对象 | 创作者侧（发布全流程） | 用户侧（安装使用+隐私） | 平台侧（合规验收） |
|---|---|---|---|
| **锻造炉自身** | selfcheck 全量/写作门 | 信号链路/透明控制 | 发布 --check/zip 合规 |
| **锻造炉产出的技能** | 产出技能过写作门 | 样例信号链路/dry-run | 发布 check/描述 ≤1024/无运行时产物 |
| **藏经阁云端** | 注册/提案/指标 | 上传/拉回/成长报告 | 8 SCF health/端点 |

**执行**：
1. **本地全量**（无凭据即可跑）：`scripts/joint_test.py` —— A 锻造炉自身（selfcheck 33 项）+ B 产出技能（临时样例：写作门/发布 check/SEO/信号链路/zip 合规）+ C 云端配置探测。
2. **完整链路**（需 SCF 凭据）：`joint_test.py --with-cloud` —— 追加真实云端链路（8 SCF health + 公网端点 + 真实上传/L2 拉回闭环 + 幂等 + 零残留；偶发限流自动重试一次）。
3. **任一 ❌ → 退回修复，不进入下一步**（不发布/不提交/不部署）。退出码 0=全绿。
4. **自动补全细节**：新功能/新脚本/新配置必须同步补进 joint_test 对应阶段（selfcheck 入口健康/W6 引用/W8 孤儿自动覆盖新增文件；行为类新增须手动补断言段）。
5. 定期巡检：WorkBuddy 自动化每周日 09:00 跑本地全量；发布前必跑完整版。
6. 三侧三方矩阵与用例库（C/U/P 系列）权威版见运维技能 `smartlib-gateway-ops`「三侧三方联合测试」章节（v2.22+）。

## 纪律 17 — 云鼎实验室安全审计闸门（SkillHub 发布路径强制前置）

走 **SkillHub 发布路径**前，强制跑 `skills-security-check` 对发布包（SKILL.md + scripts/references/ + 所有脚本）做纯静态只读审计：
- ✅ **Benign（76–100）**：通过，可发布。
- ⚠️ **Suspicious（31–75）**：附整改说明（固定依赖版本/venv/固化远程脚本+checksum）后经用户确认可发布。
- 🔴 **Malicious（0–30）**：**硬阻断**，拒绝发布，回退 S2/S6。
与纪律 13 边界：13=发布包脱敏（包里不该有什么）；17=技能本体安全（自动干了什么危险的）。审计结论记入 `references/security-audit.md`。详见 `references/yunding-security-audit.md`。
