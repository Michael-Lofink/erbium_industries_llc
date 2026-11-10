---
aliases:
  - The Star Plague
  - Vacuum Sickness
  - The Call
type: affliction
tags:
  - erbium-industries
  - settled-systems
  - environmental-effect
  - gm-lore
  - disease
  - occult
  - space-travel
status: playtest
updated: 2026-11-09
---

# Void Calling

**Void Calling**, also called the **Star Plague**, is an occult disease encountered during travel beyond natural planetary atmospheres. Early symptoms can interrupt ordinary shipboard work: someone hears a relative calling through a ventilation grille, or repeatedly checks an exterior camera for a person the other watch officer cannot see. Over several days, the afflicted may become suspicious of their crewmates and try to leave the vessel to reach whoever they believe is outside.

This slower exposure syndrome can develop into true Void Calling after the victim enters vacuum. The true form causes severe weakness and confusion within minutes, followed by death and transformation into a Void-Drawn. Survivors sometimes retain physical changes associated with the [[Rules/Campaign/Archetypes/Void-Returned Archetype|Void-Returned archetype]]. Settled Systems Code `A9%11&4-6` classifies the disease as **vacuum-associated cognitive exposure syndrome**, usually shortened to **vacuum sickness** in official reports.

## Shared Affliction Rules

### Natural planetary atmosphere

Either form becomes **dormant immediately** within a natural planetary atmosphere. A toxic or unbreathable atmosphere qualifies, including while the person is inside a sealed habitat on that world. Use the setting's atmosphere boundary; trace gas in near-vacuum does not qualify. Air maintained aboard a ship, station, or spacesuit outside that boundary provides ordinary life support while the affliction remains active.

Record the form, stage, and remaining time until the next stage save or the end of onset. Also record any consecutive success required by virulent. During dormancy, pause these timers and suppress the affliction's symptoms, conditions, vacuum adaptation, and transmission. Injuries and Hit Points already lost require ordinary recovery.

Leaving the natural atmosphere restores the recorded stage effects and resumes the remaining timer. If a body has reached the lethal stage, atmosphere pauses its pending transformation; the victim remains dead.

A dormant infection is **undetectable**, so examinations during dormancy are inconclusive. Previous symptoms and exposure records can justify suspicion.

### The Drift

Travel within the Drift prevents new exposure to either form. Crews commonly believe that entering it also suppresses an existing infection.

### Cosmic carriers

A creature that contracts either form while it has the cosmic trait begins at **stage 1** after any onset, even on a critically failed initial save. Its harmful stage effects are suppressed, and it remains a carrier until an effect counteracts or removes the disease.

If a creature gains the cosmic trait while already afflicted, retain its recorded stage and suppress the harmful stage effects. It functions as a stage-1 carrier for transmission. Continue the existing onset or stage timer, using the normal interval for the recorded stage. While that stage is above 1, attempt a stage save at each interval: successes reduce it according to the infection's recovery rules, to a **minimum of stage 1**; failures leave it unchanged. Apply virulent normally. At stage 1, intervals continue without a roll.

If the cosmic trait ends, apply the effects and ordinary save outcomes of the current recorded stage, preserving the remaining interval and any pending virulent success. Natural planetary atmosphere pauses all of these timers under the dormancy rules.

### Transmission and exposure checks

**Transmission begins at stage 1.** For an ongoing exposure source, make the initial save when the stated exposure duration is completed, then once per additional 24 hours while that source persists. A discrete attack or hazardous manifestation uses its own exposure instruction. An existing infection follows its stage timer; repeated exposure to that same form does not accelerate it.

A creature can carry one form at a time. If a creature with Exposure contracts true Void Calling, replace Exposure with the true form. On a successful initial save against the true form, retain its existing Exposure stage and timer.

### Saves and recovery

Use the usual affliction rules: an initial failure produces stage 1, and an initial critical failure produces stage 2 after any onset. At each stage interval, a failure increases the stage by 1 and a critical failure by 2. A success reduces it by 1 and a critical success by 2, subject to virulent. For a creature without the cosmic trait, recovering below stage 1 cures the infection.

A virulent affliction requires two consecutive successful stage saves for a one-stage reduction. A critical success reduces the stage by 1 immediately. After a reduction or a failed save, start a fresh count. Initial saves use their normal results.

## Void Calling Exposure

```sf2e-stats
# Void Calling, Exposure
## Disease 6
==Disease== ==Mental== ==Occult==

The afflicted hears familiar voices through machinery noise or the exterior hull. As the syndrome develops, those voices become easier to recognize than the people aboard the vessel.

**Exposure** Spending 24 consecutive hours outside a natural planetary atmosphere and the Drift aboard a vessel or habitat without a functioning void-grounding protocol; spending 8 consecutive hours aboard the same occupied vessel or habitat as a creature with an active stage-1-or-higher infection; or an exposure ability of a Void-Drawn.

**Saving Throw** DC 22 Will
**Onset** 3 days

**Virulent proximity** This form gains virulent for stage saves made within 30 feet of another active carrier of either form. If that proximity ends, the next save uses ordinary recovery rules and clears any pending virulent success.

**Stage 1** Asymptomatic carrier. (1 day)

**Stage 2** Stupefied 1. A familiar voice seems to speak through ventilation, machinery, or the hull. (4 hours)

**Stage 3** Stupefied 1. Before taking a move action that would bring you within 10 feet of another creature, attempt a DC 5 flat check. On a failure, the action is lost. (4 hours)

**Stage 4** As stage 3, and other creatures are hidden from you. A creature within your reach is observed. A creature within 30 feet becomes observed from the moment it uses a move or manipulate action until the end of its turn. These are the ways this stage allows a creature to become observed. (1 day)

**Stage 5** As stage 4, with the airlock compulsion below. (1 hour)

**Airlock compulsion** At the start of your turn in an encounter, or once per 10 minutes during exploration, attempt a DC 22 Will save. These are compulsion saves and do not change the disease's stage.

**Critical Success or Success** You act normally.
**Failure** Spend your first available action moving toward the nearest known route into open space. If adjacent to its access mechanism, use that action to Interact with it.
**Critical Failure** Spend all available actions pursuing that route and operating its access mechanisms.

If you know no route, the GM describes the direction indicated by the hallucination. The required movement follows that direction. This is a compulsion effect.

**Vacuum escalation** Entering vacuum at any active stage exposes you to true Void Calling, including while wearing a spacesuit. If this form becomes active while you are already in vacuum, resolve that exposure immediately. Make at most one initial save per 24 hours from this trigger.
```

---

## True Void Calling

```sf2e-stats
# Void Calling
## Disease 10
==Disease== ==Mental== ==Occult== ==Virulent==

True Void Calling develops immediately after a failed initial save. Breathing stops or becomes irregular, the victim's limbs weaken, and their responses become slow and confused. They may continue describing people or structures visible only to them.

**Exposure** Vacuum escalation from Void Calling, Exposure; spending 10 minutes within 30 feet of a Void-Drawn; or direct exposure to a powerful manifestation designated by the GM. Ordinary proximity to a living carrier exposes a susceptible creature to the slower Exposure form.

**Saving Throw** DC 27 Will
**Onset** Immediate

**Vacuum adaptation** Throughout active stages 1–3, you can survive the basic environmental effects of vacuum and function without breathing there.

**Stage 1** Stupefied 1 and enfeebled 1. (1 minute)

**Stage 2** Stupefied 2, enfeebled 2, and slowed 1. You gain resistance 5 to cold and void damage. (1 minute)

**Stage 3** Stupefied 3, enfeebled 3, and slowed 2. Your resistance to cold and void damage is 10. Your limbs respond slowly, and speaking requires considerable effort. (1 minute)

**Stage 4** Death. After 1d4 rounds, the body rises as a Void-Drawn under the GM's control.

An initial failure followed by ordinary failed stage saves causes death after 3 minutes. Critical failures can shorten that interval to 1 minute.
```

## Nature of the Affliction

Void Calling spreads through an occult interaction between minds. Several people aboard a vessel may describe someone standing outside the same viewport, with each witness recognizing a different person. Medical investigators use these related accounts to trace outbreaks; efforts to isolate a consistent organism have been inconclusive.

Long driftless voyages create repeated opportunities for exposure, especially when crew members sleep poorly or work alone for extended periods. An asymptomatic carrier can expose crewmates aboard a well-run vessel.

Entering a natural planetary atmosphere suppresses the infection. A patient can recover clear speech and recognize their companions while still carrying the disease, which resumes when they depart. This makes exposure records important during crew transfers: a medical examination conducted planetside yields an inconclusive result even for an infected traveler.

## Hallucinations

The hallucinations use people and situations the victim remembers. A crew member might hear a missing relative asking for help outside a maintenance lock, using a familiar nickname. Someone accustomed to rescue work might see a stranded worker pointing to damaged equipment and move to collect a suit before mentioning the sighting to anyone else.

As symptoms worsen, the victim may struggle to recognize the people helping them. A familiar crewmate's face appears wrong, or their movements seem delayed. The person outside remains recognizable, and an attempt to restrain the victim can look like an obstruction to an urgent rescue.

## Recognition and Diagnosis

Outside a natural planetary atmosphere, Medicine can identify the recurring symptoms and Occultism can identify the influence during a structured examination. An examination takes 1 minute and uses a secret check against the form's DC: 22 for Exposure or 27 for true Void Calling. Medicine requires a medkit and physical access to the subject. Occultism requires the subject to be conscious, cooperative, and able to communicate with the examiner. Success identifies the active form and stage; failure is inconclusive.

Record someone who previously tested positive as a suspected dormant carrier until a cure or an active-state examination resolves their status.

Watch logs can help identify the first symptoms. Repeated requests to inspect an exterior hatch warrant an assessment when the person also reports interrupted sleep or a familiar voice outside. During true Void Calling, weakening limbs and delayed responses make treatment urgent; another caregiver can examine the patient while assistance begins.

Crews check reported exterior emergencies against independent sensors before opening an airlock. An afflicted witness can still report a real accident, so their condition becomes part of the assessment alongside camera footage, pressure readings, and the location of other personnel.

## Prevention

Long-voyage crews work paired watches and check one another's sleep and recent observations during handover. Grounding protocols maintain a regular daily routine and limit time spent alone watching open space. Some vessels cover viewports during rest periods and use artificial horizon displays to help the crew remain oriented.

Exterior access requires an independent check of the reported problem and authorization from a second person. Mechanical locks keep the airlock secured during a software failure. A crew member showing credible symptoms is relieved of flight-critical duties while someone stays with them and arranges an assessment. Navigators keep a diversion toward a natural planetary atmosphere available when the route permits it.

Before departure, crew members choose **anchors** they can use during a grounding check. An anchor can be a shared memory or a familiar object. A caregiver might discuss a repair they completed together while checking the patient’s awareness of their present location.

## Treatment

Treat Disease uses its normal eight-hour activity to prepare for a subsequent stage save. Grounding Check provides a shorter way to prepare for a stage save. During true Void Calling's minute-long intervals, use Emergency Grounding below, a suitable disease-removal effect, or rapid transport into a natural atmosphere.

Effects that counteract or remove diseases can cure either form, including a dormant infection, if their targeting requirements are met. For counteracting, Exposure is rank 3 at DC 22 and true Void Calling is rank 5 at DC 27. Treatment that only improves stage saves remains subject to the cosmic carrier’s stage-1 floor. An effect used on a suspected dormant carrier gives no diagnostic confirmation of infection or cure while the target remains in atmosphere; the GM tracks the result privately. Disease-removal effects apply to pending transformation only if their normal targeting permits affecting the body.

Caregivers bring a patient with Exposure to a compartment with covered viewports and supervised exits. Someone familiar stays with them, explains where they are, and checks reported emergencies with the rest of the crew. During the true disease's crisis, attendants clear space around the patient and prepare for immediate transport. A patient being cured in vacuum needs a functioning suit or other environmental protection as the disease's vacuum adaptation ends.

## Settled Systems Classification

Settled Systems Code `A9%11&4-6`, the **Extended-Voyage Cognitive Exposure and Quarantine Standard**, sets the minimum precautions for registered long-voyage vessels. Operators must maintain watch records and an approved grounding protocol, restrict airlock access, and provide a procedure for relieving symptomatic personnel. An afflicted person with control of navigation or exterior doors can endanger everyone aboard, making supervision an immediate operational concern.

The standard also requires records of unexplained exterior alarms and provision for treatment or diversion toward a natural planetary atmosphere. Exposure at stage 3 or higher requires a formal incident report, as does every episode of true Void Calling. Medical records must distinguish dormant infection from confirmed cure so the next crew can plan for a patient's departure from atmosphere.

These records affect liability after an outbreak. An operator with signed acknowledgments and complete grounding logs can attribute a loss to a worker's failure to follow procedure. Incomplete records can cost a vessel its insurance or docking eligibility, and survivors may lose compensation even when equipment failed.

Quarantine procedures call for supervision and sensory grounding. On ships with limited medical staff or spare compartments, security personnel often sedate a patient and restrain them alone. The arrangement leaves the patient with fewer opportunities to compare their perceptions with another person and reduces the crew's ability to notice a worsening condition.

# Discovery

The earliest human and dwarven voyage records after the [[Star Dream]] contain no accounts of Void Calling. Those crews traveled comparatively short routes near inhabited systems and stayed in close contact while learning to operate their vessels. The first surviving descriptions of the disease come from expeditions beyond the region now recognized as the [[Settled Systems]].

Separate expeditions recorded relatives apparently standing outside the hull and crew members entering maintenance locks to reach them. Recovery teams later found intact, empty suits and bodies that moved in vacuum. Several ships returned before their crews showed obvious symptoms; outbreaks subsequently appeared aboard vessels that had stayed closer to settled worlds. The surviving records leave the identity of the first affected expedition uncertain.

By Lapse 2, paired watches and mechanical airlock restrictions were common on long driftless voyages. Crews also covered viewports during scheduled periods and checked one another's identity and location aloud. These practices survive in spacer routines, including the habit of asking another watch officer to verify an unexplained sound outside the hull before investigating it.

# Player Options
```sf2e-stats
# Grounding Check
## Activity 10 Minutes
==Auditory== ==Concentrate== ==Mental==

You guide an afflicted creature through familiar memories, physical sensations, current surroundings, and independently verified facts.

**Requirements** You are trained in Diplomacy, Medicine, or Occultism; the target has an active form of Void Calling, is willing, within your reach, and able to perceive you.

---

Attempt a Diplomacy, Medicine, or Occultism check against the DC of the target's Void Calling affliction. The target is temporarily immune to further Grounding Checks for 8 hours.

**Critical Success** The target gains a +2 circumstance bonus to its next stage save against Void Calling. For 10 minutes, the target treats creatures within 30 feet as observed unless another effect would make them hidden or undetected.

**Success** The target gains a +1 circumstance bonus to its next stage save against Void Calling.

**Failure** You provide comfort but no mechanical benefit.

**Critical Failure** As failure.

A bonus from Grounding Check doesn't stack with the bonus from Treat Disease.
```

---

```sf2e-stats
# Emergency Grounding `pf2:2`
==Concentrate== ==Mental==

**Requirements** You are trained in Medicine or Occultism; the target has active true Void Calling and is within your reach. Using Medicine requires a medkit and gives this activity the manipulate trait. Using Occultism requires a conscious, willing target that can perceive you and gives it the auditory trait.

You support the patient's failing coordination or guide them through a brief orientation to their surroundings. Attempt a Medicine or Occultism check against DC 27. The target is then immune to further Emergency Grounding attempts until after its next stage save.

**Critical Success** The target gains a +2 circumstance bonus to its next stage save against true Void Calling.
**Success** The target gains a +1 circumstance bonus to that save.
**Failure or Critical Failure** No effect.

Use the highest applicable circumstance bonus if the target also benefits from Grounding Check or Treat Disease.
```

---

```sf2e-stats
# Voidwise
## Feat 1
==General== ==Skill==

**Prerequisites** trained in Occultism

---

You have studied the symptoms, spacer traditions, and containment procedures associated with Void Calling.

You can use Occultism in place of Medicine to Treat Disease when the target is afflicted with either form of Void Calling.

While you can perceive at least one allied creature within 30 feet, you gain a +1 circumstance bonus to saving throws against Void Calling.
```

---
![[Rules/Campaign/Archetypes/Void-Returned Archetype]]

---

# GM Information

> [!danger] GM Information  
> Transmission occurs when one mind begins accepting an afflicted mind's perception of the void. The hallucinations use information taken from the victim. A Void-Drawn can reproduce a private phrase or familiar voice belonging to someone known to that victim, including people the creature has never met.
> 
> The Calling became capable of interpreting the minds of the Elect through the first frontier infections. This accounts for the absence of cases among the earliest post-Star-Dream crews. The mechanisms behind that adaptation and atmospheric suppression remain unresolved.
> 
> Erbium has outbreak records that overlap with suppressed survey routes and abandoned extraction claims. Its research divisions disagree about what causes the disease, and access to findings is restricted between departments. A researcher may know that a particular route has an unusually high incidence while lacking the records needed to explain it.
> 
> A Void-Drawn retains fragments of its former identity. Some have directed rescuers toward survivors; others have used familiar voices to persuade people to open airlocks. Whether the original person remains conscious is unresolved.
> 
> When creating a Void-Drawn, use a creature of approximately the victim's former level. Add the cosmic and undead traits, darkvision, void healing, the standard undead immunities, and the ability to survive in vacuum. A Void-Drawn should also have an auditory or telepathic ability capable of exposing nearby creatures to Void Calling, Exposure.
> 
> Destroying a Void-Drawn ends its immediate influence. Existing infections continue according to their recorded stages and timers.

## Drift adjudication

Before running an infected creature’s journey through the Drift, decide whether that transit suppresses the infection or allows it to remain active. For suppression, use atmospheric dormancy’s bookkeeping; for continued activity, use the existing stage timer and active-state diagnosis rules. Record the observed result for that episode while leaving the broader cause and reliability of suppression open.

## Revision record

Revised November 9, 2026. The GM's October messages establish transmission beginning at stage 1, including asymptomatic carriers. This revision separates the slow Exposure syndrome from the one-minute crisis, introduces atmospheric dormancy and diagnostic silence, and establishes persistent cosmic carriers. Cosmic suppression retains normal stage intervals and permits improvement down to stage 1; curing a carrier requires an effect that counteracts or removes disease. Existing PDF exports are earlier snapshots.

Rules reference: Starfinder 2e Player Core p. 201 for Treat Disease and pp. 422–423 for affliction onset, stage saves, repeated exposure, and virulent. The dormancy, carrier intervals, examination, and Emergency Grounding procedures above are campaign homebrew. See [[Campaign/GM Notes/Continuity/Void Calling Revision and UNITY Keys|the design and continuity note]] for timing examples and unresolved lore.

## Proposed Settled Systems Code Register Addition

|Citation|Formal Subject|Public Purpose|Practical Effect|
|---|---|---|---|
|`A9%11&4-6`|**Extended-Voyage Cognitive Exposure and Quarantine Standard**|Establishes minimum prevention, reporting, quarantine, airlock-security, and treatment procedures for vacuum-associated cognitive exposure syndrome.|Protects crews during real outbreaks while allowing employers to remove symptomatic workers from duty, restrict travel, impose compulsory evaluation, and deny liability when required grounding records appear complete.|
