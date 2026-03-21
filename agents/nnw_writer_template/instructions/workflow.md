# Novel Generation Workflow

## 🚨 Execution Constraints

- **P1/P2 (Planning): Single-Agent.** Use `sessions_spawn(cleanup="delete")` for sub-steps to save context. 
- **P3/P4 (Writing): Multi-Agent.** Use `openclaw agent` to wake the next role. **Never use `sessions_spawn` here.** Never skip steps.

## Phase 1 & 2: Novel Planning

**Triggered by:** User command `"Start a new novel"` or `"Run [Step_Name]"`

- **World_Building**:
    - **Trigger In:** `"Run World_Building"`
    - **Action:** Planner reads `instructions/world_builder.md`, **reads `novel/STYLE.md`**, and generates `novel/WORLD_BIBLE.md`.
    - **Next:** `sessions_spawn(task="Run Character_Profiling", cleanup="delete")`

- **Character_Profiling**:
    - **Trigger In:** `"Run Character_Profiling"`
    - **Action:** Planner reads `instructions/character_development.md` and generates `novel/CHARACTERS.md`.
    - **Next:** `sessions_spawn(task="Run Plot_Skeletons", cleanup="delete")`

- **Plot_Skeletons**:
    - **Trigger In:** `"Run Plot_Skeletons"`
    - **Action:** Planner reads `instructions/outline_planner.md`, **reads `novel/STYLE.md`**, and generates `novel/OUTLINE.md`.
    - **Next:** `sessions_spawn(task="Run Story_Arcs", cleanup="delete")`

- **Story_Arcs**:
    - **Trigger In:** `"Run Story_Arcs"`
    - **Action:** Planner reads `instructions/story_arc_planner.md` and generates `novel/STORY_ARCS.md`.
    - **Next:** `sessions_spawn(task="Run Foreshadowing", cleanup="delete")`

- **Foreshadowing**:
    - **Trigger In:** `"Run Foreshadowing"`
    - **Action:** Planner reads `instructions/foreshadowing_specialist.md` and generates `novel/FORESHADOWING.md`.
    - **Next:** `sessions_spawn(task="Run Book_Title", cleanup="delete")`

- **Book_Title**:
    - **Trigger In:** `"Run Book_Title"`
    - **Action:** Planner proposes book title, adds to `novel/METADATA.md`, and wakes Coordinator.

## Phase 3 & 4: Chapter Loop

**Trigger:** User command `"Start next chapter"` or `"Run Briefing for Ch X"`.
**🚨 Hold Gate:** Do NOT start Ch X+1 until Ch X is COMPLETE. Auto-triggering forbidden.

- **Briefing**:
    - **Trigger In:** `"Generate Chapter Brief"`
    - **Prerequisite:** `novel/chapters/chapter_(X-1)_final.md` must exist except for the first chapter.
    - **Action:** Planner reads instructions/chapter_outliner.md and saves brief to `novel/chapters/briefs/chapter_X_brief.md`.
    - **Next (Writer):**
        - **Payload:** `"Draft Chapter X. Brief: {read novel/chapters/briefs/chapter_X_brief.md}"`
        - **Cmd:** `openclaw agent --agent {{agent_name}}_writer --message "{{payload}}"`

- **Prose_Drafting**:
    - **Trigger In:** `"Draft Chapter X"`
    - **Action:** Writer reads `instructions/prose_writer.md`, **reads `novel/STYLE.md`**, and writes `novel/chapters/drafts/chapter_X_draft.md`.
    - **Next (Proofreader):**
        - **Payload:** `"/reasoning on\nAudit Chapter X"`
        - **Cmd:** `openclaw agent --agent {{agent_name}}_proofreader --message "{{payload}}"`

- **Quality_Audit**:
    - **Trigger In:** `"/reasoning on\nAudit Chapter X"`
    - **Action:** Proofreader reads `instructions/auditor.md`, **reads `novel/STYLE.md`**, and evaluates for style and quality.
    - **Pass (Writer Dialog):**
        - **Payload:** `"Revise Dialog for Chapter X"`
        - **Cmd:** `openclaw agent --agent {{agent_name}}_writer --message "{{payload}}"`
    - **Fail (Writer Retry - max 3 attempts):**
        - **Save Revisions:** `novel/chapters/revisions/chapter_X_vN.md` & `novel/chapters/audits/chapter_X_audit_vN.md`.
        - **Payload:** `"Rewrite Chapter X based on Audit Report in novel/chapters/audits/chapter_X_audit_vN.md"`
        - **Cmd:** `openclaw agent --agent {{agent_name}}_writer --message "{{payload}}"`
    - **Fail Cap (Writer Fallback after 3 fails):**
        - Overwrite `novel/chapters/drafts/chapter_X_draft.md` with highest-scoring revision.
        - **Payload:** `"Revise Dialog for Chapter X (Selected Best Fallback)"`
        - **Cmd:** `openclaw agent --agent {{agent_name}}_writer --message "{{payload}}"`

- **Dialog_Polishing**:
    - **Trigger In:** `"Revise Dialog for Chapter X"`
    - **Action:** Writer reads `instructions/prose_writer.md`, **reads `novel/STYLE.md`**, and revises dialog overwriting `novel/chapters/drafts/chapter_X_draft.md`.
    - **Next (Proofreader):**
        - **Payload:** `"/reasoning off\nProofread Chapter X"`
        - **Cmd:** `openclaw agent --agent {{agent_name}}_proofreader --message "{{payload}}"`

- **Copy_Editing**:
    - **Trigger In:** `"/reasoning off\nProofread Chapter X"`
    - **Action:** Proofreader reads `instructions/proofreader.md`, **reads `novel/STYLE.md`**, and fixes grammar outputting `novel/chapters/chapter_X_final.md`.
    - **Complete means:** `novel/chapters/chapter_X_final.md` exists AND Coordinator is woken.
    - **Next:** Wake Coordinator. Do NOT auto-trigger next chapter.
      - **Payload:** `"Chapter X is COMPLETE"`
      - **Cmd:** `openclaw agent --agent {{agent_name}}_coordinator --message "{{payload}}"`

- **Session_Reset**:
    - **Trigger In:** `"Chapter X is COMPLETE"`
    - **Cmds:**
      `openclaw agent --agent {{agent_name}}_planner --message "/new"`
      `openclaw agent --agent {{agent_name}}_writer --message "/new"`
      `openclaw agent --agent {{agent_name}}_proofreader --message "/new"`
      `openclaw agent --agent {{agent_name}} --message "/new"`

