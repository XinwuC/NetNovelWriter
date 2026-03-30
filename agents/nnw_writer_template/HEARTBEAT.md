## Workflow Watchdog


1. Check the last modified timestamp of all files under `novel/` folder, If the most recently modified file is within 30 minutes, reply `HEARTBEAT_OK` and stop.
2. Check the `novel/briefs` directory to find all available chapters. Extract the numerical chapter number `X` from the filenames (e.g., from `chapter_2_brief.md`, X=2).
3. For each chapter number `X`, check if the file `novel/logs/chapter_{X}_updates.md` exists, and make a list of chapters that DO NOT have this updates file.
4. If ALL chapters have their `updates.md` file, reply `HEARTBEAT_OK` and stop.
5. Find the **lowest** chapter number `X` from your list of incomplete chapters.
6. For this specific chapter `X`, find all files within the `novel/` directory (and its subdirectories) that contain `chapter_{X}_` in their filename. **Critically: ensure your search exactly matches the number so that `chapter_1_` does not accidentally match `chapter_10_`.**
7. Check the last modified timestamp of all those matching files.
8. If the most recently modified file is OLDER than 30 minutes:
   - Reset Sessions
```bash
openclaw agent --agent {{agent_name}}_planner --message "/new"
openclaw agent --agent {{agent_name}}_writer --message "/new"
openclaw agent --agent {{agent_name}}_proofreader --message "/new"
openclaw agent --agent {{agent_name}} --message "/new"
```
   - Run the following command (replace `[X]` with your actual chapter number):
     `openclaw agent --agent {{agent_name}} --message "check progress for chapter [X] and resume automatically"`
   - Stop heartbeat immediately.
9. If the most recently modified file was updated LESS than 30 minutes ago, move to the NEXT lowest chapter number `X` on your incomplete list, and repeat steps 5-8. If no chapters are left, reply `HEARTBEAT_OK`.