<%*
/* =========================================================
   STARFINDER 2E ANCESTRY OUTLINE
   ========================================================= */

function required(value, fieldName) {
    const cleaned = String(value ?? "").trim();

    if (!cleaned) {
        throw new Error(`${fieldName} is required.`);
    }

    return cleaned;
}

function yamlQuote(value) {
    return `"${String(value)
        .replace(/\\/g, "\\\\")
        .replace(/"/g, '\\"')}"`;
}


/* =========================================================
   ANCESTRY IDENTITY
   ========================================================= */

const existingTitle =
    /^Untitled(?: \d+)?$/i.test(tp.file.title)
        ? ""
        : tp.file.title;

const ancestry = required(
    await tp.system.prompt(
        "Ancestry name:",
        existingTitle,
        true
    ),
    "Ancestry name"
);

const rarity = await tp.system.suggester(
    ["Common", "Uncommon", "Rare", "Unique"],
    ["Common", "Uncommon", "Rare", "Unique"],
    true,
    "Select ancestry rarity",
    undefined,
    "Common"
);

const additionalTraitInput = await tp.system.prompt(
    "Additional traits, separated by commas:",
    "Humanoid",
    true
);

const additionalTraits = String(additionalTraitInput ?? "")
    .split(",")
    .map(trait => trait.trim())
    .filter(Boolean);

const allTraits = [
    ...new Set([ancestry, ...additionalTraits])
];

const traitLine = [rarity, ...allTraits]
    .map(trait => `==${trait}==`)
    .join(" ");


/* =========================================================
   PORTRAIT
   ========================================================= */

const imageSlug = ancestry.replace(/[^A-Za-z0-9]+/g, "");

const portrait = required(
    await tp.system.prompt(
        "Portrait filename:",
        `ancestryPortrait_${imageSlug}.png`,
        true
    ),
    "Portrait filename"
);

const imageWidthInput = await tp.system.prompt(
    "Portrait width in pixels:",
    "300",
    true
);

const imageWidth =
    /^\d+$/.test(String(imageWidthInput).trim())
        ? String(imageWidthInput).trim()
        : "300";


/* =========================================================
   BASE MECHANICS
   ========================================================= */

const hitPoints = required(
    await tp.system.prompt(
        "Hit Points:",
        "8",
        true
    ),
    "Hit Points"
);

const size = await tp.system.suggester(
    [
        "Small",
        "Medium",
        "Small or Medium",
        "Large",
        "Tiny"
    ],
    [
        "Small",
        "Medium",
        "Small or Medium",
        "Large",
        "Tiny"
    ],
    true,
    "Select ancestry size",
    undefined,
    "Medium"
);

const speed = required(
    await tp.system.prompt(
        "Speed:",
        "25 feet",
        true
    ),
    "Speed"
);

const attributeBoosts = required(
    await tp.system.prompt(
        "Attribute Boosts:",
        "Free, Free",
        true
    ),
    "Attribute Boosts"
);

const attributeFlaw = required(
    await tp.system.prompt(
        "Attribute Flaw:",
        "None",
        true
    ),
    "Attribute Flaw"
);

const languages = required(
    await tp.system.prompt(
        "Starting languages:",
        "Common",
        true
    ),
    "Languages"
);

const vision = await tp.system.suggester(
    [
        "Low-Light Vision",
        "Darkvision",
        "No vision feature"
    ],
    [
        "Low-Light Vision",
        "Darkvision",
        "None"
    ],
    true,
    "Select vision feature",
    undefined,
    "Low-Light Vision"
);

let visionText = "";

if (vision === "Low-Light Vision") {
    visionText =
        "You can see in dim light as though it were bright light, " +
        "and you ignore the concealed condition due to dim light.";
}

if (vision === "Darkvision") {
    visionText =
        "You can see in darkness and dim light just as well as you can see in bright light, though your vision in darkness is in black and white.";
}


/* =========================================================
   ANCESTRY FEATURES
   ========================================================= */

const featureInput = await tp.system.prompt(
    "Base ancestry feature names, separated by commas:",
    "Ancestry Feature",
    true
);

const featureNames = String(featureInput ?? "")
    .split(",")
    .map(feature => feature.trim())
    .filter(Boolean);


/* =========================================================
   RENAME NOTE
   ========================================================= */

await tp.file.rename(ancestry);


/* =========================================================
   BUILD OPTIONAL SECTIONS
   ========================================================= */

const visionSection =
    vision === "None"
        ? ""
        : `#### ${vision}

${visionText}

`;

let featureCursor = 20;

const featureSections = featureNames
    .map(featureName => {
        const cursor = tp.file.cursor(featureCursor++);
        return `#### ${featureName}

${cursor}

`;
    })
    .join("");


/* =========================================================
   OUTPUT NOTE
   ========================================================= */

tR += `---
type: ancestry
ancestry: ${yamlQuote(ancestry)}
rarity: ${rarity.toLowerCase()}
status: draft
created: ${tp.date.now("YYYY-MM-DD")}
tags:
  - starfinder-2e
  - ancestry
  - settled-systems
---

\`\`\`sf2e-stats
| ${traitLine}
\`\`\`

![[${portrait}#wrapright|${imageWidth}]]

${tp.file.cursor(1)}

If you want to roleplay ${tp.file.cursor(2)}, you should play ${ancestry.toLowerCase().startsWith("a") ? "an" : "a"} ${ancestry.toLowerCase()}.

# You Might...

- ${tp.file.cursor(3)}
- ${tp.file.cursor(4)}
- ${tp.file.cursor(5)}

# Others Probably...

- ${tp.file.cursor(6)}
- ${tp.file.cursor(7)}
- ${tp.file.cursor(8)}

# Physical Description

${tp.file.cursor(9)}

# Society

${tp.file.cursor(10)}

# Beliefs

${tp.file.cursor(11)}

**Popular Edicts** ${tp.file.cursor(12)}

**Popular Anathema** ${tp.file.cursor(13)}

# Sample Names

${tp.file.cursor(14)}

# Other Information
%% Optional setting-specific section. Rename or delete as appropriate. %%
## Place in the Settled Systems
${tp.file.cursor(15)}

# ${ancestry} Mechanics

#### Hit Points

${hitPoints}

#### Size

${size}

#### Speed

${speed}

#### Attribute Boosts

${attributeBoosts}

#### Attribute Flaw

${attributeFlaw}

#### Languages

${languages}

Additional languages equal to 1 + your Intelligence modifier, if it is positive. Choose from the list of common languages and any other languages to which you have access, such as languages prevalent on your home world.

${visionSection}${featureSections}%% Add ancestry-specific rules references and footnotes below. %%

`;
%>