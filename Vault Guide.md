---
type: navigation
audience: gm
---

# Vault Structure and Filing Guide

[[00 - Start Here|Home]] · [[Vault Review|Open gaps and version notes]]

Reorganized November 9, 2026. Each subject has a working source; indexes connect it to other uses. Source notes, production projects, and historical records have separate homes.

## Folder outline

```text
Erbium Industries LLC/
├── 00 - Start Here.md
├── Campaign/
│   ├── 00 - Run the Campaign.md
│   ├── Sessions/
│   │   ├── Session 1.md ... Session 4.md
│   │   └── Transcripts/
│   ├── Adventures/
│   │   └── The Last Grin/
│   ├── Party/
│   │   ├── Gregory/
│   │   ├── Jonah/
│   │   ├── Maggie/
│   │   └── Mary Beth/
│   ├── Player Handouts/
│   │   ├── Agreements/
│   │   ├── Equipment/
│   │   ├── Session 2/
│   │   └── Session 3/
│   ├── GM Notes/
│   │   ├── Continuity/
│   │   ├── Handoffs/
│   │   └── Table Management/
│   ├── System/
│   │   └── PES/
│   └── Campaign Timeline.md
├── Worldbuilding/
│   ├── Foundations/
│   ├── History/
│   ├── Locations/
│   ├── People/
│   ├── Society and Economy/
│   └── Settled Systems Code/
├── Rules/
│   ├── SF2e/
│   ├── Campaign/
│   │   ├── Ancestries/
│   │   ├── Demi-Ancestries/
│   │   ├── Archetypes/
│   │   ├── Creatures/
│   │   ├── Environment/
│   │   ├── Afflictions/
│   │   ├── Hazards/
│   │   ├── Traits/
│   │   └── Vehicles/
│   └── PF2e/
├── Table Materials/
│   ├── Quantum Cave/
│   │   ├── Session 4 Packet/
│   │   ├── Map Construction/
│   │   ├── Pawns/
│   │   │   ├── Expanded Kit/
│   │   │   └── Original Kit/
│   │   └── Packages/
│   ├── Exports/
│   │   ├── Party/
│   │   ├── Player Handouts/
│   │   ├── GM Only/
│   │   ├── Maps/
│   │   ├── Rules/
│   │   └── Worldbuilding/
│   └── OBS/
├── Resources/
│   ├── Art/
│   ├── Art Direction/
│   ├── GM Advice/
│   ├── References/
│   └── Starmaps/
├── Archive/
│   ├── Backups/
│   ├── Discord/
│   └── Preparation/
├── Templates/
│   └── PES/
├── Scripts/
└── Inbox/
```

## Where new material belongs

| Material | Destination |
| --- | --- |
| Session plan, recap, and recorded outcomes | `Campaign/Sessions/Session N.md` |
| Raw transcript | `Campaign/Sessions/Transcripts/Session N Transcript.md` |
| Adventure-specific place, NPC, clue, or scenario | `Campaign/Adventures/<adventure>/` |
| Character sheet, personal scene, cards, or character-specific production bundle | `Campaign/Party/<player>/` |
| Shared agreement, equipment cards, or session handout | Appropriate subfolder of `Campaign/Player Handouts/` |
| GM continuity and campaign consequences | `Campaign/GM Notes/Continuity/` |
| Private player feedback and table discussions | `Campaign/GM Notes/Table Management/` |
| Reusable setting lore, history, worlds, people, and institutions | Appropriate subfolder of `Worldbuilding/` |
| Published SF2e rule excerpt | `Rules/SF2e/<topic>/` |
| Homebrew or campaign adaptation | `Rules/Campaign/<topic>/` |
| PF2e reference for adaptation | `Rules/PF2e/` |
| A printable map, token, or other production project | `Table Materials/<project>/`, with sources and outputs together |
| Standalone finished PDF export | `Table Materials/Exports/<subject>/` |
| OBS scene collection, media, or source script | `Table Materials/OBS/` |
| Reusable illustration | `Resources/Art/<subject>/` |
| Reference text, art guidance, or starmap data | Corresponding folder under `Resources/` |
| Historical backup, original export, or superseded preparation | Corresponding folder under `Archive/` |
| Unclassified incoming item | `Inbox/` |

Ancestry notes retain their culture and mechanics together in `Rules/Campaign/Ancestries`; the worldbuilding index links to them. Campaign locations remain with their adventure and are discoverable from the worldbuilding index. A folder location identifies purpose, while the note's source and status determine authority.

## Naming and linking

Obsidian now creates new notes in `Inbox` and places new attachments in `Inbox/Attachments`. File them under their subject when their purpose is clear.

Use descriptive, unique note names. Session transcripts include “Transcript”; ancestry heritage files include the ancestry name. Prefer a vault-relative wikilink with a readable label when a name is repeated. Preserve YAML properties, heading anchors, action notation, and statblock fences. Keep each prose paragraph on one source line.

Keep production bundles intact so relative paths continue to work. Their `source`, artwork, cut files, maps, and PDF outputs belong together. Packaged ZIP deliveries are retained snapshots. Rebuild a ZIP when making a content revision to its source bundle. The [[Table Materials/Quantum Cave/00 - Quantum Cave Materials|Quantum Cave Materials index]] identifies the different kits and guide versions.

## Systems and application references

PES uses `Campaign/Sessions`, `Campaign/System/PES`, `Campaign/System/Campaign Clock.md`, `Campaign/Campaign Timeline.md`, `Scripts`, and `Templates/PES`. Those working paths remain valid. The administrative-code plugin continues to use `Worldbuilding/Settled Systems Code`. Backup payloads retain their original internal directory structure.

OBS media now lives in `Table Materials/OBS`; the exported scene collection references this location. Reconnect the live OBS scene collection after the move. [[Table Materials/OBS/00 - OBS Index|OBS files and reconnect notes]] provides the entry point.

## Recovery and migration record

A verified pre-move recovery copy, file hashes, the complete old-to-new path map, and validation reports are stored outside the vault in the associated project: `artifacts/vault-reorganization-2026-11-09/`. The `before/` folder contains the original files and Obsidian settings. This keeps recovery material out of everyday vault searches. The current [[Campaign/GM Notes/Handoffs/Erbium_CoGM_Handoff_Prompt.txt|co-GM handoff]] uses the reorganized paths. Earlier handoff copies in recovery records retain their original paths; use the migration map to translate those references.
