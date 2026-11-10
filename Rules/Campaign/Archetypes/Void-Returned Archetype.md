---
type: archetype
status: playtest
updated: 2026-11-09
tags:
  - starfinder-2e
  - archetype
  - occult
---

## Void-Returned Archetype

Some survivors of true Void Calling retain physical changes after the crisis ends. Their breathing may pause for several minutes, and injuries that should have killed them leave them conscious. Others hear voices through sealed hulls or sense a nearby person before seeing them. Spacers call these survivors **Void-Returned**.

A survivor may have a dormant infection or have been cured. Record that status separately from this archetype. A dormant infection continues progressing according to [[Rules/Campaign/Afflictions/Void Calling|Void Calling's rules]], and an infected survivor can transmit the disease while it is active. A cured survivor retains the abilities gained here.

Examinations inside a natural planetary atmosphere are inconclusive because the affliction is dormant there. The changes represented by these feats continue to function in atmosphere. A Void-Returned remains a living creature.

When a feat grants the cosmic trait, use [[Rules/Campaign/Afflictions/Void Calling#Cosmic carriers|the cosmic carrier rules]]: harmful stage effects are suppressed while the normal timer continues. Failures and critical failures hold the stage in either environment. Outside atmosphere, successful saves can reduce the infection to stage 1. In natural planetary atmosphere, recovery saves continue at stage 1 and can cure the infection. When temporary protection ends, use the current recorded stage and remaining interval, applying atmospheric suppression where relevant.

```sf2e-stats
# Void-Returned Dedication

## Feat 2

==Rare== ==Archetype== ==Dedication==

**Prerequisites** You survived true Void Calling at stage 2 or higher and subsequently brought the affliction into dormancy or were cured

---

A part of the solution to UNITY. You retained part of the physical adaptation that sustained you during the crisis.

You become trained in Occultism. If you were already trained in Occultism, you instead become trained in Void Calling Lore. If you were already trained in both, you become trained in another Lore skill of your choice.

You gain the Refuse the Call reaction.

**Refuse the Call** `pf2:r`
==occult==  
**Frequency** once per day  
**Trigger** You would be reduced to 0 Hit Points by damage but would not be immediately killed.

**Effect** Your body repeats one of the changes that kept you alive during true Void Calling. You remain at 1 Hit Point and don't fall unconscious. For 1 minute, you gain the cosmic trait and are stupefied 1. If you are already stupefied, this effect doesn't increase the value of your stupefied condition.

**Special** You can't select another dedication feat until you have gained two other feats from the Void-Returned archetype.
```

---

```sf2e-stats
# Vacuum Memory

## Feat 4

==Archetype== ==Occult==

**Prerequisites** Void-Returned Dedication

---

The physical changes left by Void Calling help you withstand exposure.

Choose cold or void. You gain resistance to the chosen damage type equal to half your level.

While you are outside a natural planetary atmosphere, this resistance applies to both cold and void damage.
```

---

```sf2e-stats
# Someone You Know `pf2:R`

## Feat 4

==Archetype== ==Illusion== ==Mental== ==Occult== ==Visual==

**Prerequisites** Void-Returned Dedication

**Frequency** once every 10 minutes

**Trigger** A creature within 30 feet that can perceive you makes a Strike against you

---

For an instant, the attacker sees a familiar person from its memories where you are standing.

You are concealed from the triggering creature against the triggering Strike. It must attempt the normal DC 5 flat check to target you. After the Strike is resolved, the hallucination ends.

The creature doesn't necessarily understand what it saw, even if the Strike succeeds.
```

---

```sf2e-stats
# I Know That Voice

## Feat 6

==Archetype==

**Prerequisites** Void-Returned Dedication

---

You have already heard a voice use your own memories against you.

You gain a +1 circumstance bonus to saving throws against mental effects. This bonus increases to +2 against auditory mental effects and mental effects that would control you, confuse you, compel your movement, or dictate how you spend your actions.
```

---

```sf2e-stats
# No Breath Between Stars

## Feat 8

==Archetype== ==Occult==

**Prerequisites** Void-Returned Dedication

---

The temporary adaptation that once appeared only during the disease has become permanent.

You gain the cosmic trait. You can survive the basic environmental effects of vacuum and don't need to breathe while in space or a vacuum.

This feat doesn't grant a fly Speed. If you have a fly Speed from another source, the cosmic trait allows you to use it normally in vacuum and zero gravity.
```

---

```sf2e-stats
# Hear Them Through the Hull

## Feat 8

==Archetype== ==Occult==

**Prerequisites** Void-Returned Dedication

---

Empty space has never felt completely empty since you recovered.

You gain lifesense as an imprecise sense with a range of 30 feet. You perceive vital and void energies as faint voices, knocks, displaced movement, or the sensation that someone is standing just beyond your field of view.

This sense distinguishes living creatures from undead creatures but doesn't identify a specific creature by itself.

```

---

```sf2e-stats
# Invitation from Outside `pf2:2`

## Feat 10

==Archetype== ==Auditory== ==Concentrate== ==Incapacitation== ==Mental== ==Occult==

**Prerequisites** Void-Returned Dedication

**Frequency** once every 10 minutes

---

Choose one creature within 60 feet that can hear you. You speak in a voice drawn from the target's own memories and briefly show it a place, person, or emergency that appears to demand its immediate attention.

The target attempts a Will save against your class DC or spell DC, whichever is higher. This is a compulsion effect.

Choose an unoccupied point the target can perceive within 30 feet of it. Any movement caused by this ability must bring the target closer to that point and can't knowingly move it into hazardous terrain.

**Critical Success** The target is unaffected and is temporarily immune to Invitation from Outside for 10 minutes.

**Success** The target is frightened 1.

**Failure** The target is frightened 1. On its next turn, it must spend its first action Striding toward the chosen point if it is able to do so.

**Critical Failure** The target is frightened 2. On its next turn, it must spend its first two actions Striding toward the chosen point if it is able to do so.
```

---

```sf2e-stats
# Calling Recognition

## Feat 12

==Archetype== ==Occult==

**Prerequisites** Hear Them Through the Hull

---

You recognize the particular disturbance produced when the Calling has already touched a mind.

The range of your lifesense increases to 60 feet.

Your lifesense is precise when detecting creatures with an active form of Void Calling, including asymptomatic cosmic carriers, and creatures created by Void Calling, such as Void-Drawn. For other living and undead creatures, it remains imprecise.

A dormant infection provides no recognizable signature. Within a natural planetary atmosphere, a carrier is detected using ordinary lifesense. A Void-Drawn remains a transformed creature and can still be detected precisely.
```

---

```sf2e-stats
# Void-Drawn Resurgence `pf2:0`

## Feat 16

==Archetype== ==Concentrate== ==Occult== ==Polymorph==

**Prerequisites** Void-Returned Dedication

**Frequency** once per day

---

You allow the changes left by Void Calling to complete themselves temporarily without surrendering your identity.

Your breathing stops. Your body becomes unnaturally cold. Your eyes reflect points of light that don't correspond to the surrounding stars, and your voice occasionally seems to originate from somewhere beside or behind you.

For 1 minute, you gain the following benefits:

- You gain 40 temporary Hit Points.

- You gain a fly Speed equal to your land Speed.

- You gain the cosmic trait.

- You gain darkvision. If you already have darkvision, you gain greater darkvision for the duration.

- You gain resistance 15 to cold and void damage.

- The first time each round that you deal damage to a creature with a Strike or spell, you deal an additional 2d6 mental or void damage, chosen when you deal the damage.


While transformed, you remain a living creature. You don't gain the undead trait or void healing, and you don't become a Void-Drawn when the transformation ends.
```
