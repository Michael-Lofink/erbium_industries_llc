# PES Timekeeping Toolkit

A command-palette workflow for the Erbium Industries LLC Obsidian vault. Uses the installed Templater and Dataview plugins. Version 1.0.0.

## What you do at the table

Open your session note. Run **PES Advance time**, enter the fictional time that passed, then use **PES Record scene** to attach the current stamp to a scene. The session note displays separate planned and actual timelines. Every scene in either table links to its heading.

For your existing prep, initializing Session 1 preserves these planned times:

| Scene | Offset | Planned PES stamp |
| --- | ---: | --- |
| Tarn And Eight Ball Eval Time | 0 | 29:08472119 PES |
| Awkward Ooze (Mordrun and Ponderer) | 0 | 29:08472119 PES |
| Exiting the drift | 133 | 29:08472252 PES |
| Ship under attack | 200 | 29:08472319 PES |

To connect the last two scenes, run **PES Plan scene**, select **Ship under attack**, choose **Minutes after another scene**, select **Exiting the drift**, and enter `67`. If you later move Drift exit to +150, the attack moves to +217, or `29:08472336 PES`. A fixed +200 offset remains +200 until you edit it. A delay of zero makes scenes simultaneous.

During play, suppose Drift exit happens at +140. Advance the session by `140` and record that scene **Now**. Its actual stamp becomes `29:08472259 PES`; the plan stays intact. Advance by another `67` to reach +207. If the session eventually ends at +240, **PES Finish session** commits `29:08472359 PES` to the campaign clock. Repeating Finish adds no time. A fresh Session 2 initialized afterward starts at that ending stamp.

The uploaded Session 1's `elapsed-minutes: 240` is imported as a **planned duration**. Actual elapsed time begins at zero; no previous play is invented. If you are entering an already played session, enter its actual elapsed duration and record its events using the earlier-time option before finishing it.

## Installation — automated option

This package is an add-on; it does not contain the full vault or replace your campaign archive. Extract `PES-Toolkit.zip`. Its `vault/` folder contains the files to install. Your destination is the directory that already contains `Campaign`, `Scripts`, `Templates`, and `.obsidian`.

Close Obsidian before applying the installer. On Linux, from the extracted `PES-Toolkit` directory, preview the changes:

```bash
python3 install.py "/absolute/path/to/Erbium Industries LLC"
```

Then install:

```bash
python3 install.py "/absolute/path/to/Erbium Industries LLC" --apply
```

Replace that example path with your actual vault path. The first command is a dry run. The second copies the toolkit files, backs up files it replaces, and merges the Templater settings needed for commands. Other Templater settings, existing command registrations, and any existing `local-time.json` anchor are retained. It leaves your system hotkeys and the other plugins' settings alone. It checks the saved configuration format and stops if your folder configuration needs manual handling.

Backups are stored at `PES-Backups/<installation timestamp>/`, with an `install-record.json` listing replaced and newly created files. The installer updates the old `Scripts/advance_stamp.js` and `Templates/Advance Stamp.md` to route into the session clock. Existing Advance Stamp commands will therefore require an active session note.

Reopen Obsidian, open `Campaign/Sessions/Session 1.md` in an editing mode, and press **Ctrl+P**:

1. Run **Templater: Insert PES Initialize session**. This imports the old heading offsets, preserves the stored session start, snapshots the lapse size, and replaces the two old session Dataview blocks with shared views.
2. Run **Templater: Insert PES Upgrade displays** once. This updates the Campaign Clock and Campaign Timeline display code, keeping their properties. The clock's four hard-coded configuration bullets are removed because the shared view displays the current values.
3. Run **Templater: Insert PES Check session**.
4. When play begins, run **Templater: Insert PES Start session**.

Depending on Templater's display settings, command names may include their folder path. Search for `PES`. Choose the **Insert** commands. In the uploaded Templater 2.20.6, registration also exposes **Create** commands; those create a new file and are unnecessary for this workflow.

The existing `Campaign Clock` and session notes are migrated by these commands, after installation. The installer does not apply note migrations or advance time.

## Manual installation

Merge the package's `vault/` contents into the vault root. Keep an existing `local-time.json` if you have already configured an anchor. Preserve the folder structure and make a copy of the existing `Scripts/advance_stamp.js` and `Templates/Advance Stamp.md` before replacing them.

| Exact vault-relative path | Purpose |
| --- | --- |
| `Scripts/pes.js` | Command prompts and note updates |
| `Scripts/advance_stamp.js` | Compatibility entry point for the previous command |
| `Templates/Advance Stamp.md` | Previous command, now using the session clock |
| `Templates/PES/*.md` | Individually registerable commands |
| `Campaign/System/PES/core.js` | Shared arithmetic, scene parsing, and session transitions |
| `Campaign/System/PES/view.js` | Shared Dataview renderer |
| `Campaign/System/PES/local-time.json` | Optional Theosis anchor; initially unset |
| `Campaign/System/PES/PES-Dictionary.txt` | Optional field-name autocomplete |

In **Settings → Templater**, set **Template folder location** to `Templates` and **Script files folder location** (or **User scripts folder**) to `Scripts`. Register the files in `Templates/PES/` under **Template hotkeys**. Registration exposes commands even when no key combination is assigned. The inspected version saves these paths in `enabled_templates_hotkeys`.

If your live Templater settings use another scripts folder, place `pes.js` there and preserve the existing setting. If templates live elsewhere, move the PES command templates into that folder and register their actual paths. The shared `Campaign/System/PES/` location stays as listed above.

In **Settings → Dataview**, keep **Enable JavaScript Queries** enabled. It is already enabled in the uploaded configuration, along with automatic refresh at 2,500 milliseconds. Meta Bind's JavaScript setting can stay disabled; this toolkit does not use it.

After registering the templates, follow the four first-run commands above. Reload Obsidian if the user script has not been picked up yet.

## Command reference and suggested hotkeys

Assign combinations under **Settings → Hotkeys** by searching for the Insert command. These are suggestions; check Obsidian's conflict indicator before assigning them.

| Template in `Templates/PES/` | What it does | Suggested key |
| --- | --- | --- |
| `PES Menu.md` | Searchable list of all PES actions | Ctrl+Alt+P |
| `PES Initialize session.md` | Initialize a fresh note or import existing prep | — |
| `PES Plan scene.md` | Stamp an existing heading or append a new scene | Ctrl+Alt+S |
| `PES Start session.md` | Claim the campaign clock for this session | — |
| `PES Advance time.md` | Add fictional elapsed time to this session | Ctrl+Alt+A |
| `PES Record scene.md` | Record current/earlier actual time, or clear it | Ctrl+Alt+R |
| `PES Insert current stamp.md` | Insert the session's actual current stamp into prose | Ctrl+Alt+I |
| `PES Correct elapsed time.md` | Set actual elapsed time to an explicit duration | — |
| `PES Synchronization.md` | Choose on-stamp, off-stamp, or unspecified | — |
| `PES Planned duration.md` | Set the expected session duration | — |
| `PES Finish session.md` | Commit the ending stamp, or recover an interrupted finish | — |
| `PES Check session.md` | Validate scene times and clock ownership | — |
| `PES Upgrade displays.md` | Migrate the campaign clock and campaign timeline views | — |

These are Templater Insert commands: run them with a session note open in Source mode or Live Preview. They preserve selected text before opening their prompts. The current-stamp command inserts at the resulting cursor position. A new scene is appended to the note, and an existing heading can be selected anywhere in it.

Input accepts whole minutes (`67`, `67m`, `67 minutes`), whole hours (`2h`), corporate standard days (`1d` = 1,440 minutes), Theosis civic bands (`1 band` = 1,470 minutes), and Theosis rotations (`1 rotation` = 11,760 minutes). Units are case-insensitive. Use one whole-number unit per input; `90m` expresses an hour and a half. Negative values are allowed for planned session offsets, such as a flashback. Actual elapsed time and delays after another scene must be nonnegative.

## Planning, actual time, and historical records

Each scene stores a stable ID and timing data in a single HTML comment immediately below its heading. The commands manage this line:

```markdown
## Exiting the drift
<!-- pes: {"id":"pes-example-exit","plan":{"kind":"offset","minutes":133}} -->

Your existing scene prose continues here.
```

The comment is hidden in Reading view. Keep it immediately beneath the heading when moving scenes, and keep the ID when renaming a scene. A relative scene references that ID, so changing a title does not break its dependency. Removing a referenced scene produces a visible error until its dependent scenes are retimed. Circular dependencies, duplicate IDs, and identical stamped headings are rejected; give simultaneous scenes distinct names so heading links remain unambiguous.

| Timing mode | Effect when another scene moves |
| --- | --- |
| Offset from session start | Stays at its stored offset |
| Absolute PES stamp | Stays at its stored stamp |
| Minutes after a scene | Moves with that scene's planned **start** |
| Recorded actual time | Stays at its recorded absolute stamp |

The reference point is always a scene's start. Set the delay to include that scene's duration and any gap you intend. The toolkit does not infer durations from prose or advance time from a real-world timer. Actual timelines sort by actual time; planned timelines sort by planned time. Equal stamps retain note order.

Stored fields are ordinary YAML properties. `stamp-start-lapse`, `stamp-start-minute`, and `stamp-lapse-size` belong to that session. Advancing the campaign never rewrites them. `stamp-planned-minutes` holds the expected duration; `stamp-actual-minutes` holds elapsed play time. The legacy `elapsed-minutes` field is synchronized to actual elapsed time on completion for compatibility. The new views use the separate fields throughout play.

Create the next session as a fresh note in `Campaign/Sessions/`, then initialize it. Copy only desired prose when reusing a completed note; copying its session ID, status, and timestamps would also copy its history. A session prepared before the previous one ends keeps its planned starting stamp. If that start has become stale, Start session refuses to claim the clock. In a **prep** note with no recorded actual times, you can set `stamp-start-lapse` and `stamp-start-minute` to the committed campaign stamp in Properties. Session offsets then move with the new start; absolute scene stamps remain fixed.

Finished sessions are locked to the editing commands. Manual Markdown edits remain possible, so normal vault backups or Git history remain useful. The toolkit does not reconstruct the historical outcome of a session from its prep.

## Finishing, interruptions, and corrections

The campaign clock holds the last committed time while the active session holds live time. Only one session can own that clock. Do all advances in the active session, using the new command or the redirected old Advance Stamp command.

Finish first writes a `closing` record with the intended absolute ending stamp. It then updates the campaign clock, marks the session completed, and releases the active-session claim. If a write is interrupted, run **PES Finish session** again on the same note. A commit identifier prevents time from being applied twice. An interrupted Start can likewise be retried on the same note.

If another process changes the campaign clock during play, commands stop with a conflict message. Inspect the active session's frozen starting stamp and the clock's edit history before correcting it. An active session expects the committed campaign clock to remain at its start; its live elapsed time is in the session note. Do not run these commands concurrently on multiple devices. The in-app guard and atomic per-file checks are not a distributed synchronization lock.

To correct an accidental advance during an active session, use **PES Correct elapsed time**. It refuses a time earlier than an already recorded event; clear or correct that event first through **PES Record scene**. That command's earlier-time option also lets you record an event you forgot to stamp. Re-recording a scene updates its single actual timestamp. Use separate headings for distinct repeated occurrences.

Do not rename or move an active session until it finishes: the campaign clock records its owning path. If you already moved it, restore the original path shown in `pes-active-path`, finish, then move it. A copied active note cannot claim ownership through its duplicated ID.

## Off-stamp time and local calendars

Set synchronization to **on-stamp** while the group has an authenticated relay connection. At separation, choose **off-stamp**. The clock continues to advance normally, and each actual scene records its synchronization status. Leaving an on-stamp state preserves the last authenticated stamp; an unspecified previous state does not invent one. The ending synchronization state and known authentication stamp carry into the next session.

Reconnecting marks the current modeled stamp authenticated. This version does not simulate oscillator drift, contested corporate records, or payroll reconciliation. Changing relay status never deletes or adds elapsed minutes.

Theosis conversion factors are available for duration input immediately. Converting a PES stamp into a specific local rotation and band requires an epoch pairing that the supplied sources do not establish. `local-time.json` therefore starts with `"theosis": null`.

If you establish an anchor, set `stamp-local-calendar: theosis` in the session's Properties and fill the configuration using your chosen known values:

```json
{
  "theosis": {
    "stamp": "29:08472119 PES",
    "rotation": 100,
    "band": 1,
    "minute": 0
  }
}
```

Those rotation/band values are an **illustrative configuration only**, not established campaign canon. Band numbers are 1–8 and minute-in-band is 0–1469. The display supplies a numbered rotation, band, and minute relative to your anchor; it does not invent local month names, a year epoch, or civic-period boundaries. Editing the shared anchor changes the optional local display, while raw PES stamps stay fixed.

## Autocomplete

Various Complements can suggest field names and vocabulary from a custom dictionary. Dynamic current-stamp insertion and dependent timing are handled by the commands. To enable optional typing assistance:

1. In Various Complements, enable **Custom dictionary complement**.
2. Add `Campaign/System/PES/PES-Dictionary.txt` to **Custom dictionary paths**, preserving any existing paths.
3. Run its **Reload custom dictionaries** command.

The dictionary contains literal field names, so it needs no custom replacement delimiter. It does not calculate stamps or execute scripts. For a calculated timestamp in prose, use **PES Insert current stamp**. Use **PES Plan scene** for timing metadata. Existing manually typed `[stamp-offset:: 133]` headings can still be read; rerun Initialize to convert them before editing them through the commands. Do not combine that inline field with a PES comment on the same heading.

No Various Complements settings file was present in the uploaded archive, so existing live settings could not be verified. No autocomplete setting is changed by the installer.

## Verification and remaining Obsidian checks

All 24 automated tests passed: 21 JavaScript tests and 3 installer tests. The automated suite tests arithmetic, zero-padding, rollover, invalid values, simultaneous scenes, linked dependencies, loops, deleted references, local anchors, prose-preserving legacy import, session ownership, the finish/retry sequence, and the next session's starting stamp. The command tests use an in-memory Obsidian/Templater mock; renderer tests use a Dataview API mock. They do not substitute for opening the result in Obsidian.

With Node 18 or newer installed, run from the toolkit directory:

```bash
node --test tests/*.test.js
```

The installer needs Python 3.9 or newer and uses only its standard library. Neither Node nor Python is required for the installed commands to run in Obsidian.

Check these once in a copy of your vault before relying on the workflow during a session:

- The registered **Insert PES** commands appear and do not add blank template text or remove a selection.
- Session 1 shows four planned scene rows after migration, with the stamps in the example above; clicking each row reaches its heading.
- Editing a planned scene refreshes the view within the configured Dataview interval. If needed, reopen the note. After changing `core.js`, `view.js`, or `local-time.json`, reopen the note or reload Dataview; external script changes may not trigger a note-index refresh.
- Start, advance 10 minutes, record a scene, and finish in your test copy. The next initialized session starts 10 minutes later. Running Finish again leaves that stamp unchanged.
- Optional dictionary suggestions appear while typing, and any local anchor produces the expected boundary transition.

The source code was checked against the APIs and the plugin versions in your archive: Templater 2.20.6, Dataview 0.5.68, Meta Bind 1.4.15, and Various Complements 11.4.0. Actual UI interaction, OS-specific hotkey conflicts, and live vault sync remain untested here.

## References

- [Templater settings and command registration](https://silentvoid13.github.io/Templater/settings.html)
- [Templater user scripts](https://silentvoid13.github.io/Templater/user-functions/script-user-functions.html)
- [Templater completion hook](https://silentvoid13.github.io/Templater/internal-functions/internal-modules/hooks-module.html)
- [Templater access to the Obsidian API](https://silentvoid13.github.io/Templater/internal-functions/internal-modules/obsidian-module.html)
- [Dataview JavaScript reference](https://blacksmithgu.github.io/obsidian-dataview/api/code-reference/)
- [Various Complements custom dictionaries](https://tadashi-aikawa.github.io/docs-obsidian-various-complements-plugin/1.%20Features/Custom%20dictionary%20complement/)

The campaign protocol and conversion values came from your uploaded Campaign Clock, Time in the Settled Systems, Theosis note, and Session 1 prep. No new calendar anchor has been assumed.