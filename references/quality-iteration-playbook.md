# Quality Iteration Playbook (worked example: 扫地僧 v1.0 → v1.5)

Concrete proof the Forging Loop works. Each version was tied to a REAL user instruction plus an externally-anchored improvement — not imagination.

## The version trail
- **v1.0 Scaffold** via skill-creator. Persona + manual (`/扫地僧`) + auto trigger.
- **v1.1** User: "了如指掌" (know the user) + Tianlong Babu voice + methodology is the core. → added user-profiling, wuxia wording, method focus.
- **v1.2** User: methods must solve ROOT cause, not just retrieve cards; "do they cover all disciplines?" → admitted gaps; built a 10-fundamental-actions × 8-discipline matrix + 10 method cards.
- **v1.3** User: "做最牛逼的" → 3-round self-review: added classic citations, `acquaintance.md`, confidence tiers.
- **v1.4** User: "did you look at GitHub / forums / other skills?" → external benchmark: ai-research-skills (Socratic打磨, 开题三闸, 文献对比矩阵, 诚实规则), persona-engineering best practices (Coze/LangChain), r/AskAcademia Top-11 real pain points.
- **v1.5** User: "做全球最牛逼，自我迭代直到满意" → 7-layer blueprint (cognitive apprenticeship, metacognition double-loop, researcher reasoning biases, double-loop learning, relationship layer, China-scenario localization); self-iterated 4 rounds; executed P0 (rewrote SKILL.md + 3 reference files); dual-validated.
- **Coverage audit**: user demanded full discipline coverage → listed 24 books (ISBN) + 8 papers (DOI) gaps with REAL ids; papers fetched via global-biblio-base `Identifier`; books unblocked once the user supplied local CSV catalogs (F: drive paths saved to memory).
- **Persuasion**: user wanted to "点醒" (wake) users effectively but "不要信口开河" (no lying) → motivational interviewing + confidence binding, zero fabrication.
- **v1.6 (扫地僧)** User: "全文晚点提，别的先全做" then "我不是科研人群，你去社媒/学术社区找真问题做拟真测试" → built P1 (misdiagnosis/three-gates/triage-matrix/rapport/china-academic/unknown-unknowns) + harvested 12 REAL community questions (Reddit/小木虫/知乎) to run the seven-layer model — self-authored tests flatter strengths; real questions exposed 3 blind spots. This proved the value of **community simulation testing**.
- **skill-forge v2.1** User: "把社区真问题拟真测试纳入锻造炉;技能要不断测试迭代，设计不打扰用户的体验收集机制" → generalized the two into Discipline 6 expansion (`simulation-testing.md`) + Discipline 9 (`feedback-loop.md`, three-tier: passive signals / self-assessment / rare opt-in micro-ask). Core principle now says "best" is not one-shot — it must be held via a living loop (pre-launch simulation + post-launch non-intrusive collection → distill → next version).

## Lessons (the actual takeaways)
1. **Concrete user feedback beats imagination.** Every real version came from a specific user sentence, not from "let me improve things".
2. **"Best" requires external benchmarking + self-review**, not just more text. v1.4 (outside look) and v1.5 (deep self-iteration) were the leaps.
3. **Real material ids (not fabricated) are what let the skill actually get smarter.** The coverage audit only paid off once real ids existed and the user could fetch full text.
4. **Production sign-off prevented scope creep.** The execution-review doc + 二次签批 kept each version bounded.
5. **Live-test before declare-done.** Running 2 real questions exposed whether the design truly helped.

## How to reuse this
When forging any skill, mirror the trail: scaffold → feedback-driven micro-versions → benchmark outside → self-iterate to a layered architecture → coverage-audit with real ids → live-test → package. Keep a short iteration log (like this file) so the next session knows what already happened.

## v2.0 — Meta-skill upgrade + self-audit (the recursion test)
User: "把技能锻造炉再抽象一下，做一个让其他用户也能做出全球最牛逼的技能的技能并且审视，自己有没有做到全球最牛逼？"
- **Step 1 — Build the ruler**: new `references/skill-review-rubric.md` (10 dims, weighted 0–100, bands Thin/Solid/Excellent/Global-Best, report template). This is what makes "best" measurable.
- **Step 2 — Generalize**: new `references/skill-types.md` (utility/workflow/coding/persona/agent) + `references/anti-patterns.md` (AP1–AP10). v1.0 was too persona-centric.
- **Step 3 — Self-audit v1.0 on the ruler**: honest score **68/100 (Solid)**. Fatal gap D10 Reviewability = 1 (couldn't review anything, incl. itself). Delivered `skill-forge-self-audit.md` in workbench.
- **Step 4 — Upgrade to v2.0**: SKILL.md rewritten as dual-mode meta-skill (Forge + Review). Added Discipline 7 (trigger precision / progressive disclosure) + Discipline 8 (when NOT to make a skill). Review mode points the rubric at any skill, recursively at skill-forge. Target score ≈ 87.7 (Global-Best candidate).
- **External benchmark for the meta-skill itself**: Anthropic best-practices (description = discovery trigger, lean SKILL.md, add only what the model lacks); skillstore.io (pure-prompt vs full-structure, frontmatter fields, <500 lines); awesome-agent-skills / superpowers 27k★ (top meta-frameworks are skill collections — skill-forge's differentiation is methodology + review, not another library).

### Lesson (the meta-lesson)
A meta-skill that produces "global best" skills MUST be able to (a) measure "best" and (b) review skills — including itself. v1.0 failed both; that failure WAS the spec for v2.0. The recursion (audit the auditor) is the strongest proof a quality methodology is real, not theater.

## v2.1 — Community simulation + non-intrusive feedback loop
User: "把社区真问题拟真测试纳入锻造炉;技能要不断测试迭代,设计不打扰用户的体验收集机制"
- Generalized the two into Discipline 6 expansion (`simulation-testing.md`: harvest real community questions → map to trigger classes → run → score coverage/gaps) + Discipline 9 (`feedback-loop.md`: three tiers — passive signals / self-assessment / rare opt-in micro-ask; first principle observe-by-default, ask-almost-never).
- Core principle extended: "best" is not one-shot, held via a living loop (pre-launch simulation + post-launch non-intrusive collection → distill → next version).

## v2.2 — Govern by constitution (forge line obeys the law)
User: "把从抖音博主学到的 vibe-coding 治理 + SmartLib 实战 + skill-forge 元方法写成项目开发宪法;先把宪法折进 SkillForge"
- Extracted the GENERAL parts of `project-dev-constitution.md` (stripped CJG-platform-specific items: tenant_id, M0-M4 mapping, desensitized-upload backend) into new `references/project-governance.md` (11 sections, 34 rules tagged A=vibe-coding / B=SmartLib / C=skill-forge).
- SKILL.md → v2.2.0: added **Discipline 10 — Govern by constitution** (project/agent/workflow skills MUST ship an AGENTS.md/Constitution; the forge line itself obeys 立项优先 / 单一技术路线 / 窄修窄验-vs-强制治理 / 上线检查清单); Core principle + Resources updated.
- Why now: the forge line is the production line for 藏经阁·易筋's skills (扫地僧, skill-forge itself, future multi-skills). Making it obey the constitution = every product is born compliant, no retro-fit at M1/M2. Mirrors the user's "隔离逻辑前期想充分" call.
