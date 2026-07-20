---
type: session
session: 1
stamp-start-lapse: 29
stamp-start-minute: 8472119
elapsed-minutes: 386
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

## Timeline

- Shift briefing begins. [stamp-offset:: 0]
- The mining vessel departs. [stamp-offset:: 38]
- Long-range communications fail. [stamp-offset:: 127]
- The crew discovers the abandoned relay. [stamp-offset:: 241]
- The Erbium vessel abandons the crew. [stamp-offset:: 318]

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

    const lists = dv.array(session.file.lists ?? []);

    const events = lists
        .where(item => item["stamp-offset"] != null)
        .sort(item => Number(item["stamp-offset"]), "asc")
        .map(item => {
            const cleanText = item.text
                .replace(/\[stamp-offset::\s*\d+\s*\]/g, "")
                .trim();

            return [
                addMinutes(item["stamp-offset"]),
                cleanText
            ];
        });

    if (events.length === 0) {
        dv.paragraph(
            "*No stamped events have been recorded for this session.*"
        );
    } else {
        dv.table(["Stamp", "Event"], events);
    }
}
```