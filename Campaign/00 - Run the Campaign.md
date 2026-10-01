---
type: navigation
audience: gm
---

# Run the Campaign

[[00 - Start Here|Home]] · [[Worldbuilding/00 - Worldbuilding Index|Worldbuilding]] · [[Starfinder 2e Rules/00 - Rules Index|Rules]]

## At the table

| Need | Open |
| --- | --- |
| Current preparation | [[Campaign/Sessions/Session 2|Session 2]] |
| Clock and recorded time | [[Campaign/System/Campaign Clock|Campaign Clock]] · [[Campaign/Campaign Timeline|Timeline]] |
| PES commands and hotkeys | [[Campaign/GM Notes/PES Timekeeping Toolkit|PES Timekeeping Toolkit]] |
| Previous session and continuity | [[Campaign/Sessions/Session 1|Session 1]] · [[Campaign/GM Notes/Erbium_Session_1_Assessment_Recap_Continuity|Assessment, recap, and GM continuity]] |
| Player characters and opening scenes | [[Campaign/Party/00 - Party Index|Party Index]] |
| Shared equipment and agreements | [[Campaign/Player Handouts/00 - Player Handouts Index|Player Handouts]] |

## Session 2 references

These links support the existing preparation. Outcomes and open questions remain in the session note.

- [[Campaign/Locations/Outside Settled Systems/The Last Grin/The Last Grin|The Last Grin]]
- [[Campaign/Locations/Outside Settled Systems/The Last Grin/Fresh-Breath|Fresh-Breath]]
- [[Starfinder 2e Rules/Creature/Level 2/Beast/Electrovore|Electrovore]]
- [[Starfinder 2e Rules/Actions/Analyze Environment|Analyze Environment]]
- [[Starfinder 2e Rules/Environment/Atmosphere/Nitrous-Oxide Atmosphere|Nitrous-Oxide Atmosphere]]
- [[Starfinder 2e Rules/Environment/Atmosphere/Thin Atmosphere|Thin Atmosphere]]
- [[Starfinder 2e Rules/Equipment/Armor/Environmental Protection|Environmental Protection]]
- [[Starfinder 2e Rules/Conditions/Broken|Broken]]

## Sessions

```dataview
TABLE session AS Session, stamp-status AS Status, stamp-planned-minutes AS Planned, stamp-actual-minutes AS Actual
FROM "Campaign/Sessions"
WHERE type = "session"
SORT session DESC
```

## Campaign locations

```dataview
LIST
FROM "Campaign/Locations"
WHERE type != "navigation"
SORT file.name ASC
```

## GM notes and table management

```dataview
LIST
FROM "Campaign/GM Notes"
WHERE type != "navigation"
SORT file.name ASC
```


```dataview
LIST
FROM "Campaign/Table Management"
WHERE type != "navigation"
SORT file.name ASC
```

## Campaign premise

[[Campaign/Plot Hook|Frontier Extraction Division recruitment pitch]]

OBS scenes and media are in `Campaign/OBS_ASSETS`; Discord records are indexed under [[Resources/00 - Resource Index|Resources]].
