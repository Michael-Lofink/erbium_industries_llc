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

We follow the passage past a technician kneeling beneath an open panel, then enter a private room. Tarn sits with her headphones on as a hand taps her shoulder, and she looks up at the android she's been waiting to power up.

[Lower the music sharply with the next sentence.]

She pulls her headphones down around her neck, and we hear the ventilation running overhead.

# Progression

## Tarn And Eight Ball Eval Time [stamp-offset:: 0]
Song: Finish fading out **Levitating**.

> Beside Tarn, the terminal displays a questionnaire with 8-Ball's name already filled in. A charging lead hangs loose beside his chair, and a small robot hovers near the table, adjusting its position whenever either of you moves. At the bottom of the form, the overall assessment remains blank.

Maggie has **The Crew** and **RoutineEvalFor8Ball**. Let Tarn introduce herself and conduct the evaluation, with Gregory deciding what 8-Ball knows, remembers, and chooses to disclose. The dossier's account of his crimes and consent to remain wiped is Erbium's account.

The form tells Tarn to ask the questions as written. Play out whichever answers produce conversation and summarize routine answers if needed. “Who do you consider to be part of your current crew?” helps establish whom he knows; the question about remaining wiped gives Gregory room to establish 8-Ball's response. Pause or redirect if he becomes distressed, as the form instructs.

Tuppie supplies tools and diagnostic readings when Tarn asks. Sven'a remains with 8-Ball under the existing authorization. Any ghosting can follow Gregory's established portrayal; this scene needs no mandatory memory reveal.

**Move on:** Once they have established how they treat each other, cut to Mordrun and Ponderer. The form can be finished afterward.

## Awkward Ooze (Mordrun and Ponderer) [stamp-offset:: 0]
> Outside the assessment room, your names share a line on the watch display: Ponderer and Mordrun Stronglimb. Beneath it, a reminder asks assigned partners to complete their pre-arrival grounding check. A crew member passes with a toolkit under one arm. “Get that logged before we come out of the Drift. Then bring your gear through for the check.”

Use the pairing discussed with Mary Beth: Mordrun and Ponderer are assigned partners under **A9%11&4-6**, the Extended-Voyage Cognitive Exposure and Quarantine Standard. The repository's Void Calling precautions include paired watches, spoken identity/location checks, and familiar anchors. They are checking on someone they boarded with; let their existing level of familiarity shape the exchange.

**Conversation prompts:** Confirm where they are and where they are going, ask how the other has been sleeping, and share a familiar object, routine, song, or memory that helps them feel grounded. Use one or two questions and let them talk. This is an ordinary prevention routine; it does not require a disease save or the treatment activity's skill check. There is no presumed infection.

Ponderer's background in counseling gives Jonah an opening, while Reen can answer as Mordrun and draw on his actual experience aboard the Dustbound Voyage. Neither must disclose private history. Do not require Ponderer to read his partner's mind.

**Disguise:** Reen can wear his issued armor over the holoskin under the September 18 ruling. His badge and processed assignment remain sufficient for the routine check; there is no new biometric intake here. Leave the reveal to Mary Beth and events in play, including Tarn's existing abilities below.

**Move on:** Once the pair has something to build on, Tarn and 8-Ball emerge or the crew member calls the group through.

## The Four become One
> Four equipment assignments fill the terminal, with Tarn listed as the personnel reviewer. Beside the rack, a crew member checks off the equipment you bring through. “Seals, charge levels, comm check. Then tell me who's carrying the shared kit.”

Let characters who have not met introduce themselves. This is a pre-arrival check of the **FED package already issued before the campaign**. Have the equipment cards available. Items marked crew-shared have one copy for the group; other issued items are individually leased. This equipment supplements their starting purchases. Establish who carries the repair kit, emergency beacon, and medical supplies, including what is stowed in null-space modules.

The crew member asks everyone to test their suit controls and the common comm channel. All personal weapons received the **SDI-68 Interlock**, as announced September 17; apply the existing equipment card when it matters. Tarn can explain her observation and reporting duties in her own words. These duties do not automatically make her the ship's captain or give her an unrestricted mandate to investigate her colleagues.

**When Tarn encounters Mordrun:** Her **Hologram Skeptic** card grants its check without needing to Search or Interact when the effect qualifies. Honor that trigger. You approved expert, Charisma-based **Persona (Mordrun Stronglimb) Lore** as a substitute modifier for Deception checks to Impersonate this persona. Use that ruling where applicable; it is not an extra item bonus or general Deception increase. Resolve discovery from the actual check and circumstances. Spotting a holographic disguise alone does not establish Reen's name, age, or history. The reveal has no scheduled scene, and neither outcome is guaranteed.

**Something to interact with:** A supply case has been left across the marked walkway beside the equipment rack. Its restraint will not latch. Anyone examining it can see a bent catch; securing the case with a spare strap solves the immediate problem. If left there, the case comes loose during the attack.

Once the check is complete, allow a little shipboard conversation, then advance the clock to Drift exit.

## Exiting the drift [stamp-offset::  133]
> The vibration beneath your feet changes. Beyond the nearest viewport, the purple light stretches into narrow bands and disappears, leaving a field of stars. A chime sounds through the ship. “Drift transit complete. Frontier personnel, check your relay caches before separation from stamp authority.”

The crew confirms that everyone's **PES-DR4 Relay Cache**, or Ghost Box, has retained an authenticated stamp. As coverage ends, it continues a locally signed record for later reconciliation. Local comms still work; outbound intersystem messages require relay access.

Give each player an opportunity to send a final message while the connection is available. They choose the recipient and content, or decline. Afterward, describe a sent message being acknowledged and any later message remaining queued.

**If asked:** The crew expects to continue the scheduled expedition and regain authorized communications when coverage permits. They have received no warning of an attack. Questions about exactly where they are going can use the assignment you establish for this voyage.

Advance through the remaining routine travel once the players have finished.

## Ship under attack [stamp-offset::  200]
Song: **Debris — Steven Price**, after the first impact.

> A hard impact throws a loose cup across the room. The lights go out and return in red, while a metallic rattle runs along the ceiling. Over the comm comes a strained voice: “We've taken a hit. Seal your suits. Get clear of the aft passage.” A second impact interrupts the transmission, and the floor begins to tilt.

**Situation:** The ship has lost its main drive and is on a descending trajectory toward a nearby body. A damaged pressure door separates the personnel compartment from the aft section. The bridge is attempting an emergency landing with the remaining controls.

Give the players that information when they check a display or contact the bridge. The crash is the planned campaign opening; emergency checks determine what they preserve and how the landing goes. Resolve each immediate problem once, using **DC 15 as a suggested improvised difficulty** when the outcome is uncertain. Let suitable equipment or a clear practical solution remove the need for a roll.

- **Door obstruction:** The door is trying to close against displaced equipment. Athletics, Crafting, or a suitable tool can clear it so the compartment seals. Failure leaves a pressure leak and forces them into the inner compartment; their sealed suits remain useful.
    
- **Crew member in the passage:** The equipment technician is down with a leg pinned beneath a shifted rack. Lifting or bracing it frees them. Successful rescue means they reach the protected compartment and can survive the landing.
    
- **Emergency landing controls:** A nearby terminal offers a connection to the bridge's emergency controls. Piloting can improve the approach; Computers or Crafting can restore a damaged control connection. Success keeps the personnel hatch clear at touchdown. Otherwise it is buried or jammed, requiring another exit.
    
- **Loose supplies:** Securing reachable gear preserves it. Gear they already carry or have stowed remains with them. The case from the earlier equipment check is either safely restrained or sliding across the walkway.
    

Ask each player what they do and allow them to help one another. Make the emergency controls clearly reachable so Mary Beth can use Reen's Piloting investment if she chooses. Tarn can work on damaged systems with her laptop and toolkit; Ponderer can coordinate or assist frightened personnel; 8-Ball can clear the route or move someone. Tuppie remains available for treatment and technical assistance within its existing abilities. These are opportunities, and players may pursue other workable approaches.

**Move on:** After everyone has affected the emergency, the bridge calls for restraints. Let them secure themselves and anyone they rescued before describing the landing.

## Crash Landing
Stop the music at impact.

> The first contact jolts through the seat frames. Metal tears somewhere beneath you, and the compartment shudders through a long scrape before finally stopping. Dust drifts through the emergency lights. Over the comm, you can hear breathing and someone trying the bridge channel again.

Let the PCs check one another and any rescued crew member. Their compartment has held; elsewhere, inaccessible sections and unanswered comm calls leave casualties uncertain. Record the actual survivors and the equipment protected during the descent.

Once they inspect the ship, they can establish that its drive cannot be restored with the tools and parts immediately available. The Ghost Boxes still record local time. Their emergency beacon can transmit locally, but reaching home requires access to a working intersystem relay or another vessel.

The hatch condition follows their actions during the descent. Describe the exterior once they obtain a view; choose its terrain and atmosphere when establishing the crash site. Keep suits sealed until they have assessed the environment.

##  Session Ending
End after the group gets its first clear look outside and chooses an immediate priority: search the wreck for survivors, establish a safe place to shelter, or position the beacon. Note that choice so October 3 begins with their action already underway.

**Carry forward:** Their location within the wreck, survivor names, carried supplies, damaged access routes, and last authenticated stamp. If the earlier scenes run long, stop at touchdown and begin October 3 with the compartment description above.

**First combat:** You told Mary Beth it would likely fall at the end of session 1 or in session 2. Keep space for a short encounter at the crash site if the table reaches it early; otherwise prepare it for October 3. The ship emergency is not itself a creature combat. Select the opposition after choosing the crash location; no attacker or encounter was established in these exports.

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