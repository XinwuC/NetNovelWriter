# Novel Generation Workflow

The pipeline is fully automated and self-delegating. To prevent context explosion, agents MUST use the `sessions_spawn()` tool with `cleanup="delete"` to execute each step. This spawns a subagent of itself with a new session.

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

**Triggered by:** User command `"Start next chapter"` or `"Run P3-S1 for Chapter X"`

- **P3-S1-Brief**: Planner reads `instructions/chapter_outliner.md`. Reads all planning files. Generates the Chapter Brief and saves to `novel/chapters/briefs/chapter_X_brief.md`.
    - Next: `openclaw agent --agent {{agent_name}}_writer --session-id P3-S2-$(date +%s) --message "Run P3-S2: Draft Chapter X. Brief: [copy-paste brief here]"`
- **P3-S2-Draft**: Writer reads `instructions/prose_writer.md`. Writes `novel/chapters/drafts/chapter_X_draft.md`.
    - Next: `openclaw agent --agent {{agent_name}}_proofreader --session-id P3-S3-$(date +%s) --message "Run P3-S3 for Chapter X"`
- **P3-S3-Audit**: Proofreader reads `instructions/auditor.md`. Evaluates chapter for cliffhanger, continuity (World Bible), and quality (power feats, exposition).
    - If ALL pass: `openclaw agent --agent {{agent_name}}_writer --session-id P3-S4-$(date +%s) --message "Run P3-S4 for Chapter X"`
    - If ANY fail and retries < 3: Save failed draft to `novel/chapters/revisions/chapter_X_v[AttemptCount].md` AND save Audit Report to `novel/chapters/revisions/chapter_X_audit_v[AttemptCount].md`. Run `openclaw agent --agent {{agent_name}}_writer --session-id P3-S2-$(date +%s) --message "Rewrite Chapter X based on Audit Report in novel/chapters/revisions/chapter_X_audit_v[AttemptCount].md"`. Re-run P3-S3 on the new rewrite.
    - If 3 retries exhausted without a perfect pass: Proofreader compares original draft and all saved `v[N]` files in `revisions/`. Overwrites `novel/chapters/drafts/chapter_X_draft.md` with the highest-scoring version. Run `openclaw agent --agent {{agent_name}}_writer --session-id P3-S4-$(date +%s) --message "Run P3-S4 for Chapter X (Selected Best Fallback)"`.
- **P3-S4-Dialog**: Writer reads `instructions/prose_writer.md`. Reads `novel/chapters/drafts/chapter_X_draft.md`. Revises dialog and overwrites `novel/chapters/drafts/chapter_X_draft.md`.
    - Next: `openclaw agent --agent {{agent_name}}_proofreader --session-id P4-S1-$(date +%s) --message "Run P4-S1 for Chapter X"`
- **P4-S1-Proofread**: Proofreader reads `instructions/proofreader.md`. Reads `novel/chapters/drafts/chapter_X_draft.md`. Fixes grammar and outputs `novel/chapters/chapter_X_final.md`.
    - Next: Wakes up Coordinator stating "Chapter X is polished and ready."
