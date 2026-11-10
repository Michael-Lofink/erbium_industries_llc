---
type: navigation
audience: gm
---

# Run the Campaign

[[00 - Start Here|Home]] · [[Worldbuilding/00 - Worldbuilding Index|Worldbuilding]] · [[Rules/00 - Rules Index|Rules]] · [[Table Materials/00 - Table Materials Index|Table materials]]

## At the table

| Need | Open |
| --- | --- |
| Current preparation | [[Campaign/Sessions/Session 4\|Session 4]] |
| Last played session | [[Campaign/Sessions/Session 3\|Session 3]] |
| Current adventure | [[Campaign/Adventures/The Last Grin/00 - The Last Grin\|The Last Grin and Fresh-Breath]] |
| Cave guide and physical pieces | [[Table Materials/Quantum Cave/00 - Quantum Cave Materials\|Quantum Cave Materials]] |
| Clock and recorded time | [[Campaign/System/Campaign Clock\|Campaign Clock]] · [[Campaign/Campaign Timeline\|Timeline]] |
| Timekeeping commands | [[Campaign/System/PES Timekeeping Toolkit\|PES Timekeeping Toolkit]] |
| Characters and personal scenes | [[Campaign/Party/00 - Party Index\|Party]] |
| Agreements and shared cards | [[Campaign/Player Handouts/00 - Player Handouts Index\|Player handouts]] |
| General house rules | [[Rules/Campaign/General Play homebrew\|General Play homebrew]] |
| Continuity and private table matters | [[Campaign/GM Notes/00 - GM Index\|GM notes]] |

## Sessions

```dataview
TABLE session AS Session, stamp-status AS Status, stamp-planned-minutes AS Planned, stamp-actual-minutes AS Actual
FROM "Campaign/Sessions"
WHERE type = "session"
SORT session DESC
```

[[Campaign/Sessions/00 - Session Index|Session notes and matching transcripts]]

## Adventures

```dataview
LIST
FROM "Campaign/Adventures"
WHERE type != "navigation"
SORT file.name ASC
```

## Campaign premise

[[Campaign/GM Notes/Frontier Extraction Recruitment|Frontier Extraction Division recruitment pitch]]
