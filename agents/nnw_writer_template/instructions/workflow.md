# Novel Generation Workflow

## Notify <agent_name> with <message>
- bash: `openclaw agent --agent <agent_name> --message "<message>" --no-wait`
- **never use `sessions_spawn` for notification**

---

## Phase 1: World & Characters

- **P1-S1: World_Building**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `instructions/world_builder.md` → `novel/WORLD_BIBLE.md` + initialize `novel/CHARACTER_STATE.md` + `novel/CHAPTER_LOG.md`
  - Next: notify `{{agent_name}}` with message `run Character_Profiling`

- **P1-S2: Character_Profiling**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `instructions/character_development.md` → `novel/CHARACTERS.md`
  - Next: notify `{{agent_name}}` with message `run Plot_Skeletons`

- **P1-S3: Plot_Skeletons**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `instructions/outline_planner.md` → `novel/OUTLINE.md`
  - Next: notify  `{{agent_name}}` with message `run Story_Arcs`

---

## Phase 2: Arcs & Foreshadowing

- **P2-S1: Story_Arcs**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `instructions/story_arc_planner.md` → `novel/STORY_ARCS.md`
  - Next: notify `{{agent_name}}` with message `run Foreshadowing`

- **P2-S2: Foreshadowing**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `instructions/foreshadowing_specialist.md` → `novel/FORESHADOWING.md`
  - Next: notify `{{agent_name}}` with message `run Book_Title`

- **P2-S3: Book_Title**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `instructions/book_title.md` → `novel/METADATA.md`
  - Next: notify `{{agent_name}}` with message `"Phase 1+2 complete"`

---

## Phase 3: Chapter Drafting & Audit

> 🚨 Hold Gate: do NOT start Ch X+1 until `novel/chapters/chapter_X_final.md` exists. Auto-triggering forbidden.

- **P3-S1: Chapter_Brief**
  - Agent: `{{agent_name}}_planner`
  - Prerequisite: `novel/chapters/chapter_(X-1)_final.md` exists (skip for Ch 1)
  - Action: Follow `instructions/chapter_outliner.md` → `novel/chapters/briefs/chapter_X_brief.md`
  - Next: notify `{{agent_name}}` with message `run Prose_Draft`

- **P3-S2: Prose_Draft**
  - Agent: `{{agent_name}}_writer`
  - Action: Follow `instructions/prose_writer.md` → `novel/chapters/drafts/chapter_X_draft_v0.md`
  - Next: notify `{{agent_name}}` with message `"Audit novel/chapters/drafts/chapter_X_draft_v0.md"`

- **P3-S3: Audit_and_Revise**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `Audit_and_Revise` step in `instructions/planner_workflow.md`
  - Next:
    - Audit **Passed**: -> `novel/chapters/drafts/chapter_X_draft_audited.md`
    - Audit **Failed**: Run `Prose_Revision`

 - **P3-S4: Prose_Revision**
    - Agent: `{{agent_name}}_writer`
    - Action: 
      - **If `novel/chapters/drafts/chapter_X_draft_audited.md` exists**: skip this step and move on to next
      - **Otherwise**: Follow `instructions/prose_reviser.md` to create `novel/chapters/drafts/chapter_X_draft_v[attempt+1].md`.
    - Next: notify `{{agent_name}}` with message `"Audit revised draft: novel/chapters/drafts/chapter_X_draft_v[attempt+1].md"`

---

## Phase 4: Polish

- **P4-S1: Dialog_Polish**
  - Agent: `{{agent_name}}_writer`
  - Action: Follow `instructions/prose_dialog_polisher.md` → `novel/chapters/drafts/chapter_X_draft_polished.md`
  - Next: notify `{{agent_name}}` with message `run Copy_Edit`

- **P4-S2: Copy_Edit**
  - Agent: `{{agent_name}}_proofreader`
  - Action: Follow `instructions/proofreader.md` → `novel/chapters/chapter_X_final.md`
  - Next: notify `{{agent_name}}` with message `run State_Update`

- **P4-S3: State_Update**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `instructions/state_updater.md` → update `novel/CHARACTER_STATE.md` + `novel/CHAPTER_LOG.md` + `novel/FORESHADOWING.md`
  - Next: notify `{{agent_name}}` with message `"Chapter X is COMPLETE"`


---

## Supporting Steps (on-demand)
- **Story_Arcs_Update**
  - Agent: `{{agent_name}}_planner`
  - Trigger: every 10 approved chapters, or coordinator sends "Update Story Arcs"
  - Action: Follow `instructions/story_arc_planner.md` → overwrite `novel/STORY_ARCS.md`
  - Next: notify `{{agent_name}}` with message `"Story_Arcs updated"`
