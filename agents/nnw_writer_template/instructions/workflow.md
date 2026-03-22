# Novel Generation Workflow

## 🚦 Role & Transition Rules

### 📥 1. Incoming Message (When you are woken)
When you receive a message, find its step in the workflow and check its `Agent:`:
- **If Agent is YOU:** Run it.
- **If Agent is NOT YOU:** Forward/Wake that agent using `openclaw agent --agent {{agent_name}}_[role] --message "[Step_Name]"`.

### 📤 2. Next Step Transition (When you finish)
When you finish a step, find the next step listed in its `Next:` field. Check THAT step's `Agent:`:
- **If Next Agent is YOU:** Use `sessions_spawn(task="Run [Step_Name]", cleanup="delete")`.
- **If Next Agent is NOT YOU:** Wake them using `openclaw agent --agent {{agent_name}}_[role] --message "Run [Step_Name]"`.

## Phase 1: World & Characters Planning

**Triggered by:** User command `"Start a new novel"` or `"Run [Step_Name]"`

- **P1-S1: World Building**:
    - **Agent:** {{agent_name}}_planner
    - **Trigger In:** `"Run World Building"`
    - **Action:** Planner follows `instructions/world_builder.md` and generates `novel/WORLD_BIBLE.md`.
    - **Next:** `"Run Character Profiling"`

- **P1-S2: Character Profiling**:
    - **Agent:** {{agent_name}}_planner
    - **Trigger In:** `"Run Character Profiling"`
    - **Action:** Planner follows `instructions/character_development.md` and generates `novel/CHARACTERS.md`.
    - **Next:** `"Run Plot Skeletons"`

- **P1-S3: Plot Skeletons**:
    - **Agent:** {{agent_name}}_planner
    - **Trigger In:** `"Run Plot Skeletons"`
    - **Action:** Planner follows `instructions/outline_planner.md` and generates `novel/OUTLINE.md`.
    - **Next:** `"Run Story Arcs"`

## Phase 2: Arcs & Foreshadowing

- **P2-S1: Story Arcs**:
    - **Agent:** {{agent_name}}_planner
    - **Trigger In:** `"Run Story Arcs"`
    - **Action:** Planner follows `instructions/story_arc_planner.md` and generates `novel/STORY_ARCS.md`.
    - **Next:** `"Run Foreshadowing"`

- **P2-S2: Foreshadowing**:
    - **Agent:** {{agent_name}}_planner
    - **Trigger In:** `"Run Foreshadowing"`
    - **Action:** Planner follows `instructions/foreshadowing_specialist.md` and generates `novel/FORESHADOWING.md`.
    - **Next:** `"Run Book Title"`

- **P2-S3: Book Title**:
    - **Agent:** {{agent_name}}_planner
    - **Trigger In:** `"Run Book Title"`
    - **Action:** Planner proposes book title, adds to `novel/METADATA.md`, and wakes Coordinator.

## Phase 3: Chapter Drafting & Audit

**Trigger:** User command `"Start next chapter"` or `"Run Briefing for Ch X"`.

**🚨 Hold Gate:** Do NOT start Ch X+1 until Ch X is COMPLETE. Auto-triggering forbidden.

- **P3-S1: Briefing**:
    - **Agent:** {{agent_name}}_planner
    - **Trigger In:** `"Generate Chapter Brief"`
    - **Prerequisite:** `novel/chapters/chapter_(X-1)_final.md` must exist except for the first chapter.
    - **Action:** Planner follows `instructions/chapter_outliner.md` and saves brief to `novel/chapters/briefs/chapter_X_brief.md`.
    - **Next:** `"Draft Chapter X"`

- **P3-S2: Prose Drafting**:
    - **Agent:** {{agent_name}}_writer
    - **Trigger In:** `"Draft Chapter X"`
    - **Action:** Writer follows `instructions/prose_writer.md` and writes `novel/chapters/drafts/chapter_X_draft.md`.
    - **Next:** `"/reasoning on\nAudit Chapter X"`

- **P3-S3: Quality Audit**:
    - **Agent:** {{agent_name}}_proofreader
    - **Trigger In:** `"/reasoning on\nAudit Chapter X"`
    - **Action:** Proofreader follows `instructions/auditor.md` and evaluates for style and quality.
    - **Outcome Pass:** `"Revise Dialog for Chapter X"`
    - **Outcome Fail (< 3 attempts):**
        - **Action:** Save audit artifacts `novel/chapters/revisions/chapter_X_vN.md` and `novel/chapters/audits/chapter_X_audit_vN.md`.
        - **Next:** `"Run Prose Revision using novel/chapters/audits/chapter_X_audit_vN.md"`
    - **Outcome Fail Cap (>= 3 attempts):**
        - **Action:** Overwrite `chapter_X_draft.md` with best revision.
        - **Next:** `"Revise Dialog for Chapter X (Fallback)"`

- **P3-S4: Prose Revision**:
    - **Agent:** {{agent_name}}_writer
    - **Trigger In:** `"Run Prose Revision using novel/chapters/audits/chapter_X_audit_vN.md"`
    - **Action:** Writer follows `instructions/prose_writer.md` and applies the specified audit report.
    - **Next:** `"/reasoning on\nAudit Chapter X"`

## Phase 4: Polish & Review

- **P4-S1: Dialog Polishing**:
    - **Agent:** {{agent_name}}_writer
    - **Trigger In:** `"Revise Dialog for Chapter X"`
    - **Action:** Writer follows `instructions/prose_writer.md` and revises dialog overwriting `novel/chapters/drafts/chapter_X_draft.md`.
    - **Next:** `"/reasoning off\nProofread Chapter X"`

- **P4-S2: Copy Editing**:
    - **Agent:** {{agent_name}}_proofreader
    - **Trigger In:** `"/reasoning off\nProofread Chapter X"`
    - **Action:** Proofreader follows `instructions/proofreader.md` and fixes grammar outputting `novel/chapters/chapter_X_final.md`.
    - **Complete means:** `novel/chapters/chapter_X_final.md` exists AND Coordinator is woken.
    - **Next:** `"Chapter X is COMPLETE"`

## Phase 5: Cleanup

- **P5-S1: Session Reset**:
    - **Agent:** {{agent_name}}
    - **Trigger In:** `"Chapter X is COMPLETE"`
    - **Cmds:**
      `openclaw agent --agent {{agent_name}}_planner --message "/new"`
      `openclaw agent --agent {{agent_name}}_writer --message "/new"`
      `openclaw agent --agent {{agent_name}}_proofreader --message "/new"`
      `openclaw agent --agent {{agent_name}} --message "/new"`
