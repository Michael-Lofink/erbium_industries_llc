---
type: session
session: 1
stamp-start-lapse: 29
stamp-start-minute: 8472119
elapsed-minutes: 240
---

# Session 1

## Session Clock

```dataviewjs
const session = dv.current();
const clock = dv.page("Campaign/System/Campaign Clock");

if (!clock) {
    dv.paragraph(
        "> [!failure] Campaign Clock not found\n" +
        "> Confirm that the clock is located at `Campaign/System/Campaign Clock.md`."
    );
} else {
    const limit = Number(clock["lapse-size"]);
    const startLapse = Number(session["stamp-start-lapse"]);
    const startMinute = Number(session["stamp-start-minute"]);
    const elapsed = Number(session["elapsed-minutes"] ?? 0);

    if (
        !Number.isInteger(limit) ||
        limit <= 0 ||
        !Number.isInteger(startLapse) ||
        !Number.isInteger(startMinute) ||
        !Number.isInteger(elapsed)
    ) {
        dv.paragraph(
            "> [!failure] Invalid Session Clock\n" +
            "> Check the session clock properties."
        );
    } else {
        const total = startMinute + elapsed;
        const endLapse = startLapse + Math.floor(total / limit);
        const endMinute = total % limit;
        const width = String(limit - 1).length;

        const start =
            `${startLapse}:${String(startMinute).padStart(width, "0")} PES`;

        const end =
            `${endLapse}:${String(endMinute).padStart(width, "0")} PES`;

        dv.table(
            ["Start Stamp", "Elapsed", "End Stamp"],
            [[start, `${elapsed} minutes`, end]]
        );
    }
}
```

# Outline
> Scenes

> 	Mary Beth
> 	Jonah
> 	Maggie
> 	Gregory
> 	Opening

> Enter frontier space (personal relays to stay on-stamp)
> Their ship gets shot down, forcibly enters orbit of astral body (Crash landing)
> Everybody but the Player Characters die. probably. (Objective find a way back home)
> Dun dun DUUUUUUH


# Opening Scene
We begin in darkness. Gradually, points of light resolve into stars, and as we draw closer, we find inhabited worlds scattered among them. On each, people look up into a sky they have no means of crossing.

Then, across worlds that have never spoken to one another, people begin to have the same dream. They see unfamiliar stars, other peoples, and a way to reach them. They wake with knowledge they have never learned, and begin building.

We pass through a workshop where handwritten calculations cover the walls. Workers guide an engine into its housing, checking connections against diagrams spread across the floor. Above their world, a vessel makes its first passage into the Drift.

Those who received the Star Dream became known as the Elect. Their ships found one another, and the first intersystem trade routes followed. Every engine required erbium, element sixty-eight, and the richest deposits ever discovered lay beneath the surface of a world called Wander.

Below us now, freight vessels crowd Wander’s orbital ports. On the surface, rail lines connect sprawling cities to excavation sites, where loaded containers emerge from shafts sunk deep into the crust. Erbium Industries brought those operations under a single administration, supplying an expanding civilization.

The image changes. A rail line hangs broken above a collapsed tunnel. Ash falls across a crowded departure platform, where families hold their luggage against their chests as company personnel check names against a manifest.

The geological disaster devastated Wander. Millions were displaced, and the governments dependent on its erbium reserves faced the loss of intersystem travel. Erbium’s surviving ships carried refugees to other worlds, while its relays coordinated the response. The company received emergency authority over the remaining supply.

That authority became permanent.

We move through a station concourse. A worker checks a housing deduction on her comm unit while a queue forms outside a clinic. Above them, a recruitment display shows a survey team stepping onto an unfamiliar planet.

Today, employment with Erbium can provide a home, medical care, and passage between worlds. Frontier service offers opportunities to those willing to leave the Settled Systems behind. Expeditions need technicians and surveyors, with crews to operate their ships and personnel to secure their claims. The Great Volunteering helps fill the vacancies.

Beyond the station, a transport is already underway. Its hull bears the marks of repeated repairs, with fresh paint around a replaced panel and dark exhaust staining near the engines. Beside its docking collar sits the emblem of Erbium Industries. The ship begins to stretch impossibly while vibrant purple and pinks burn against the exterior hull as the ship escapes into the drift.

[Start “Levitating.”]

Music plays as we pass inside. In the cargo compartment, restraint straps tremble against stacked containers. Farther along, someone in the mess holds a cup beneath a dispenser and taps their badge to the screen `credit transfer successful` then smacks the dispenser's side impatiently.

We follow the passage past a technician kneeling beneath an open panel, then enter a private room. Tarn sits with her headphones on. A hand taps her shoulder, and she looks up at the android she's been waiting to power up.

[Lower the music sharply with the next sentence.]

She pulls her headphones down around her neck, and we hear the ventilation running overhead.

# Progression

## Tarn And Eight Ball Eval Time [stamp-offset:: 0]

## Awkward Ooze (Mordrun and Ponderer) [stamp-offset:: 0]

## The Four become One

## Exiting the drift [stamp-offset::  133]

## Ship under attack [stamp-offset::  200]

## Crash Landing

## Timeline

```dataviewjs
const session = dv.current();
const clock = dv.page("Campaign/System/Campaign Clock");

if (!clock) {
    dv.paragraph(
        "> [!failure] Campaign Clock not found\n" +
        "> Confirm that the clock note path is correct."
    );
} else {
    const limit = Number(clock["lapse-size"]);
    const startLapse = Number(session["stamp-start-lapse"]);
    const startMinute = Number(session["stamp-start-minute"]);
    const width = String(limit - 1).length;

    function addMinutes(offset) {
        const total = startMinute + Number(offset);
        const lapse = startLapse + Math.floor(total / limit);
        const minute = total % limit;

        return `${lapse}:${String(minute).padStart(width, "0")} PES`;
    }

	    // Read the current note's Markdown.
	const content = await dv.io.load(session.file.path);
	
	// Find headings ending with [stamp-offset:: NUMBER].
	const headingPattern =
	    /^#{1,6}[ \t]+(.+?)[ \t]+\[stamp-offset::[ \t]*(\d+)[ \t]*\][ \t]*\r?$/gm;
	
	const events = Array.from(content.matchAll(headingPattern))
	    .map(match => ({
	        title: match[1].trim(),
	        offset: Number(match[2])
	    }))
	    .sort((a, b) => a.offset - b.offset)
	    .map(event => [
	        addMinutes(event.offset),
	        event.title
	    ]);

    if (events.length === 0) {
        dv.paragraph(
            "*No stamped events have been recorded for this session.*"
        );
    } else {
        dv.table(["Stamp", "Event"], events);
    }
}
```