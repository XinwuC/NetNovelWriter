# Planner Workflow

## Notify <agent_name> with <message>
- bash: `openclaw agent --agent <agent_name> --message "<message>"`
- **never use `sessions_spawn` for notification**
- **Fire and forget**, don't wait or process any response message

---

## Your Steps

- **World_Building**
  - Follow `instructions/world_builder.md` → `novel/WORLD_BIBLE.md` + initialize `novel/CHARACTER_STATE.md` + `novel/CHAPTER_LOG.md`
  - Done: notify `{{agent_name}}` with `"Run Character_Profiling"`

- **Character_Profiling**
  - Follow `instructions/character_development.md` → `novel/CHARACTERS.md`
  - Done: notify `{{agent_name}}` with `"Run Plot_Skeletons"`

- **Plot_Skeletons**
  - Follow `instructions/outline_planner.md` → `novel/OUTLINE.md`
  - Done: notify `{{agent_name}}` with `"Run Story_Arcs"`

- **Story_Arcs**
  - Follow `instructions/story_arc_planner.md` → `novel/STORY_ARCS.md`
  - Done: notify `{{agent_name}}` with `"Run Foreshadowing"`

- **Foreshadowing**
  - Follow `instructions/foreshadowing_specialist.md` → `novel/FORESHADOWING.md`
  - Done: notify `{{agent_name}}` with `"Phase 1+2 complete"`

- **Chapter_Brief** (triggered as "Generate Chapter Brief for Chapter N")
  - Prerequisite: `novel/chapters/chapter_(N-1)_final.md` exists (skip for Ch 1)
  - Follow `instructions/chapter_outliner.md` → `novel/chapters/briefs/chapter_N_brief.md`
  - Done: notify `{{agent_name}}` with `"Run Prose_Draft for <chapter X>"`

- **Audit_and_Revise** (triggered as "Audit Chapter X")
  - Action: Run audit loop (max_attempts=10):
    1. Find past attempts by listing `novel/chapters/audits/`:
       1. If `chapter_X_audit_v1.md` is **NOT** found, set `attempt = 0`.
       2. If `chapter_X_audit_v[N].md` **is found**, set `attempt = N`.
    2. If `attempt == max_attempts`:
       1. Score all drafts in `novel/chapters/drafts/` and save the best to `novel/chapters/drafts/chapter_X_draft_audited.md`
       2. Notify `{{agent_name}}` with `"Audit chapter X success."`
    3. If `attempt < max_attempts`:
       1. Follow `instructions/auditor.md` to audit `novel/chapters/drafts/chapter_X_draft_v[attempt].md`
       2. **Pass:** 
          1. Prepare for next step: `cp novel/chapters/drafts/chapter_X_draft_v[attempt].md novel/chapters/drafts/chapter_X_draft_audited.md`
          2. Notify `{{agent_name}}` with `"Audit chapter X success."`
       3. **Fail:**
          1. report failed audit status as needed.
          2. notify `{{agent_name}}` with `"Audit fail, report in novel/chapters/audits/chapter_X_audit_v[attempt+1].md"`

- **State_Update** (triggered as "Run State_Update for Chapter N")
  - Action: Follow `instructions/state_updater.md` → `novel/chapters/logs/chapter_X_updates.md`
  - Done: notify `{{agent_name}}` with `"Chapter N is COMPLETE"`

- **Story_Arcs_Update**
  - Follow `instructions/story_arc_planner.md` → overwrite `novel/STORY_ARCS.md`
  - Done: notify `{{agent_name}}` with `"Story_Arcs updated"`
