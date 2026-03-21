# Novel Generation Workflow

## 🚨 Execution Constraints

- **P1/P2 (Planning): Single-Agent.** Use `sessions_spawn(cleanup="delete")` for sub-steps to save context. 
- **P3/P4 (Writing): Multi-Agent.** Use `openclaw agent` to wake the next role. **Never use `sessions_spawn` here.** Never skip steps.

## Phase 1 & 2: Novel Planning

**Triggered by:** User command `"Start a new novel"` or `"Run [Step_Name]"`

- **P1-S1: World Building**:
    - **Trigger In:** `"Run P1-S1: World Building"`

    - **Action:** Planner follows `instructions/world_builder.md` and generates `novel/WORLD_BIBLE.md`.

    - **Next:** `sessions_spawn(task="Run P1-S2: Character Profiling", cleanup="delete")`



- **P1-S2: Character Profiling**:
    - **Trigger In:** `"Run P1-S2: Character Profiling"`

    - **Action:** Planner follows `instructions/character_development.md` and generates `novel/CHARACTERS.md`.
    - **Next:** `sessions_spawn(task="Run P1-S3: Plot Skeletons", cleanup="delete")`



- **P1-S3: Plot Skeletons**:
    - **Trigger In:** `"Run P1-S3: Plot Skeletons"`

    - **Action:** Planner follows `instructions/outline_planner.md` and generates `novel/OUTLINE.md`.

    - **Next:** `sessions_spawn(task="Run P2-S1: Story Arcs", cleanup="delete")`



- **P2-S1: Story Arcs**:
    - **Trigger In:** `"Run P2-S1: Story Arcs"`

    - **Action:** Planner follows `instructions/story_arc_planner.md` and generates `novel/STORY_ARCS.md`.
    - **Next:** `sessions_spawn(task="Run P2-S2: Foreshadowing", cleanup="delete")`


- **P2-S2: Foreshadowing**:
    - **Trigger In:** `"Run P2-S2: Foreshadowing"`
    - **Action:** Planner follows `instructions/foreshadowing_specialist.md` and generates `novel/FORESHADOWING.md`.
    - **Next:** `sessions_spawn(task="Run P2-S3: Book Title", cleanup="delete")`



- **P2-S3: Book Title**:
    - **Trigger In:** `"Run P2-S3: Book Title"`

    - **Action:** Planner proposes book title, adds to `novel/METADATA.md`, and wakes Coordinator.


## Phase 3 & 4: Chapter Loop

**Trigger:** User command `"Start next chapter"` or `"Run Briefing for Ch X"`.
**🚨 Hold Gate:** Do NOT start Ch X+1 until Ch X is COMPLETE. Auto-triggering forbidden.

- **P3-S1: Briefing**:
    - **Trigger In:** `"Run P3-S1: Briefing"`
    - **Prerequisite:** `novel/chapters/chapter_(X-1)_final.md` must exist except for the first chapter.
    - **Action:** Planner follows `instructions/chapter_outliner.md` and saves brief to `novel/chapters/briefs/chapter_X_brief.md`.
    - **Next (Writer):**
        - **Payload:** `"Run P3-S2: Draft Chapter X"`
        - **Cmd:** `openclaw agent --agent {{agent_name}}_writer --message "{{payload}}"`


- **P3-S2: Prose Drafting**:
    - **Trigger In:** `"Run P3-S2: Draft Chapter X"`

    - **Action:** Writer follows `instructions/prose_writer.md` and writes `novel/chapters/drafts/chapter_X_draft.md`.

    - **Next (Proofreader):**
        - **Payload:** `"/reasoning on\nRun P3-S3: Audit Chapter X"`
        - **Cmd:** `openclaw agent --agent {{agent_name}}_proofreader --message "{{payload}}"`


- **P3-S3: Quality Audit**:
    - **Trigger In:** `"/reasoning on\nRun P3-S3: Audit Chapter X"`
    - **Action:** Proofreader follows `instructions/auditor.md` and evaluates for style and quality.

    - **Outcome Pass:**
        - **Action:** Proceed to Dialog Polishing.
        - **Payload:** `"Run P4-S1: Revise Dialog for Chapter X"`
        - **Cmd:** `openclaw agent --agent {{agent_name}}_writer --message "{{payload}}"`

    - **Outcome Fail (< 3 attempts):**
        - **Action:** Save `novel/chapters/revisions/chapter_X_vN.md` and `novel/chapters/audits/chapter_X_audit_vN.md`. Proceed to Prose Revision.
        - **Payload:** `"Run P3-S4: Prose Revision using novel/chapters/audits/chapter_X_audit_vN.md"`
        - **Cmd:** `openclaw agent --agent {{agent_name}}_writer --message "{{payload}}"`

    - **Outcome Fail Cap (>= 3 attempts fallback):**
        - **Action:** Overwrite `chapter_X_draft.md` with best revision. Proceed to Dialog Polishing.
        - **Payload:** `"Run P4-S1: Revise Dialog for Chapter X (Fallback)"`
        - **Cmd:** `openclaw agent --agent {{agent_name}}_writer --message "{{payload}}"`


- **P3-S4: Prose Revision**:
    - **Trigger In:** `"Run P3-S4: Prose Revision using novel/chapters/audits/chapter_X_audit_vN.md"`
    - **Action:** Writer follows `instructions/prose_writer.md` and applies the specified audit report.
    - **Next:**
        - **Payload:** `"/reasoning on\nRun P3-S3: Audit Chapter X"`
        - **Cmd:** `openclaw agent --agent {{agent_name}}_proofreader --message "{{payload}}"`



- **P4-S1: Dialog Polishing**:
    - **Trigger In:** `"Run P4-S1: Revise Dialog for Chapter X"`

    - **Action:** Writer follows `instructions/prose_writer.md` and revises dialog overwriting `novel/chapters/drafts/chapter_X_draft.md`.

    - **Next (Proofreader):**
        - **Payload:** `"/reasoning off\nRun P4-S2: Proofread Chapter X"`
        - **Cmd:** `openclaw agent --agent {{agent_name}}_proofreader --message "{{payload}}"`


- **P4-S2: Copy Editing**:
    - **Trigger In:** `"/reasoning off\nRun P4-S2: Proofread Chapter X"`

    - **Action:** Proofreader follows `instructions/proofreader.md` and fixes grammar outputting `novel/chapters/chapter_X_final.md`.

    - **Complete means:** `novel/chapters/chapter_X_final.md` exists AND Coordinator is woken.
    - **Next:** Wake Coordinator. Do NOT auto-trigger next chapter.
      - **Payload:** `"Chapter X is COMPLETE"`
      - **Cmd:** `openclaw agent --agent {{agent_name}}_coordinator --message "{{payload}}"`


- **P4-S3: Session Reset**:

    - **Trigger In:** `"Chapter X is COMPLETE"`

    - **Cmds:**
      `openclaw agent --agent {{agent_name}}_planner --message "/new"`
      `openclaw agent --agent {{agent_name}}_writer --message "/new"`
      `openclaw agent --agent {{agent_name}}_proofreader --message "/new"`
      `openclaw agent --agent {{agent_name}} --message "/new"`

