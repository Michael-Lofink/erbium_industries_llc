---
aliases:
  - Telepath Archetype
type: archetype
status: playtest
audience: player
updated: 2026-11-09
tags:
  - starfinder-2e
  - archetype
  - homebrew
  - occult
  - settled-systems
---
# Telepath

You can communicate mentally with another person and learn to recognize thoughts they have yet to express. With practice, you can follow several people in a shared conversation or anticipate an opponent’s movement from their immediate intention.

Some telepaths discover their abilities during ordinary conversations, answering questions before anyone speaks. Others develop them through training or after an unusual experience. A telepath might use these abilities to interview witnesses, coordinate a crew during an emergency, or help a companion resist mental interference.

This is a campaign homebrew archetype adapted from [Eyeswide Detective](https://2e.aonsrd.com/archetypes/16-eyeswide-detective). Its feats are available to characters who meet the listed prerequisites.

## Using this archetype

### Telepath DC

When you gain Telepath Dedication, choose Intelligence, Wisdom, or Charisma as your telepath attribute. Your **telepath DC** equals 10 + your level + your proficiency bonus + that attribute modifier. The proficiency bonus is +2 while trained, +4 while expert, and +6 while master. You are trained initially, become expert at level 9, and become master at level 17.

This proficiency applies to your telepath DC. You can change the attribute choice by retraining the dedication while retaining its dependent feats.

### Telepathy range and targeting

Your **telepathy range** is the range of the limited telepathy granted or improved by the dedication. Each ability uses its listed range; an entry that specifies your telepathy range uses this value.

These abilities require line of effect unless an entry states otherwise. Ordinary telepathy requires awareness of the recipient and knowledge of its location. Follow each ability’s targeting requirements, including visibility where specified.

Creatures immune to mental effects are unaffected by this archetype's mental abilities. An ability with the linguistic trait also requires a shared language unless that ability explicitly says otherwise. Open Communication removes the language requirement for voluntary communication only.

### Communication and information

Ordinary telepathic communication carries messages that participants deliberately send and follows the timing of ordinary speech. Abilities with auditory requirements require audible sound.

A participant can leave a willing link at any time as a free choice, taking no action. Players describe their own characters’ voluntarily shared experiences. When an ability reads thoughts or memories, the information reflects the subject’s knowledge and recollection, including mistakes.

### Effects and defenses

Telepath abilities are occult magical abilities. An ongoing effect has a counteract rank equal to half your level rounded up and uses your telepath DC. Its duration appears in its entry. Wards against telepathy or mental intrusion apply to the corresponding abilities.

For Delve Memory’s incapacitation trait, a target of higher level than you improves its saving throw result by one degree.

## Feat progression

| Level | Feats |
| --- | --- |
| 2 | Telepath Dedication |
| 4 | Attuned Perception; Mental Shelter |
| 6 | Psychic Interruption; Shared Channel |
| 8 | Read Thoughts; Open Communication |
| 10 | Predictive Strike; Borrowed Senses |
| 12 | Anticipate Danger; Delve Memory |
| 14 | Mindsense; Enduring Shelter |
| 16 | Distant Channel |
| 18 | Hold Together |
| 20 | Concordant Awareness |

## Level 2

```sf2e-stats
# Telepath Dedication
## Feat 2
==Uncommon== ==Archetype== ==Dedication== ==Occult==

**Prerequisites** Intelligence +2, Wisdom +2, or Charisma +2

A part of the solution to UNITY. You learn to send a thought deliberately and recognize a reply. A brief exchange becomes easier as you grow familiar with the other person.

You gain limited telepathy with a range of 30 feet. If you already have limited telepathy or telepathy with a range of at least 30 feet, increase that existing range by 30 feet instead; this is your telepathy range for this archetype. You retain any broader language access your existing telepathy grants. If its range was less than 30 feet, it becomes 30 feet.

You become trained in Occultism. If you are already trained in Occultism, become trained in another skill of your choice. Choose your telepath attribute and gain the telepath DC progression described above.

You gain Share Impression.

**Special** You cannot select another dedication feat until you have gained two other feats from the Telepath archetype.
```

---

```sf2e-stats
# Share Impression `pf2:1`
==Concentrate== ==Linguistic== ==Mental== ==Occult==

**Range** your telepathy range
**Targets** one willing creature you can see that shares a language with you

Send the target a sensory impression you remember, lasting up to 6 seconds. The target experiences it as a recollection while remaining aware of its surroundings. Alternatively, invite the target to share an impression; accepting and sending it are part of your action.

The sender chooses the content and can omit or invent details. Resolve an attempt to deceive using the Lie rules, with Deception opposed by the recipient’s Perception DC.
```

---

## Level 4

```sf2e-stats
# Attuned Perception
## Feat 4
==Archetype== ==Detection== ==Mental== ==Occult==

**Prerequisites** Telepath Dedication

You sense another creature’s attention as you observe its behavior. This impression helps you judge its intentions or notice its attempts to hide.

You gain a +2 circumstance bonus to Perception checks to Sense Motive against, or Seek, creatures within your telepathy range and line of effect that are not immune to mental effects. You also gain a +2 circumstance bonus to your Perception DC against those creatures' attempts to Lie to you.
```

---

```sf2e-stats
# Mental Shelter `pf2:R`
## Feat 4
==Archetype== ==Mental== ==Occult==

**Prerequisites** Telepath Dedication
**Frequency** once per 10 minutes
**Trigger** You or one willing ally you can see within your telepathy range is about to attempt a Will saving throw against a mental effect that you are aware of.

You send a reassuring thought that helps the target concentrate through an intrusion. The target gains a +1 circumstance bonus to the triggering save. Use this reaction before the roll.
```

---

## Level 6

```sf2e-stats
# Psychic Interruption `pf2:1`
## Feat 6
==Archetype== ==Concentrate== ==Linguistic== ==Mental== ==Occult==

**Prerequisites** Telepath Dedication
**Range** your telepathy range
**Targets** one enemy you can see that shares a language with you
**Defense** Will against your telepath DC

You insert an insistent question into the target's attention. After attempting its save, it is temporarily immune to your Psychic Interruption for 1 hour, regardless of the result.

**Critical Success** No effect.
**Success** The target cannot use reactions until the start of your next turn.
**Failure** As success, and the target is stupefied 1 for 1 minute.
**Critical Failure** As failure, but stupefied 2.

An affected target can spend one action with the concentrate trait to dismiss the question and end the stupefied condition imposed by this ability. The reaction restriction lasts until the start of your next turn.
```

---

```sf2e-stats
# Shared Channel
## Feat 6
==Archetype== ==Occult==

**Prerequisites** Telepath Dedication

You learn to follow several mental conversations at once, keeping track of who is speaking as you pass messages between them. You gain Establish Channel.
```

---

```sf2e-stats
# Establish Channel
==Concentrate== ==Exploration== ==Linguistic== ==Mental== ==Occult==

**Time** 1 minute
**Targets** up to three willing creatures you can see within your telepathy range, each sharing a language with you
**Duration** 1 hour

You join the targets and yourself in a shared conversation. Each participant can send a deliberate message to the entire channel or to one chosen participant. A pair of participants must share a language to understand each other. Messages pass through you; line of effect is required between you and each participant.

An individual participant's connection is suspended while it is outside your telepathy range, lacks line of effect to you, is unconscious, or is immune to mental effects. It resumes when those conditions end within the duration. Your own unconsciousness suspends the entire channel. Participants can leave at any time. Establishing another channel ends the previous one.
```

---

## Level 8

```sf2e-stats
# Read Thoughts `pf2:2`
## Feat 8
==Archetype== ==Concentrate== ==Detection== ==Mental== ==Occult==

**Prerequisites** Telepath Dedication
**Frequency** once per 10 minutes
**Range** 30 feet
**Targets** one creature you can see
**Defense** Will against your telepath DC

You briefly perceive what the target is thinking, which might arrive as words or an image. The target becomes temporarily immune to your Read Thoughts for 1 hour after the attempt, regardless of the result. A willing target can choose the failure result instead of rolling.

**Critical Success** You learn nothing. The target receives one vague surface thought from you and recognizes you as the source of the intrusion.
**Success** You learn nothing. The target notices that someone attempted a mental intrusion, without automatically identifying you.
**Failure** You perceive one brief, vague surface thought occupying the target at that moment.
**Critical Failure** As failure, and you discern the immediate emotion or intention associated with that thought.

On a failure or critical failure, the intrusion itself goes unnoticed; the target can still infer it from your behavior or other evidence. You understand the gist of the thought across language differences. The GM selects a current thought for an NPC, and a player selects the thought for their own character.
```

---

```sf2e-stats
# Open Communication
## Feat 8
==Archetype== ==Occult==

**Prerequisites** Telepath Dedication

You learn to understand the meaning a person intends to communicate across language differences. Increase your telepathy range by 30 feet. Your ordinary telepathic communication can reach any creature that knows at least one language.

Share Impression and Establish Channel lose the linguistic trait for you, and each target qualifies by knowing at least one language. Participants in your channel understand one another’s deliberately sent messages. Psychic Interruption and Delve Memory retain their shared-language requirements.
```

---

## Level 10

```sf2e-stats
# Predictive Strike `pf2:1`
## Feat 10
==Archetype== ==Concentrate== ==Fortune== ==Mental== ==Occult==

**Prerequisites** Telepath Dedication, Attuned Perception
**Frequency** once per 10 minutes
**Range** your telepathy range
**Targets** one creature you can see

You study the intention that precedes your opponent's movement. Attempt a secret Perception check against the target's Deception DC. Attuned Perception's bonus applies to this check. The fortune effect applies only to the attack roll granted by the result.

**Critical Success** As success. If the affected Strike hits, it deals additional precision damage: 2 if you are trained in Perception, 4 if expert, 6 if master, or 8 if legendary. Double this additional damage normally on a critical hit.
**Success** Before the end of your current turn, the next Strike you make against this target rolls its attack roll twice and uses the higher result. If that Strike critically hits, the target is off-guard until the start of your next turn.
**Failure** No effect.
**Critical Failure** No effect.

You must still be able to perceive the target when you Strike. Resolve the Strike using its normal range, multiple attack penalty, and targeting flat checks. Apply the normal rules for fortune effects.
```

---

```sf2e-stats
# Borrowed Senses `pf2:2`
## Feat 10
==Archetype== ==Concentrate== ==Mental== ==Occult==

**Prerequisites** Telepath Dedication, Shared Channel
**Frequency** once per 10 minutes
**Range** 120 feet
**Targets** one willing creature with an active connection in your Shared Channel
**Duration** sustained up to 1 minute

You experience the surroundings from your companion’s position. Their view might reveal a doorway around a corner or someone approaching behind you.

You receive the target’s current sight and hearing, including its low-light vision or darkvision. While receiving them, apply the blinded and deafened conditions to your body’s interaction with its surroundings. Checks using the borrowed sight and hearing use your own Perception, with those two conditions excluded from the check.

Measure the range and line of effect of your abilities from your own body. The borrowed sight and hearing provide your view of the target’s surroundings.

The effect ends if the channel connection becomes inactive, either participant becomes unconscious, or the target moves beyond 120 feet or your line of effect. Either participant can end it at any time, taking no action. When it ends, remove the blinded and deafened conditions imposed by Borrowed Senses. These ending conditions also apply through a Distant Channel.
```

---

## Level 12

```sf2e-stats
# Anticipate Danger `pf2:R`
## Feat 12
==Archetype== ==Mental== ==Occult==

**Prerequisites** Telepath Dedication, Attuned Perception
**Frequency** once per 10 minutes
**Trigger** A creature whose location you know, within your telepathy range and line of effect, makes an attack roll against you while you are off-guard to it.

You react to the intention behind the attack. Resolve the triggering attack roll against your Perception DC instead of your AC. Use this reaction before the roll. You remain off-guard, and the attack retains its usual targeting flat checks and effects, including sneak attack.
```

---

```sf2e-stats
# Delve Memory
## Feat 12
==Archetype== ==Concentrate== ==Detection== ==Exploration== ==Incapacitation== ==Linguistic== ==Mental== ==Occult==

**Prerequisites** Telepath Dedication, Read Thoughts
**Frequency** once per day
**Time** 1 minute
**Range** 30 feet
**Targets** one creature you can see that shares a language with you
**Defense** Will against your telepath DC

You follow a recollection back through its associations. An incidental smell or half-remembered face can become clearer as the experience takes shape.

Name a specific event that the target personally experienced, such as the last time it spoke to a particular person. The target must remain within range, visible to you, and within line of effect for the entire activity. If these conditions fail, the attempt ends and the daily use is spent. The target senses the intrusion from the start and can act normally throughout the attempt.

At the end, the target attempts its save and becomes temporarily immune to your Delve Memory for 24 hours. A willing target can choose the failure result instead of rolling. Apply incapacitation normally to a rolled save.

**Critical Success** You retrieve nothing. The target also recognizes the event you sought.
**Success** You retrieve nothing.
**Failure** You experience up to 1 minute of the target's recollection of that event, selected by the GM to address the event you named. The target identifies you as the source.
**Critical Failure** As failure, and you can ask up to three short factual questions about details the target remembers from that same event. You receive the corresponding recollections immediately, without further saves.

The event must be present in the target’s accessible memories for you to retrieve it. You experience the recollection as the target remembers it, including errors and any alterations made to the memory.
```

---

## Level 14

```sf2e-stats
# Mindsense
## Feat 14
==Archetype== ==Detection== ==Mental== ==Occult==

**Prerequisites** Telepath Dedication, Attuned Perception

You locate nearby creatures by sensing their mental activity. You gain mindsense as an imprecise sense with a range of 30 feet, detecting creatures with minds within your line of effect. Creatures immune to mental effects are excluded. Mindsense functions independently of light, sound, and language.

Resolve hiding, Seeking, and detection using the normal rules for an imprecise sense. A creature detected solely by mindsense is hidden to you and requires the normal DC 11 flat check to target. Attuned Perception applies to qualifying Seek checks.
```

---

```sf2e-stats
# Enduring Shelter
## Feat 14
==Archetype== ==Occult==

**Prerequisites** Telepath Dedication, Mental Shelter

You maintain contact through a painful mental intrusion, helping the target concentrate as it resists. The circumstance bonus from your Mental Shelter increases to +2. Its target also gains resistance to mental damage equal to half your level, rounded down, against damage dealt by the triggering effect as part of resolving that save. Apply the normal rules for overlapping resistances.
```

---

## Level 16

```sf2e-stats
# Distant Channel
## Feat 16
==Archetype== ==Occult==

**Prerequisites** Telepath Dedication, Shared Channel, Open Communication

You can maintain mental conversations across considerable distances. When you Establish Channel, you can spend 10 minutes to create a distant channel. You can do so once per day. It lasts 8 hours and can include up to six willing creatures besides yourself. Each target must meet Establish Channel's initial visibility, range, and line-of-effect requirements.

Once established, a distant channel carries deliberate messages within 1 mile of you, or across any distance if you and the participant are on the same planet. Messages pass through intervening barriers. A participant's connection is suspended while it is on another plane, outside these distance limits, unconscious, immune to mental effects, or protected by an effect that blocks telepathy. Your unconsciousness suspends the entire channel. A suspended connection resumes if the cause ends during the duration.

You can maintain one Shared Channel at a time, whether normal or distant. The increased range applies to messages; other abilities use their listed range and line-of-effect requirements.
```

---

## Level 18

```sf2e-stats
# Hold Together `pf2:R`
## Feat 18
==Archetype== ==Fortune== ==Mental== ==Occult==

**Prerequisites** Telepath Dedication, Mental Shelter, Shared Channel
**Frequency** once per day
**Trigger** One effect you are aware of requires you or one or more willing participants in your Shared Channel to attempt a Will saving throw against a mental effect.

When the group faces mental interference, you remind the affected companions of their surroundings and help them concentrate on resisting it. Choose up to four eligible creatures, including yourself if applicable. Each must be within 60 feet and your line of effect, and each ally must have an active channel connection. Use this reaction before any chosen creature rolls.

Each chosen creature rolls its triggering Will save twice and uses the higher result. Apply the normal rules for fortune effects. All chosen saves must be against the same triggering effect.
```

---

## Level 20

```sf2e-stats
# Concordant Awareness `pf2:2`
## Feat 20
==Archetype== ==Concentrate== ==Mental== ==Occult==

**Prerequisites** Telepath Dedication, Mindsense, Shared Channel
**Frequency** once per day
**Range** 60 feet
**Targets** you and up to three willing creatures with active connections in your Shared Channel
**Duration** 1 minute

You help the participants react to threats by sharing your awareness of nearby minds. Each target gains a +1 status bonus to AC and Reflex saves, and a +1 status bonus to Will saves against mental effects.

Each target gains precise mindsense within 30 feet for the duration, following Mindsense’s rules for eligible creatures and line of effect. Use the recipient’s Perception for detection checks and the normal rules for hiding from a precise sense. For a target that already has mindsense, this benefit makes it precise within 30 feet.

The effect ends for an ally if it leaves 60 feet, loses line of effect to you, or its channel connection becomes inactive. Reapplying this benefit requires a new use of Concordant Awareness. The entire effect ends if you become unconscious.
```
