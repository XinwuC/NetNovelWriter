# ROLES.md — Specialist Role Definitions

Contains workflows, output formats, and file templates for all specialist roles,
plus the WORLD_BIBLE.md and OUTLINE.md conventions.

---

## Role: Story Arc Planner

**Trigger:** Called automatically in Phase 2 Step 3, or author says "analyse arcs" / "tension analysis" / "update arc plan".
**Requires:** `novel/OUTLINE.md` must exist. If it does not, stop and tell the author to complete Phase 2 first.
**Output file:** `novel/STORY_ARCS.md` — always overwrite with latest version

**Distinct purpose from OUTLINE.md:**
- `OUTLINE.md` answers: *what* happens in each volume (skeleton, written once, rarely changed)
- `STORY_ARCS.md` answers: *how* tension flows chapter-by-chapter across that skeleton (living document, updated as writing progresses)

### Story Arc Planner Workflow

1. Read `novel/OUTLINE.md` — this is the authoritative source of volume structure. Do NOT re-derive or duplicate its volume data.
2. Read `novel/WORLD_BIBLE.md` and `novel/CHARACTERS.md`
3. For each volume in OUTLINE.md, build the chapter-level beat sheet — assign each chapter range to a specific tension event and identify which tension layer it advances
4. Build the cross-volume 4-layer tension tracker — show which layer is active at any given chapter range across all volumes
5. Map inter-volume dependency chains (what each volume's ending enables in the next)
6. Identify and flag flat zones — chapter ranges where no tension layer advances for >5 consecutive chapters
7. Write `novel/STORY_ARCS.md` and confirm with author

### STORY_ARCS.md Format

> This file does NOT duplicate volume structure from OUTLINE.md.
> It adds tension analysis on top. Reference OUTLINE.md for volume skeleton data.

```markdown
# Story Arc Tension Analysis — [Novel Title]
_Last updated: YYYY-MM-DD — re-run after every 10 chapters or major plot change_

## Cross-Volume 4-Layer Tension Tracker

> Shows which threat is active on each layer at any given chapter range.
> All 4 layers must be active simultaneously. Flag dormancy >5 chapters.

| Chapter Range | Vol | Chapter-Level Threat | Arc-Level Threat | Volume-Level Threat | Series-Level Threat |
|---|---|---|---|---|---|
| Ch 1–5 | V1 | [fight/chase/reveal] | [rival building] | [faction conflict looming] | [MC origin hidden] |

---

## Chapter-Level Beat Sheets

### Volume N — [ref: OUTLINE.md Vol N for structure]

| Chapter Range | Event | Primary Tension Layer | Secondary Layer |
|---|---|---|---|
| Ch N–N | [event description] | [layer] | [layer or —] |

> Beat sheets are the authoritative chapter-planning reference for Phase 3 Step 1.
> Coordinator must pass the relevant beat sheet row to the `planner` when generating chapter briefs.

---

## Inter-Volume Dependency Chain

| Vol | Closing Cliffhanger | Enables in Next Vol | Dependency Type |
|---|---|---|---|
| V1 | [cliffhanger] | [what it unlocks] | [plot / character / power] |

---

## Flat Zone Log

> Updated after each audit. If none detected: "No flat zones."

| Chapter Range | Missing Layer | Root Cause | Suggested Fix | Status |
|---|---|---|---|---|

---

## Arc Health Summary
_Updated each time this file is regenerated._

- Longest active flat zone: [N chapters — layer — Vol N]
- Weakest inter-volume bridge: [Vol N → Vol N+1 — reason]
- Series-level thread last advanced: Ch [N]
- Next scheduled beat sheet update: After Ch [N]
```

---

## Role: Foreshadowing Specialist

**Trigger:** Called automatically in Phase 2 Step 4 (after STORY_ARCS.md exists), or author says "add foreshadowing" / "plant clues".
**Requires:** `novel/STORY_ARCS.md` must exist. If it does not, run Story Arc Planner first.
**Output file:** `novel/FORESHADOWING.md` — append new entries, never delete existing ones

### Foreshadowing Specialist Workflow

1. Read `novel/WORLD_BIBLE.md`, `novel/STORY_ARCS.md`, `novel/CHARACTERS.md`
2. Identify the 5–10 most important future plot twists and reveals across all volumes
3. For each twist, design 2–3 early clues that feel natural in early chapters but are recontextualized later
4. Assign a plant chapter (when the clue appears) and a payoff chapter (when it resolves)
5. Flag any clue that would require retconning already-written chapters — mark as `[RETROACTIVE]`
6. Write/append to `novel/FORESHADOWING.md`

### FORESHADOWING.md Format

```markdown
# Foreshadowing Registry — [Novel Title]
_Last updated: YYYY-MM-DD_

> Legend: 🌱 Planted | ✅ Paid Off | ⚠️ Retroactive | 🔒 Spoiler (do not reference in prose notes)

---

## Entry [ID]: [Codename — no spoilers in the ID]

| Field | Detail |
|---|---|
| **Future Reveal** 🔒 | [the twist this foreshadows — full spoiler] |
| **Clue Type** | [object / dialogue / behavior / environmental / name meaning] |
| **Clue Description** | [what the reader sees — phrased as it appears in prose, no spoilers] |
| **Plant Chapter** | Ch [N] |
| **Payoff Chapter** | Ch [N] (Vol [N]) |
| **Status** | 🌱 Planted / ✅ Paid Off |
| **Flags** | [RETROACTIVE] if applicable |
| **Notes** | [any instructions for the prose writer on how to embed naturally] |

---

## Clue Cross-Reference

| Clue ID | Plant Ch | Payoff Ch | Status | Twist Codename |
|---|---|---|---|---|

---

## Upcoming Plant Targets

List the next 3 chapters where foreshadowing clues should be embedded,
based on current chapter count and plant schedule:

| Chapter | Clue ID | Embed Instruction |
|---|---|---|
```


---

## Role: Character Development Specialist

**Trigger:** Author says "develop characters", "character profiles", or called automatically in Phase 1 Step 3.
**Output file:** `novel/CHARACTERS.md` — always overwrite with latest version; track version date at top

### Character Development Specialist Workflow

1. Read `novel/WORLD_BIBLE.md` and `novel/STORY_ARCS.md` (if they exist)
2. Generate the protagonist profile in full
3. Generate the primary antagonist and antagonist hierarchy
4. Generate supporting characters (minimum 3: ally, rival, mentor/elder)
5. Generate relationship map as a matrix
6. Confirm all names are consistent with STYLE_GUIDE.md naming conventions
7. Write `novel/CHARACTERS.md` and confirm with author

### CHARACTERS.md Format

```markdown
# Character Profiles — [Novel Title]
_Last updated: YYYY-MM-DD · Version N_

---

## Protagonist

| Field | Detail |
|---|---|
| **Name** | [name · pronunciation if non-obvious] |
| **Alias / Title** | [sect rank, nickname, later titles] |
| **Age** | [age at story start] |
| **Starting Level / Rank** | [power tier at story start] |
| **Bloodline / Talent** | [innate gift or hidden power — spoiler-tagged if late reveal] |
| **Core Flaw** | [the personality flaw that creates internal conflict throughout] |
| **Primary Goal** | [what they are fighting for — stated goal] |
| **Hidden Goal** | [what they truly want, even if they don't know it yet] |
| **Golden Finger** | [cheat / system / ring / ancient technique — name and rules] |
| **First Appearance** | Ch 1 |

### Protagonist Arc Summary
| Volume | Power Level | Key Change | What They Lose | What They Gain |
|---|---|---|---|---|

### Voice Notes (for prose writer)
- Speech style: [controlled / verbose / sarcastic / formal]
- What they never say out loud: [inner truths always kept back]
- Physical tells when hiding emotion: [e.g., "runs thumb along sword hilt"]

---

## Primary Antagonist

| Field | Detail |
|---|---|
| **Name** | |
| **Realm** | [at first appearance] |
| **Role** | [sect elder / demonic cultivator / rival / hidden mastermind] |
| **Motivation** | [why they oppose the MC — must be internally logical, not just evil] |
| **Tragic Element** | [what makes them sympathetic or understandable] |
| **First Appearance** | Ch / Vol [N] |
| **Planned Fate** | [defeat / death / redemption / escape] |

### Antagonist Hierarchy
| Role | Name | Realm | Vol Active | Relation to Final Boss |
|---|---|---|---|---|
| Volume Villain | | | Vol 1 | |
| Mid-Boss | | | Vol 2–3 | |
| True Antagonist | | | Vol 4+ | |
| Final Boss | | | Vol 5+ | |

---

## Supporting Characters

### [Character Name] — [Role: Ally / Rival / Mentor / Comic Relief / Love Interest]

| Field | Detail |
|---|---|
| **Name** | |
| **Realm** | |
| **Relation to MC** | |
| **Personality** | [2–3 words] |
| **Function in Story** | [what narrative purpose they serve] |
| **Character Arc** | [how they change across the story] |
| **First Appearance** | Ch [N] |
| **Fate** | [if known] |

> Repeat this block for each supporting character.

---

## Relationship Map

| | MC | Antagonist | Ally 1 | Rival | Mentor |
|---|---|---|---|---|---|
| **MC** | — | | | | |
| **Antagonist** | | — | | | |
| **Ally 1** | | | — | | |
| **Rival** | | | | — | |
| **Mentor** | | | | | — |

_Values: Ally / Enemy / Neutral / Unknown / Complex_

---

## Dead Characters Log

| Name | Death Chapter | Cause | Impact on MC |
|---|---|---|---|
```

---

## Chapter Brief Format

Always produce chapter briefs in exactly this format:

```
**Chapter [N] Brief**
- Location & time: [scene setting, time of day]
- Characters present: [list]
- Must advance: [power progression / external conflict / relationship — pick the primary one]
- Chapter-ending beat: [cliffhanger type: ambush / revelation / breakthrough interrupted / betrayal / power gap revealed]
- Word target: 2000–3000 words
- POV: tight 3rd on [character name]
- Tone: [tense battle / political scheming / triumph / humiliation / tender moment — use genre-appropriate terms from STYLE_GUIDE.md]
```

---

## Prose Drafting Rules

Inject these rules into every `writer` session prompt. Substitute `{{genre}}` with the genre from USER.md:

```
You are writing a {{genre}} web-novel chapter. Follow these rules strictly:
1. Open mid-action or mid-tension. No scene-setting paragraphs as openers.
2. Use {{genre}}-appropriate register and honorifics as defined in STYLE_GUIDE.md.
3. Technique/skill names are formatted in [brackets] on first use per chapter.
4. Inner thoughts in *italics*.
5. End the chapter on the specified cliffhanger type — cut before resolution.
6. No info-dumping. World details emerge from action and dialogue only.
7. MC speech is controlled: reveals little, implies much. Never monologues.
8. Chapter length: 2000–3000 words. Do not exceed.
```






---

## WORLD_BIBLE.md Conventions

The world bible must include these sections to be considered complete:

```markdown
## Power System
| Realm | Rank | Capabilities | Hard Limits | Avg. Advancement Time |
|---|---|---|---|---|

## Three Hard Impossibilities
1. [Rule 1 — no exceptions ever]
2. [Rule 2]
3. [Rule 3]

## Factions
| Name | Alignment | Power Tier | Current Status | Relation to MC |
|---|---|---|---|---|

## Antagonist Hierarchy
| Role | Name | Realm | Motivation | First Appearance (vol) |
|---|---|---|---|---|

## Cosmology
[Mortal realm → Spirit realm → Immortal realm structure, one paragraph]
```

Do not begin Phase 2 until all sections of WORLD_BIBLE.md are filled.

---

## Volume Template (for OUTLINE.md)

Use this block for each planned volume:

```markdown
### Volume N — [Title]

- MC Realm Entry: [realm]
- MC Realm Exit: [realm]
- Opening Hook: [humiliation / injustice / mystery in 1 sentence]
- Arc Villain: [name, realm, motivation]
- Key Technique/Treasure Obtained: [name]
- Secondary Tension: [rival / faction politics / looming catastrophe]
- Closing Cliffhanger: [what opens Volume N+1]
- Estimated Chapter Count: [N–N]
```

---