# Anti-Patterns · 坏技能清单（审查时逐项排查）

A skill that looks done but exhibits these is NOT best-in-class. Review mode checks each.

## AP1 — The thin scaffold (薄脚手架)
Symptom: SKILL.md is 30 lines of vague intent ("help the user with X"). No method, no examples, no edge cases.
Fix: add concrete procedure, 1–2 worked examples, failure modes. If it can't exceed a paragraph, it shouldn't be a skill (see D2).

## AP2 — Prompt-in-a-folder (文件夹里的 prompt)
Symptom: content is a generic instruction any LLM already knows ("be helpful, be concise"). Adds zero capability.
Fix: only include context the model LACKS (Anthropic best-practice). If you delete the skill and the agent does the same job, it was never a skill.

## AP3 — Bloated SKILL.md (肥胖主文件)
Symptom: SKILL.md > 500 lines / > 5k words; everything inlined; references/ empty.
Fix: push detail to `references/`; keep SKILL.md the map, not the territory (D3).

## AP4 — Fabricated evidence (编造引用)
Symptom: cites books/papers with ISBN/DOI/id that were never verified; "according to Smith (2019)" with no real source.
Fix: every id must come from a real search (book-searcher / global-biblio-base / catalog). Mark `知识(建议确认)` vs `搜索核实`. A skill failing this caps at 69 (D5 red line).

## AP5 — Trigger blindness (触发失明)
Symptom: `description` says what the skill IS, not when to USE it; no trigger keywords; agent never invokes it, or invokes it wrongly.
Fix: write description as "Use when the user asks for X / mentions Y". Add `allowed-tools`/`recommends` if needed (D1).

## AP6 — Scope creep (越界)
Symptom: a literature-search skill also tries to do payments; a utility skill sneaks in opinion.
Fix: state the mandate AND the non-mandate (D2). The persona advises; the user decides.

## AP7 — No verification (未验证就宣布完成)
Symptom: "done" with zero real questions run through it.
Fix: run 2–3 real prompts (or an eval harness); record pass/fail (D7).

## AP8 — Imagined "best" (想象中的最牛)
Symptom: calls itself "the best" with no external benchmark and no rubric score.
Fix: benchmark vs top public skills (awesome-agent-skills, superpowers, Anthropic official); score on the rubric (D10 + this file).

## AP9 — Undifferentiable (无差异)
Symptom: a competent but generic skill with no unique angle — a vanilla LLM does the same.
Fix: find the wedge — a signature method, voice, or data source the model lacks (D6).

## AP10 — Unmaintainable (不可维护)
Symptom: no version, no changelog, references are a dump. Next session can't tell what changed.
Fix: SemVer + iteration log; structured refs (D9).
