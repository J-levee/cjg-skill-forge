# Skill Types · 技能类型与适配要点

skill-forge v1.0 leaned on the 扫地僧 persona case. A global-best meta-skill must cover ALL skill shapes. Pick the type before you forge; the disciplines apply differently per type.

## 1. Utility skill (工具型)
Examples: pdf, docx, xlsx, web-artifacts-builder, book-searcher.
- Core: deterministic, reproducible operations on a file/format/API.
- Forge focus: **D7 verification** (exact I/O examples), **D8 robustness** (malformed input), **D1 trigger** (file extension / intent keywords).
- Lean is everything — a utility skill is often PURE PROMPT (single SKILL.md, no refs).

## 2. Workflow skill (流程型)
Examples: tcb-deploy, wechatpay-scf-deploy, smartlib-email-campaign.
- Core: a multi-step SOP with ordering, gates, and rollbacks.
- Forge focus: **D2 scope** (when NOT to auto-run), **D8 robustness** (rollback / 回退方案), **D9 maintainability** (versioned SOP template).
- Production-sign-off (Discipline 5) is MANDATORY here — these touch live systems.

## 3. Coding skill (编码型)
Examples: code-reviewer, test-driven-development, using-git-worktrees.
- Core: guides the agent to write/refactor/test code correctly.
- Forge focus: **D4 coverage** (which languages/frameworks), **D7 verification** (run the tests), **D8 robustness** (don't bypass hooks).
- Pair with real repo context; the skill is the discipline, not the implementation.

## 4. Persona / expert skill (人设型)
Examples: 扫地僧, sweeping-monk, any branded advisor.
- Core: a character users trust enough to follow.
- Forge focus: **D6 differentiation** (signature voice), **D5 evidence** (confidence tiers, no lie), **acquaintance memory** (knows the user).
- See `references/persona-design.md`. This is the ONLY type that needs a voice/character layer.

## 5. Agent / orchestration skill (编排型)
Examples: dispatching-parallel-agents, subagent-driven-development.
- Core: decomposes work and coordinates sub-agents/tools.
- Forge focus: **D2 scope** (what NOT to delegate), **D8 robustness** (partial failure), **D1 trigger** (task-size threshold).
- Keep the human in the loop for destructive ops.

## Cross-cutting
- **Pure-prompt vs full-structure**: if the whole method fits in <500 lines, ship ONE SKILL.md (utility/workflow). Add `scripts/`+`references/` only when needed (Anthropic/skillstore.io guidance).
- **Frontmatter**: `name` (lowercase-hyphen, ≤64, matches folder), `description` (≤1024, double-quoted, NO angle brackets), `agent_created: true`, optional `version`/`license`/`compatibility`/`allowed-tools`.
- Every type benefits from **D4 coverage audit** — just pick the right taxonomy (UNESCO/中图法 for academic; ACM CCS for CS; ICD for medicine; MECE for business; file-format matrix for utility).
