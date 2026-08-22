# 藏经阁·易筋 — 云端增强包（cloud-enhancement）

> **本目录不随「技能锻造炉」基础技能包发布。** 基础包刻意保持「零后台、无定时任务代码」，以通过应用市场（SkillHub / ClawHub）的安全审核。需要**跨用户云端进化**的用户，单独取用本增强包后即可启用每日自动回传。

## 它做什么

- 把 `scripts/upload_signals.py`（位于上层技能目录）挂为**每日 23:30** 的本机调度任务：
  - Windows → Task Scheduler（`schtasks`，任务名 `CJG-SkillForge-SignalUpload`）
  - macOS / Linux → `crontab`（标记 `# cjg-signal-upload`）
- 仅在用户**显式说「开启云同步」** 后由 AI 调用安装；默认不挂任何后台任务。

## 使用

```bash
# 在 cloud-enhancement/ 目录下执行
python install_signal_cron.py --enable-cloud-upload   # 装每日 23:30 定时任务（幂等）
python install_signal_cron.py --uninstall             # 卸载
python install_signal_cron.py --force                 # 重建（需配 --enable-cloud-upload）
```

- 上传端点来自上层技能的 `cloud_config.json`（含 `ingest_url`，仅公网 URL、零密钥）；
  代码中**不硬编码任何 URL**，缺失则优雅跳过（仅本地记录）。
- 上传内容全部为方法层标签（零原文、零身份），按 `signal_id` 幂等去重，失败静默、断点续传。

## 安全说明

- 不读对话内容、不碰用户文件、不知道用户是谁（随机匿名 ID）。
- 仅在有新反馈时才上传；无新反馈静默跳过。
- 关闭只需说「别传了」或运行 `--uninstall`。
