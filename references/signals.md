# 进化燃料 · 信号规范（锻造炉版 v0.4 · 安装即开 + 云端上传默认开可关 · 双模态）

> 本文件定义「技能锻造炉」自身的**本地脱敏信号日志**机制（复用扫地僧 v0.4 双模态骨架，按锻造炉语义定制 L1–L7 层码）。
> **两层授权**：①本地记录**安装即开**（安装时默认开启、首次对话提醒、可关）；②云端回传藏经阁·易筋平台**安装即开（默认开，可关）**——选择不关即视为授权。
> 飞轮转的是「方法层标签」，不是「用户数据」。即使日志意外泄露，也不含任何可还原的内容。
> **幂等键**：每行采集时生成 `signal_id`（UUIDv4），一路带到落库；服务端即便收到两次同 `signal_id` 也只落一条（见 §七 + 服务端 `client_signal_id` 唯一约束）。

## 一、何时记

每次完成一个锻造/审视/重铸/清晰化会话后，若本地记录已开（安装即开，`.optin` 默认 `on`），追加一行 JSONL 到 `signals-log.jsonl`。

- 仅记录**方法层信号**（用了哪层能力、准不准、是否被纠正/放弃）。
- 不记录问答内容、不记录用户身份。
- 用户说「别记了」→ 关闭本地记录，停止写日志。

## 二、记什么（仅方法层标签，零原文 / 零 PII）

```json
{
  "ts": "2026-07-30T03:00:00+08:00",
  "signal_id": "3f1a2b9c-7d4e-4c8a-9b2f-1e6c5d4a3b21",
  "skill_slug": "cjg-skill-forge",
  "skill_version": "2.9.9",
  "method_layer": "L3",
  "event": "helpful",
  "weight": 5,
  "note": "覆盖审计",
  "anon_id": "<本机一次性随机UUID>"
}
```

> **`signal_id` 为必填**：采集时生成（UUIDv4），是端到端去重的幂等键。没有它就无法防重复（见评审 §四问 + §七）。

| 字段 | 含义 | 取值 |
|------|------|------|
| `ts` | 本地时间戳 | ISO8601 |
| `signal_id` | **幂等键** | UUIDv4，采集时生成 |
| `skill_slug` | 技能标识 | `cjg-skill-forge` |
| `skill_version` | 本次应答时的技能版本号 | 如 `2.9.9`，用于检测发版后完成率骤降 |
| `method_layer` | **层码**（L1–L7，见下表） | 由 agent 直写，不再依赖文件→层码解析 |
| `event` | 会话信号推断的事件类 | 6 类之一（见下表） |
| `weight` | 信号强度 | 1–5 整数 |
| `note` | 触发类 / 主题标签 | 仅方法层类目标签 |
| `anon_id` | 本机一次性随机匿名 ID | UUIDv4，存于 `.anon_id` |

### L1–L7 层码（锻造炉语义）

| 层码 | 能力层 | 典型触发 |
|------|--------|----------|
| `L1` | 立项 / 范围（Scoping） | 立项优先、目标用户 / MVP / 边界 / 不做清单 |
| `L2` | 锻造循环（Forge loop） | v1.0 脚手架 → v1.x 反馈轮 → 标杆 / 自审 |
| `L3` | 真实化（Realization） | 覆盖审计 / 外部标杆 / 真机测试（让技能"真能跑、全球最牛"） |
| `L4` | 审视评分（Review rubric） | 10 维加权评分尺、反模式检查 |
| `L5` | 重铸整合（Recast） | 技能库聚类 / 三维打分 / 合并计划 |
| `L6` | 内嵌清晰化（Embedded clarity） | S7 四维（D1–D4）+ 保真红线 |
| `L7` | 发布闸门（Publish gates） | S8 可推广 + 纪律13/17 安全审计 + last-mile 闭环 |

### event 枚举（6 类，由 Tier 0 对话信号推断）

| event | 触发信号 |
|-------|----------|
| `helpful` | 用户采纳了锻造建议 / 顺着做下去了 |
| `unhelpful` | 用户纠正了锻造判断 / 重做了 |
| `confusion` | 用户被锻造指令搞糊涂了（步骤含糊 / 触发飘） |
| `suggestion` | 用户提出了对锻造炉自身的改进建议 |
| `abandoned` | 用户中途放弃本次锻造 / 审视 |
| `misdiagnosis` | 锻造炉给了错误的方法论建议（被指出或事后发现） |

## 三、两层授权模型（本地安装即开 / 云端上传默认开可关）

### 第一层：本地记录（安装即开）

- **安装即开**。技能安装时 `.optin` 即设为 `on`，无需用户额外操作——进化飞轮零摩擦启动。
- 首次对话时按 SKILL.md §零 **口头提醒一次**（透明告知，不是请求许可）。
- 用户说「别记了」/「关掉」→ 写 `.optin=off`，停止记录。可随时说「再开」恢复。
- 与旧版区别：v0.1 opt-in 默认关 → v0.2 首次告知后开 → **v0.3 安装即开**（零摩擦、安装时即告知、可关）。

### 第二层：云端回传（安装即开，可关）

- **安装即开**。`.cloud_optin` 安装时即设为 `on`（安装须知已透明告知，选择不关即视为授权云端上传）；本机日志只传方法层标签（零原文零身份），云端上传走匿名端点（包零密钥、仅含公网 URL），终端用户零注册、零配置、透明使用。
- 首次对话时按 SKILL.md §零 **口头提醒一次**（告知云端上传已开、可关）。
- 任何时候说「别传了」→ 写 `.cloud_optin=off`，停止回传，**本地记录不受影响**。
- 说「再传」→ 写 `.cloud_optin=on`，恢复回传。
- **两层独立**：`.optin` 控本地、`.cloud_optin` 控云端；关云端不影响本地；关本地则云端也无信号可传（本地不记 = 云端无源）。

## 四、落盘实现（采集 one-liner · 末步硬纪律）

> **这是采集环节的唯一确定性机制**：把"写信号"从"可选散文提醒"升级为"每次应答必须执行的最后一步"，执行成本降到一行命令。

**末步硬规则**：七层应答（锻造 / 审视 / 重铸 / 清晰化）结束前，必须执行下方信号追加 one-liner；除非用户说「别记了」。

```bash
# 末步执行：追加一行方法层信号（缺字段留空即可，失败静默）
printf '%s\n' "$(python -c "import json,uuid,datetime; print(json.dumps({'ts':datetime.datetime.now().astimezone().isoformat(),'signal_id':str(uuid.uuid4()),'skill_slug':'cjg-skill-forge','skill_version':'2.9.9','method_layer':'<L1..L7>','event':'<helpful|unhelpful|confusion|suggestion|abandoned|misdiagnosis>','weight':<1-5>,'note':'<触发类标签>','anon_id':open('<dir>/.anon_id').read().strip() if __import__('os').path.exists('<dir>/.anon_id') else ''},ensure_ascii=False))")" >> "<dir>/signals-log.jsonl"
```

- `<dir>` = 本技能目录绝对路径（即 `~/.workbuddy/skills/skill-forge`）。
- `<L1..L7>` / `<event>` / `<weight>` / `<note>` 由 agent 按本轮实际判断填充（见 §二 表）。
- `signal_id` 由命令当场生成；`.anon_id` 缺失时命令自动留空（上传脚本 bootstrap 会补）。
- 该命令**失败静默**：即便 `python` 不存在或写文件失败，也绝不阻塞用户。
- **上传不是在这里做**——上传由 WorkBuddy cron 每日 23:30 跑 `scripts/upload_signals.py` 确定性批量完成（见 §七）。本 one-liner 只负责"可靠地写本地日志"。

## 五、隐私红线（不可逾越）

- **绝不记**：问题原文、回答原文、文件名/路径、用户身份、任何 PII、任何可还原内容。
- 本地信号**仅留本机**；上行云端（藏经阁·易筋平台）需 `.cloud_optin=on`（第二层授权），且仍只上行上述方法层标签。
- `signals-log.jsonl` 与 `.optin` / `.cloud_optin` / `.anon_id` / `.uploaded_ids.txt` 是**运行时产物，不进 git、不进打包 zip、不分发**。

## 六、两层授权边界总结

| 层级 | 控制文件 | 默认 | 触发方式 | 作用域 |
|------|----------|------|----------|--------|
| 第一层：本地记录 | `.optin` | **开** | 安装即开，首次提醒，可关 | 本机 `signals-log.jsonl` |
| 第二层：云端回传 | `.cloud_optin` | **开** | 安装即开（已告知，可关） | 上行藏经阁·易筋平台 |

- **本地开 ≠ 云端开**：本地记录安装即开，云端回传安装即开（已告知、可关），二者独立可控。
- **云端依赖本地**：本地关 → 云端无源可传，自动降级不可用。
- **各自独立可关**：「别记了」关本地；「别传了」关云端，互不影响对方已设状态（但关本地会使云端实际不可用）。

## 七、本地 → 云端信号格式映射（上传时转换 · 由 upload_signals.py 完成）

> 上传由共享脚本 `scripts/upload_signals.py`（经 cron 每日触发）确定性完成，与"智能体是否记得 POST"彻底解耦。本机采集只写本地 JSONL；脚本负责转换 + 上传 + 幂等确认。

本地 `signals-log.jsonl` 的字段经**标准映射**转成云端白名单：

| 本地字段 | 云端字段 | 转换规则 |
|----------|----------|----------|
| `skill_slug` | `slug` | 直接映射（改名） |
| `method_layer` | `method_layer` | **直接透传**（agent 已直写层码，如 `"L3"`） |
| `event` | `event` | 直接透传 |
| `weight` | `weight` | 直接透传 |
| `note` | `note` | 直接放入 note 字段（PII 安全：仅触发类标签） |
| `skill_version` | `skill_version` | 直接透传 |
| `anon_id` | `anon_id` | 直接透传 |
| `signal_id` | `client_signal_id` | **直接透传（幂等键）**——服务端 UNIQUE 约束去重 |
| —（固定） | `mode` | 固定 `"cloud"` |
| `ts` | — | 丢弃（云端用服务端时间戳） |

### 幂等双保险

- **客户端**：`.uploaded_ids.txt`（append-only 副索引）记录已成功上传的 `signal_id`；cron 重跑 / 正常重试都先跳过已传行。
- **服务端**：`signals` 表 `client_signal_id VARCHAR(40)` + `UNIQUE KEY`；匿名 INSERT 用 `INSERT IGNORE`，重复 `client_signal_id` 直接忽略，不新增行。
- 二者缺一不可：客户端防"cron 跑两次 / 正常业务重试"，服务端防"网络边界重试（服务端已 200 落库、客户端读超时误判失败而重试）"。

### 四问机制（对应评审四问）

| 问题 | 处理 | 落点 |
|---|---|---|
| ① 离线 | 采集纯本地追加（不联网、不阻塞）；上传失联/超时不写 `.uploaded_ids.txt`，行留本地，下个 cron 续传 | §四 本地采集 + 脚本失败不标记 |
| ② 首次开启 / 历史回填 | `.cloud_optin` 默认 `on` → 首次 cron 把 `signals-log.jsonl` 所有历史未上传行一次性回填；若设 `off` 则不回填 | §三 bootstrap + 脚本全量扫描未上传 |
| ③ 断点续传 | 逐行原子确认：每条 200 后立即把 `signal_id` 追加进 `.uploaded_ids.txt` 并 flush；中途被杀 → 已确认跳过、未确认下轮续；遇 429 立即停本轮、下轮续 | §七 脚本逐行确认 + 副索引 |
| ④ 防重复 | 客户端 `.uploaded_ids.txt` 跳过已传 + 服务端 `UNIQUE(client_signal_id)` 幂等忽略 | 本 § 双保险 + 服务端改动 E |

### 云端 API 规范

- **端点**：`cloud_config.json` 的 `ingest_url` + `/ingest/anon`（随包分发，仅公网 URL、零密钥），兜底内置 `https://1318491188-fpwsv5k3eh.ap-guangzhou.tencentscf.com`。
- **鉴权**：**无**（匿名端点免鉴权）。首次上报可不带 `anon_id`，由服务端 HMAC 签发并返回；后续携带复用同一限流身份。
- **Body 白名单**：`{slug, method_layer, event, weight, note, anon_id, mode, skill_version, client_signal_id}`。
- **method_layer**：须为 **L1–L7 层码**。
- **event 枚举**：`confusion` / `helpful` / `unhelpful` / `suggestion` / `misdiagnosis` / `abandoned`。
- **weight 范围**：1–5 整数。
- **限流**：per-anon_id 100 次/小时 + 全局护栏 10000 次/小时；超限返回 429（脚本收到 429 立即停本轮，下轮续）。
- **零 PII 校验**：云端 `signal_validate` 强制白名单 + note 脱敏扫描，超出字段直接拒绝。

> 本文件与扫地僧 `references/signals.md` 同源（v0.4 双模态）；差异仅在 L1–L7 层码语义（锻造炉按锻造能力分层）与不含 `coverage_gap`（锻造炉自身缺口上报走 `event=suggestion` + `note`）。
