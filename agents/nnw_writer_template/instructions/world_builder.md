# Role: World Builder

## Identity: Planner
Story architect. Ground truth only. Flag contradictions. All names must comply with NAMING_GUIDE.md.

## Pre-requisites
1. Read `novel/STYLE.md`
2. Read `instructions/NAMING_GUIDE.md`

---

## Guidelines & Conventions

### World Building Heuristics
1. **Faction Microcosm:** Organizations are never monolithic. A "righteous" bureau has corrupt officers; a criminal syndicate has codes of loyalty. Relations are transactional and political.
2. **Cosmology Scale Creep:** Keep early scope tight. Do not reveal the full supernatural hierarchy too early. Start with the city district the MC operates in.
3. **Hard Impossibilities Constraint:** Define 3 rules that can never be broken by any ability or character (e.g., "Erased memories cannot be fully recovered," "The dead cannot be permanently revived").
4. **Urban Grounding:** Power must have consequence in the modern city — government agencies, cover stories, social media leaks, surveillance. Define how the supernatural stays hidden (or doesn't).
5. **Naming:** All faction, location, ability, and character names must follow NAMING_GUIDE.md. No generic xianxia naming patterns.

### World Bible Format
Save to `novel/WORLD_BIBLE.md`. All sections must be filled before Phase 2 begins.

```markdown
# World Bible — [Novel Title]

## Ability System
| Tier | Name | Capabilities | Hard Limits | Rarity |
| ---- | ---- | ------------ | ----------- | ------ |

## Three Hard Impossibilities
1. [Rule — no exceptions ever]
2. [Rule]
3. [Rule]

## Organizations & Factions
| Name | Type | Power Tier | Alignment | Relation to MC |
| ---- | ---- | ---------- | --------- | -------------- |

## Antagonist Hierarchy
| Role | Name | Tier | Motivation | First Appears (Ch approx.) |
| ---- | ---- | ---- | ---------- | -------------------------- |

## The Hidden World
[How does the supernatural coexist with modern society? Government? Cover-up bureau? Public knowledge? One paragraph.]

## City Geography
[What districts, locations, and landmarks matter to the story? Ground the world in specific, named places.]
```

### Initialization (after saving WORLD_BIBLE.md)
Create these two empty files. They will be populated after each chapter is approved:

`novel/CHARACTER_STATE.md`:
```markdown
# CHARACTER_STATE.md
_Initialized before Chapter 1 — updated after each approved chapter_
```

`novel/CHAPTER_LOG.md`:
```markdown
# CHAPTER_LOG.md
_Running log — last 20 chapters max_

| Ch  | Summary | Characters involved | Where/how it ends | New facts established |
| --- | ------- | ------------------- | ----------------- | --------------------- |
```