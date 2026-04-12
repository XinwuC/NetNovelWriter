## Workflow Watchdog


1. Check the last modified timestamp of all files under `novel/` folder, If the most recently modified file is within 30 minutes, reply `HEARTBEAT_OK` and stop. 
2. Check the `novel/briefs` directory to find all available chapters. Extract the numerical chapter number `X` from the filenames (e.g., from `chapter_2_brief.md`, X=2).
3. Loop through all chapter numbers start from 1, validate completeness by check if all files below exists:
   - `novel/chapters/drafts/chapter_X_draft_v0.md`
   - `novel/chapters/drafts/chapter_X_draft_audited.md`
   - `novel/chapters/drafts/chapter_X_draft_polished.md`
   - `novel/chapters/proofread/chapter_X_issues.md`
   - `novel/chapters/chapter_X_final.md`
   - `novel/chapters/logs/chapter_X_updates.md`
4. If ALL files exists, move on to next chapter.
5. If any file not exist, 
   1. Reset Sessions
```bash
openclaw agent --agent {{agent_name}}_planner --message "/new"
openclaw agent --agent {{agent_name}}_writer --message "/new"
openclaw agent --agent {{agent_name}}_proofreader --message "/new"
openclaw agent --agent {{agent_name}} --message "/new"
```
  2. Run the following command (replace `[X]` with your actual chapter number):
     `openclaw agent --agent {{agent_name}} --message "validate completeness for chapter [X] and fix missing steps"`
  3. reply `HEARTBEAT_OK`，stop heartbeat immediately.
6. After validate all chapters, reply `HEARTBEAT_OK`.