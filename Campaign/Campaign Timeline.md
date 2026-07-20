```dataviewjs
const clock = dv.page("Campaign/System/Campaign Clock");

if (!clock) {
    dv.paragraph(
        "> [!failure] Campaign Clock not found\n" +
        "> Confirm that the clock is located at `Campaign/System/Campaign Clock.md`."
    );
} else {
    const limit = Number(clock["lapse-size"]);
    const width = String(limit - 1).length;

    function formatStamp(lapse, minute) {
        return `${lapse}:${String(minute).padStart(width, "0")} PES`;
    }

    function endStamp(page) {
        const startLapse = Number(page["stamp-start-lapse"]);
        const startMinute = Number(page["stamp-start-minute"]);
        const elapsed = Number(page["elapsed-minutes"] ?? 0);

        const total = startMinute + elapsed;

        return formatStamp(
            startLapse + Math.floor(total / limit),
            total % limit
        );
    }

    const sessions = dv.pages('"Campaign/Sessions"')
        .where(page => page.type === "session")
        .where(page =>
            page["stamp-start-lapse"] != null &&
            page["stamp-start-minute"] != null
        )
        .sort(page => Number(page.session), "asc");

    dv.table(
        ["Session", "Start Stamp", "Elapsed", "End Stamp"],
        sessions.map(page => [
            page.file.link,
            formatStamp(
                Number(page["stamp-start-lapse"]),
                Number(page["stamp-start-minute"])
            ),
            `${Number(page["elapsed-minutes"] ?? 0)} minutes`,
            endStamp(page)
        ])
    );
}
```