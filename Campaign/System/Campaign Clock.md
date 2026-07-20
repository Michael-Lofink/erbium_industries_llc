---
type: campaign-clock
lapse: 29
minute: 8472119
lapse-size: 16777216
last-session: 0
---

# Campaign Clock

```dataviewjs
const clock = dv.current();

const lapse = Number(clock.lapse);
const minute = Number(clock.minute);
const lapseSize = Number(clock["lapse-size"]);

if (
    !Number.isInteger(lapse) ||
    !Number.isInteger(minute) ||
    !Number.isInteger(lapseSize) ||
    lapseSize <= 0
) {
    dv.paragraph(
        "> [!failure] Invalid Campaign Clock\n" +
        "> Check the `lapse`, `minute`, and `lapse-size` properties."
    );
} else {
    const width = String(lapseSize - 1).length;
    const formattedMinute = String(minute).padStart(width, "0");

    dv.paragraph(
        "> [!clock] Current Post-Erbium Stamp\n" +
        `> **${lapse}:${formattedMinute} PES**`
    );
}
```

## Clock Configuration

- **Current lapse:** `29`
- **Current minute:** `8472119`
- **Minutes per lapse:** `16777216`
- **Last completed session:** `0`
