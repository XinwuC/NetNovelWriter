# Novel Generation Workflow

> Step registry only. Coordinator reads `Agent:` to dispatch. Agents read `Next:` to chain.
> Phase 1–2: planner self-chains all steps without waking coordinator between them.

---

## Phase 1: World & Characters

- **P1-S1: World_Building**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `instructions/world_builder.md` → `novel/WORLD_BIBLE.md`
  - Next: `Character_Profiling`

- **P1-S2: Character_Profiling**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `instructions/character_development.md` → `novel/CHARACTERS.md`
  - Next: `Plot_Skeletons`

- **P1-S3: Plot_Skeletons**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `instructions/outline_planner.md` → `novel/OUTLINE.md`
  - Next: `Story_Arcs`

---

## Phase 2: Arcs & Foreshadowing

- **P2-S1: Story_Arcs**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `instructions/story_arc_planner.md` → `novel/STORY_ARCS.md`
  - Next: `Foreshadowing`

- **P2-S2: Foreshadowing**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `instructions/foreshadowing_specialist.md` → `novel/FORESHADOWING.md`
  - Next: `Book_Title`

- **P2-S3: Book_Title**
  - Agent: `{{agent_name}}_planner`
  - Action: Follow `instructions/book_title.md` → `novel/METADATA.md`
  - Next: notify coordinator `"Phase 1+2 complete"`

---

## Phase 3: Chapter Drafting & Audit

> 🚨 Hold Gate: do NOT start Ch X+1 until `novel/chapters/chapter_X_final.md` exists. Auto-triggering forbidden.

- **P3-S1: Chapter_Brief**
  - Agent: `{{agent_name}}_planner`
  - Prerequisite: `novel/chapters/chapter_(X-1)_final.md` exists (skip for Ch 1)
  - Action: Follow `instructions/chapter_outliner.md` → `novel/chapters/briefs/chapter_X_brief.md`
  - Next: `Prose_Draft`

- **P3-S2: Prose_Draft**
  - Agent: `{{agent_name}}_writer`
  - Action: Follow `instructions/prose_writer.md` → `novel/chapters/drafts/chapter_X_draft.md`
  - Next: `Audit_and_Revise` with message `"Audit novel/chapters/drafts/chapter_X_draft.md"`

- **P3-S3: Audit_and_Revise**
  - Agent: `{{agent_name}}_planner`
  - Action: Run audit loop (max 3 attempts):
    1. Find past attempts by listing `novel/chapters/revisions/`:
       1. If `chapter_X_v1.md` is **NOT** found, set `attempt = 0`.
       2. If `chapter_X_v[N].md` **is found**, set `attempt = N`.
    2. If `attempt == 3`:
       1. Score all revisions in `novel/chapters/revisions/` and copy the best to `novel/chapters/drafts/chapter_X_draft.md`
       2. Proceed to  `Dialog_Polish`
    3. If `attempt < 3`:
       1. Follow `instructions/auditor.md` to audit `novel/chapters/drafts/chapter_X_draft.md`
       2. **Pass:** proceed to  `Dialog_Polish`
       3. **Fail:** 
          1. copy `novel/chapters/drafts/chapter_X_draft.md` to `novel/chapters/revisions/chapter_X_v[attempt+1].md`
          2. save audit to `novel/chapters/audits/chapter_X_audit_v[attempt+1].md` 
          3. wake writer: `openclaw agent --agent {{agent_name}}_writer --message "Run Prose_Revision using novel/chapters/audits/chapter_X_audit_v[attempt+1].md"` 
   
 - **P3-S4: Prose_Revision**
    - Agent: `{{agent_name}}_writer`
    - Action: Follow `instructions/prose_reviser.md` using the audit file specified in trigger message
    - Next: `Audit_and_Revise` with message `"Audit novel/chapters/drafts/chapter_X_draft.md"`
   
---

## Phase 4: Polish

- **P4-S1: Dialog_Polish**
  - Agent: `{{agent_name}}_writer`
  - Action: Follow `instructions/prose_dialog_polisher.md` → overwrite `novel/chapters/drafts/chapter_X_draft.md`
  - Next: `Copy_Edit`

- **P4-S2: Copy_Edit**
  - Agent: `{{agent_name}}_proofreader`
  - Action: Follow `instructions/proofreader.md` → `novel/chapters/chapter_X_final.md`
  - Next: notify coordinator `openclaw agent --agent {{agent_name}} --message "Chapter X is COMPLETE"`
