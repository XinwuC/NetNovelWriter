# Novel Generation Workflow

The pipeline is fully automated and self-delegating. To prevent context explosion, agents MUST use `openclaw agent` with a strictly fresh session ID via `$(date +%s)` to advance the state.

## Phase 1 & 2: Novel Planning

**Triggered by:** User command `"Start a new novel"` or `"Run P[X]-S[X]"`

- **P1-S1-WorldBible**: Planner reads `PROMPTS.md -> System Prompt: Planner` & `roles.md -> WORLD_BIBLE.md Conventions`. Generates `novel/WORLD_BIBLE.md`.
    - Next: `openclaw agent --agent {{agent_name}}_planner --session-id P1-S2-$(date +%s) --message "Run P1-S2"`
- **P1-S2-Characters**: Planner reads `PROMPTS.md -> System Prompt: Planner` & `roles.md -> Character Development Specialist` & `WORLD_BIBLE.md`. Generates `novel/characters.md`.
    - Next: `openclaw agent --agent {{agent_name}}_planner --session-id P2-S1-$(date +%s) --message "Run P2-S1"`
- **P2-S1-Outline**: Planner reads `PROMPTS.md -> System Prompt: Planner` & `roles.md -> Volume Template`. Reads `WORLD_BIBLE.md` and `characters.md`. Generates `novel/OUTLINE.md`.
    - Next: `openclaw agent --agent {{agent_name}}_planner --session-id P2-S2-$(date +%s) --message "Run P2-S2"`
- **P2-S2-StoryArcs**: Planner reads `PROMPTS.md -> System Prompt: Planner` & `roles.md -> Story Arc Planner`. Reads all previous files. Generates `novel/story_arcs.md`.
    - Next: `openclaw agent --agent {{agent_name}}_planner --session-id P2-S3-$(date +%s) --message "Run P2-S3"`
- **P2-S3-Foreshadowing**: Planner reads `PROMPTS.md -> System Prompt: Planner` & `roles.md -> Foreshadowing Specialist`. Reads all previous files. Generates `novel/foreshadowing.md`.
    - Next: `openclaw agent --agent {{agent_name}}_planner --session-id P2-S4-$(date +%s) --message "Run P2-S4"`
- **P2-S4-Title**: Planner proposes book title, adds to `novel/metadata.md`, and wakes Coordinator stating "Novel Planning complete."

## Phase 3 & 4: Chapter Loop

**Triggered by:** User command `"Start next chapter"` or `"Run P3-S1 for Chapter X"`

- **P3-S1-Brief**: Planner reads `PROMPTS.md -> System Prompt: Planner` & `roles.md -> Chapter Brief Format`. Reads all planning files. Generates the Chapter Brief inline.
    - Next: `openclaw agent --agent {{agent_name}}_writer --session-id P3-S2-$(date +%s) --message "Run P3-S2: Draft Chapter X. Brief: [copy-paste brief here]"`
- **P3-S2-Draft**: Writer reads `PROMPTS.md -> System Prompt: Prose Writer` & `roles.md -> Prose Drafting Rules`. Writes `novel/chapter_X_draft.md`.
    - Next: `openclaw agent --agent {{agent_name}}_writer --session-id P3-S3-$(date +%s) --message "Run P3-S3 for Chapter X"`
- **P3-S3-Dialog**: Writer reads `PROMPTS.md -> System Prompt: Prose Writer`. Reads `chapter_X_draft.md`. Revises dialog and overwrites `novel/chapter_X_draft.md`.
    - Next: `openclaw agent --agent {{agent_name}}_proofreader --session-id P4-S1-$(date +%s) --message "Run P4-S1 for Chapter X"`
- **P4-S1-Proofread**: Proofreader reads `PROMPTS.md -> System Prompt: Proofreader`. Reads `novel/chapter_X_draft.md`. Fixes grammar and outputs `novel/chapter_X_final.md`.
    - Next: Wakes up Coordinator stating "Chapter X is polished and ready."
