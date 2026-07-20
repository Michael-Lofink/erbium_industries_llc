module.exports = async function advanceStamp(tp) {
    const clockPath = "Campaign/System/Campaign Clock.md";
    const clockFile = app.vault.getAbstractFileByPath(clockPath);

    if (!clockFile) {
        new Notice(`Campaign Clock not found at: ${clockPath}`);
        return;
    }

    const input = await tp.system.prompt(
        "Minutes to advance the Stamp:"
    );

    if (input === null) {
        return;
    }

    const elapsed = Number(input.trim());

    if (!Number.isInteger(elapsed) || elapsed < 0) {
        new Notice("Enter a non-negative whole number of minutes.");
        return;
    }

    try {
        let resultingStamp = "";

        await app.fileManager.processFrontMatter(
            clockFile,
            frontmatter => {
                const lapse = Number(frontmatter.lapse);
                const minute = Number(frontmatter.minute);
                const lapseSize = Number(
                    frontmatter["lapse-size"]
                );

                if (
                    !Number.isInteger(lapse) ||
                    !Number.isInteger(minute) ||
                    !Number.isInteger(lapseSize) ||
                    lapseSize <= 0
                ) {
                    throw new Error(
                        "The Campaign Clock properties are invalid."
                    );
                }

                const total = minute + elapsed;
                const newLapse =
                    lapse + Math.floor(total / lapseSize);
                const newMinute = total % lapseSize;

                frontmatter.lapse = newLapse;
                frontmatter.minute = newMinute;

                const width = String(lapseSize - 1).length;
                resultingStamp =
                    `${newLapse}:` +
                    `${String(newMinute).padStart(width, "0")} PES`;
            }
        );

        new Notice(
            `Advanced the Stamp by ${elapsed} minutes.\n` +
            `Current Stamp: ${resultingStamp}`
        );
    } catch (error) {
        console.error("Advance Stamp failed:", error);
        new Notice(`Advance Stamp failed: ${error.message}`);
    }
};
