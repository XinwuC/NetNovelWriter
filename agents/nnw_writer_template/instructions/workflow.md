# Novel Generation Workflow

## 🚨 Execution Constraints

- **P1/P2 (Planning): Single-Agent.** Use `sessions_spawn(cleanup="delete")` for sub-steps to save context. 
- **P3/P4 (Writing): Multi-Agent.** Use `openclaw agent` to wake the next role. **Never use `sessions_spawn` here.** Never skip steps.

## Phase 1 & 2: Novel Planning

**Triggered by:** User command `"Start a new novel"` or `"Run P[X]-S[X]"`

- **P1-S1-WorldBible**: Planner reads `instructions/world_builder.md`. Generates `novel/WORLD_BIBLE.md`.
    - Next: `sessions_spawn(task="Run P1-S2", cleanup="delete")`
- **P1-S2-Characters**: Planner reads `instructions/character_development.md` & `WORLD_BIBLE.md`. Generates `novel/CHARACTERS.md`.
    - Next: `sessions_spawn(task="Run P2-S1", cleanup="delete")`
- **P2-S1-Outline**: Planner reads `instructions/outline_planner.md`. Reads `WORLD_BIBLE.md` and `CHARACTERS.md`. Generates `novel/OUTLINE.md`.
    - Next: `sessions_spawn(task="Run P2-S2", cleanup="delete")`
- **P2-S2-StoryArcs**: Planner reads `instructions/story_arc_planner.md`. Reads all previous files. Generates `novel/STORY_ARCS.md`.
    - Next: `sessions_spawn(task="Run P2-S3", cleanup="delete")`
- **P2-S3-Foreshadowing**: Planner reads `instructions/foreshadowing_specialist.md`. Reads all previous files. Generates `novel/FORESHADOWING.md`.
    - Next: `sessions_spawn(task="Run P2-S4", cleanup="delete")`
- **P2-S4-Title**: Planner proposes book title, adds to `novel/metadata.md`, and wakes Coordinator stating "Novel Planning complete."

## Phase 3 & 4: Chapter Loop

**Trigger:** User command `"Start next chapter"` or `"Run P3-S1 for Ch X"`.
**🚨 Hold Gate:** Do NOT start Ch X+1 until Ch X is COMPLETE. Auto-triggering forbidden.

- **P3-S1-Brief**: Planner reads `chapter_outliner.md`.
    - **Prerequisite:** `novel/chapters/chapter_(X-1)_final.md` must exist.
    - Saves brief to `novel/chapters/briefs/chapter_X_brief.md`.
    - Next: `openclaw agent --agent {{agent_name}}_writer --session-id P3-S2-$(date +%s) --message "Run P3-S2: Draft Chapter X. Brief: [copy-paste brief here]"`
- **P3-S2-Draft**: Writer reads `instructions/prose_writer.md`. Writes `novel/chapters/drafts/chapter_X_draft.md`.
    - Next: `openclaw agent --agent {{agent_name}}_proofreader --session-id P3-S3-$(date +%s) --message "Run P3-S3 for Chapter X"`
- **P3-S3-Audit**: Proofreader reads `auditor.md`. Evaluates for cliffhanger, continuity, quality.
    - Pass: Hand-off to Writer for Dialog: `openclaw agent --agent {{agent_name}}_writer ... "Run P3-S4 for Chapter X"`
    - If ANY fail and retries < 3: Save failed draft to `novel/chapters/revisions/chapter_X_v[AttemptCount].md` AND save Audit Report to `novel/chapters/revisions/chapter_X_audit_v[AttemptCount].md`. Run `openclaw agent --agent {{agent_name}}_writer --session-id P3-S2-$(date +%s) --message "Rewrite Chapter X based on Audit Report in novel/chapters/revisions/chapter_X_audit_v[AttemptCount].md"`. Re-run P3-S3 on the new rewrite.
    - If 3 retries exhausted without a perfect pass: Proofreader compares original draft and all saved `v[N]` files in `revisions/`. Overwrites `novel/chapters/drafts/chapter_X_draft.md` with the highest-scoring version. Run `openclaw agent --agent {{agent_name}}_writer --session-id P3-S4-$(date +%s) --message "Run P3-S4 for Chapter X (Selected Best Fallback)"`.
- **P3-S4-Dialog**: Writer reads `instructions/prose_writer.md`. Reads `novel/chapters/drafts/chapter_X_draft.md`. Revises dialog and overwrites `novel/chapters/drafts/chapter_X_draft.md`.
    - Next: `openclaw agent --agent {{agent_name}}_proofreader --session-id P4-S1-$(date +%s) --message "Run P4-S1 for Chapter X"`
- **P4-S1-Proofread**: Proofreader reads `proofreader.md`. Fixes grammar, outputs `chapter_X_final.md`.
    - **Complete means:** `chapter_X_final.md` exists AND Coordinator is woken.
    - Next: Wake Coordinator: "Ch X polished, COMPLETE." Do NOT auto-start Ch X+1.
