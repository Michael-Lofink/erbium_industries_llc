---
type: navigation
audience: gm
aliases:
  - Settled Systems
---

# Worldbuilding Index

[[00 - Start Here|Home]] · [[Campaign/00 - Run the Campaign|Campaign]] · [[Starfinder 2e Rules/00 - Rules Index|Mechanics reference]]

## Setting foundations

- [[Worldbuilding/Foundations/Erbium Industries -- Settled Systems -- Setting Guide|Erbium Industries -- Settled Systems -- Setting Guide]]
- [[Worldbuilding/Foundations/Time in the Settled Systems|Time in the Settled Systems]]
- [[Worldbuilding/History/The Fall of Wander and the Rise of Erbium Industries|The Fall of Wander and the Rise of Erbium Industries]]
- [[Worldbuilding/Settled Systems Code/Settled Systems Administrative Code System|Settled Systems Administrative Code System]]
- [[Worldbuilding/Society and Economy/Erbium Credit Trust and Equipment Financing|Erbium Credit Trust and Equipment Financing]]

## Places

```dataview
LIST
FROM "Worldbuilding/Locations"
WHERE type != "navigation"
SORT file.name ASC
```

Campaign-specific locations, including The Last Grin and Fresh-Breath, are accessible here:

```dataview
LIST
FROM "Campaign/Locations"
WHERE type != "navigation"
SORT file.name ASC
```

Starmap data is indexed in [[Resources/00 - Resource Index|Resources]].

## People

```dataview
LIST
FROM "Worldbuilding/People"
WHERE type != "navigation"
SORT file.name ASC
```

Player character notes and scenes are in the [[Campaign/Party/00 - Party Index|Party Index]].

## Ancestries and character options

```dataview
TABLE WITHOUT ID file.link AS Note, file.folder AS Folder
FROM "Worldbuilding/Mechanics"
WHERE type != "navigation"
SORT file.name ASC
```

## Hazards and afflictions

```dataview
LIST
FROM "Worldbuilding/Hazards and Afflictions"
WHERE type != "navigation"
SORT file.name ASC
```

## Society, economy, and history

```dataview
LIST
FROM "Worldbuilding/Society and Economy"
WHERE type != "navigation"
SORT file.name ASC
```


```dataview
LIST
FROM "Worldbuilding/History"
WHERE type != "navigation"
SORT file.name ASC
```

## Administrative code

```dataview
LIST
FROM "Worldbuilding/Settled Systems Code"
WHERE type != "navigation"
SORT file.name ASC
```

## Writing and visual references

[[Resources/Art Direction/Erbium Campaign Art Style|Campaign art direction]] · [[Templates/Corporate Frontier Grit — Image Prompt Templates|Image prompt templates]] · [[Templates/00 - Template Index|Note templates]]
