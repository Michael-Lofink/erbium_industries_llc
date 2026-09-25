/* PES Toolkit 1.0.0 — shared pure logic. CommonJS; no Obsidian dependency. */
"use strict";
const SIZE = 16777216;
const CONFIG = Object.freeze({ clock: "Campaign/System/Campaign Clock.md", sessions: "Campaign/Sessions/", view: "Campaign/System/PES/view" });
function integer(value, label, min = 0) {
  if ((typeof value !== "number" && typeof value !== "string") || String(value).trim() === "" || !/^-?\d+$/.test(String(value).trim())) throw Error(`${label} must be a whole number.`);
  const n = Number(value);
  if (!Number.isSafeInteger(n) || n < min) throw Error(`${label} must be a safe whole number ≥ ${min}.`);
  return n;
}
function size(value = SIZE) {
  const n = integer(value, "Lapse size", 1);
  if (n !== SIZE) throw Error(`This PES protocol requires ${SIZE} minutes per lapse.`);
  return n;
}
function total(lapse, minute, limit = SIZE) {
  size(limit);
  const l = integer(lapse, "Lapse"), m = integer(minute, "Minute");
  if (m >= limit) throw Error(`Minute must be between 0 and ${limit - 1}.`);
  const n = l * limit + m;
  if (!Number.isSafeInteger(n)) throw Error("Stamp exceeds safe integer range.");
  return n;
}
function parts(value, limit = SIZE) {
  size(limit); const n = integer(value, "Absolute minute");
  return { lapse: Math.floor(n / limit), minute: n % limit };
}
function format(value, limit = SIZE) {
  const p = parts(value, limit);
  return `${p.lapse}:${String(p.minute).padStart(8, "0")} PES`;
}
function parseStamp(value, limit = SIZE) {
  const m = String(value).trim().match(/^(\d+):(\d{1,8})(?:\s+PES)?$/i);
  if (!m) throw Error("Use Lapse:Minute PES, for example 29:08472119 PES.");
  return total(m[1], m[2], limit);
}
function add(value, delta) {
  const n = integer(value, "Stamp") + integer(delta, "Minutes", -Number.MAX_SAFE_INTEGER);
  return integer(n, "Resulting stamp");
}
function duration(value, signed = false) {
  const m = String(value).trim().match(/^([+-]?\d+)\s*(m|min|minutes?|h|hours?|d|days?|band|bands|rotation|rotations)?$/i);
  if (!m) throw Error("Enter whole units, e.g. 10, 2h, 1d, 1 band, or 1 rotation.");
  const factors = { m:1, min:1, minute:1, minutes:1, h:60, hour:60, hours:60, d:1440, day:1440, days:1440, band:1470, bands:1470, rotation:11760, rotations:11760 };
  const n = Number(m[1]) * factors[(m[2] || "m").toLowerCase()];
  return integer(n, "Duration", signed ? -Number.MAX_SAFE_INTEGER : 0);
}
function sessionStart(fm) { return total(fm["stamp-start-lapse"], fm["stamp-start-minute"], fm["stamp-lapse-size"] ?? SIZE); }
function clockNow(fm) { return total(fm.lapse, fm.minute, fm["lapse-size"]); }
function actualMinutes(fm) { return integer(fm["stamp-actual-minutes"] ?? 0, "Actual elapsed minutes"); }
function sessionNow(fm) { return add(sessionStart(fm), actualMinutes(fm)); }
function uid() { return `pes-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`; }
function split(text, parseYaml) {
  const m = text.match(/^\uFEFF?---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  return { fm: m ? (parseYaml(m[1]) || {}) : {}, body: m ? text.slice(m[0].length) : text, prefix: m ? m[0] : "", newline: text.includes("\r\n") ? "\r\n" : "\n" };
}
function join(doc, fm, stringifyYaml) { return `---${doc.newline}${stringifyYaml(fm).trimEnd().replace(/\r?\n/g, doc.newline)}${doc.newline}---${doc.newline}${doc.body}`; }
function headings(body) {
  const lines = body.split(/\r?\n/); let fence = null, inComment = false; const out = [];
  lines.forEach((line, index) => {
    const f = line.match(/^ {0,3}(`{3,}|~{3,})/);
    if (f && !inComment) {
      if (!fence) fence = f[1];
      else if (f[1][0] === fence[0] && f[1].length >= fence.length && /^\s*$/.test(line.slice(line.indexOf(f[1]) + f[1].length))) fence = null;
      return;
    }
    if (fence) return;
    if (inComment) { if (line.includes("-->")) inComment = false; return; }
    if (line.trimStart().startsWith("<!--")) { inComment = !line.includes("-->"); return; }
    const h = line.match(/^(#{1,6})[ \t]+(.+?)[ \t]*$/);
    if (h) out.push({ line: index, level: h[1], raw: h[2], title: h[2].replace(/[ \t]+#+[ \t]*$/, "").replace(/\s*\[stamp-offset::[^\]]*\]/g, "").trim() });
  });
  return out;
}
function scenes(body) {
  const lines = body.split(/\r?\n/); const ids = new Set(); const out = [];
  for (const h of headings(body)) {
    const inline = h.raw.match(/\[stamp-offset::\s*([^\]]*)\]/);
    const next = lines[h.line + 1] || "";
    const match = next.match(/^\s*<!-- pes: (.+) -->\s*$/);
    if (next.includes("<!-- pes:") && !match) throw Error(`Malformed PES metadata under ${h.title}.`);
    if (!match && !inline) continue;
    let data;
    if (match) {
      try { data = JSON.parse(match[1]); } catch { throw Error(`Invalid PES JSON under ${h.title}.`); }
      if (!data || typeof data !== "object" || Array.isArray(data) || typeof data.id !== "string" || !/^pes-[a-z0-9-]+$/i.test(data.id)) throw Error(`Invalid scene ID under ${h.title}.`);
      if (inline) throw Error(`Two planned timings on ${h.title}; remove the old stamp-offset field.`);
    } else data = { id: `legacy-${h.line}`, plan: { kind: "offset", minutes: integer(inline[1].trim(), "Scene offset", -Number.MAX_SAFE_INTEGER) } };
    if (ids.has(data.id)) throw Error(`Duplicate scene ID ${data.id}.`);
    ids.add(data.id); out.push({ ...h, ...data, legacy: !match });
  }
  return out;
}
function resolve(body, fm) {
  const entries = scenes(body), start = sessionStart(fm), map = new Map(entries.map(e => [e.id, e]));
  const cache = new Map(), visiting = new Set();
  function at(id) {
    if (cache.has(id)) return cache.get(id);
    const e = map.get(id);
    if (!e) throw Error(`Referenced scene ${id} is missing.`);
    if (visiting.has(id)) throw Error(`Circular scene timing involving ${e.title}.`);
    visiting.add(id); let n = null; const p = e.plan;
    if (p) {
      if (p.kind === "offset") n = add(start, integer(p.minutes, "Scene offset", -Number.MAX_SAFE_INTEGER));
      else if (p.kind === "absolute") { n = integer(p.total, "Absolute scene stamp"); parts(n); }
      else if (p.kind === "after") {
        const reference = at(p.scene);
        if (reference === null) throw Error(`Reference scene has no planned time: ${p.scene}.`);
        n = add(reference, integer(p.minutes, "Minutes after scene"));
      } else throw Error(`Unknown timing mode on ${e.title}.`);
    }
    visiting.delete(id); cache.set(id, n); return n;
  }
  const titles = new Set();
  return entries.map(e => {
    // Heading links cannot distinguish identical heading text. Refuse ambiguous links.
    if (titles.has(e.raw)) throw Error(`Duplicate stamped heading "${e.title}". Give these headings distinct names.`);
    titles.add(e.raw);
    const actual = e.actual == null ? null : integer(e.actual, `Actual stamp for ${e.title}`);
    if (actual !== null && (actual < start || actual > sessionNow(fm))) throw Error(`Actual time for ${e.title} is outside the session's elapsed time.`);
    return { ...e, planned: at(e.id), actual };
  });
}
function sorted(events, key) { return [...events].filter(e => e[key] !== null).sort((a,b) => a[key] - b[key] || a.line - b.line); }
function putScene(body, line, data) {
  const lines = body.split(/\r?\n/), nl = body.includes("\r\n") ? "\r\n" : "\n";
  if (!headings(body).some(h => h.line === line)) throw Error("Selected heading no longer exists.");
  lines[line] = lines[line].replace(/\s*\[stamp-offset::[^\]]*\]/g, "");
  const metadata = `<!-- pes: ${JSON.stringify(data)} -->`;
  if (/^\s*<!-- pes:/.test(lines[line + 1] || "")) lines[line + 1] = metadata;
  else lines.splice(line + 1, 0, metadata);
  return lines.join(nl);
}
function importLegacy(body, idFactory = uid) {
  for (const e of scenes(body).filter(e => e.legacy).reverse()) body = putScene(body, e.line, { id: idFactory(), plan: e.plan });
  return body;
}
function assertEditable(fm) {
  if (["closing","completed"].includes(fm["stamp-status"])) throw Error("This session is closing or completed. Its record is locked to PES commands.");
}
function initialize(fm, clock, id = uid()) {
  size(clock["lapse-size"]); const now = clockNow(clock);
  const out = { ...fm }; assertEditable(out);
  const hasStart = out["stamp-start-lapse"] != null || out["stamp-start-minute"] != null;
  if (hasStart) sessionStart(out); // Never overwrite a stored historical start.
  else { const p = parts(now); out["stamp-start-lapse"] = p.lapse; out["stamp-start-minute"] = p.minute; }
  out.type = "session";
  out["stamp-session-id"] ??= id;
  out["stamp-lapse-size"] ??= SIZE;
  out["stamp-status"] ??= "prep";
  out["stamp-planned-minutes"] ??= integer(out["elapsed-minutes"] ?? 0, "Planned elapsed minutes");
  out["stamp-actual-minutes"] ??= 0;
  out["stamp-sync-status"] ??= clock["sync-status"] ?? "unspecified";
  if (out["stamp-last-auth-total"] == null && clock["last-auth-total"] != null) out["stamp-last-auth-total"] = integer(clock["last-auth-total"], "Last authenticated stamp");
  return out;
}
function claim(clock, fm, path) {
  if (fm["stamp-status"] !== "prep" && fm["stamp-status"] !== "active") throw Error("Initialize this session first.");
  const id = fm["stamp-session-id"];
  if (!id) throw Error("Session ID is missing.");
  if (clock["pes-active-id"] && (clock["pes-active-id"] !== id || clock["pes-active-path"] !== path)) throw Error(`Another session owns the clock: ${clock["pes-active-path"]}. Finish that session first.`);
  if (clockNow(clock) !== sessionStart(fm)) throw Error("Session start differs from the campaign clock. Use a fresh session note, or reconcile its start before play.");
  return { ...clock, "pes-active-id": id, "pes-active-path": path };
}
function assertActive(clock, fm, path) {
  if (fm["stamp-status"] !== "active") throw Error("Run Start session before advancing or recording actual time.");
  if (clock["pes-active-id"] !== fm["stamp-session-id"] || (path && clock["pes-active-path"] !== path)) throw Error("This session does not own the campaign clock.");
  if (clockNow(clock) !== sessionStart(fm)) throw Error("Campaign clock changed during this session. Reconcile it before continuing.");
}
function closing(fm, body) {
  const events = resolve(body, fm);
  const end = sessionNow(fm), p = parts(end);
  if (events.some(e => e.actual !== null && e.actual > end)) throw Error("A recorded scene occurs after the session ending.");
  return { ...fm, "stamp-status": "closing", "stamp-end-lapse": p.lapse, "stamp-end-minute": p.minute, "stamp-commit-id": fm["stamp-session-id"] };
}
function commit(clock, fm) {
  if (fm["stamp-status"] !== "closing") throw Error("Session has no pending finish operation.");
  const id = fm["stamp-commit-id"];
  if (!id || id !== fm["stamp-session-id"]) throw Error("Invalid finish operation ID.");
  const end = total(fm["stamp-end-lapse"], fm["stamp-end-minute"]);
  if (end !== sessionNow(fm)) throw Error("Ending stamp changed during finish. Restore the recorded session values.");
  if (clock["pes-last-commit-id"] === id) {
    if (clockNow(clock) !== end) throw Error("Campaign clock changed after a partial finish. Restore the recorded ending stamp before retrying.");
    return { ...clock }; // Idempotent retry after the clock write.
  }
  if (clock["pes-active-id"] !== fm["stamp-session-id"] || clockNow(clock) !== sessionStart(fm)) throw Error("Campaign clock conflicts with this session. No clock change was made.");
  const p = parts(end);
  return { ...clock, lapse: p.lapse, minute: p.minute, "pes-last-commit-id": id, "sync-status": fm["stamp-sync-status"] ?? "unspecified", "last-auth-total": fm["stamp-sync-status"] === "on-stamp" ? end : (fm["stamp-last-auth-total"] ?? null), "last-session": integer(fm.session, "Session number", 1) };
}
function completed(fm) { return { ...fm, "stamp-status": "completed", "elapsed-minutes": actualMinutes(fm) }; }
function release(clock, fm) {
  const out = { ...clock };
  if (out["pes-active-id"] === fm["stamp-session-id"] && out["pes-last-commit-id"] === fm["stamp-session-id"]) { delete out["pes-active-id"]; delete out["pes-active-path"]; }
  return out;
}
function localTheosis(stamp, anchor) {
  if (!anchor) return null;
  const epoch = parseStamp(anchor.stamp), rotation = integer(anchor.rotation, "Anchor rotation");
  const band = integer(anchor.band, "Anchor band", 1), minute = integer(anchor.minute, "Anchor band minute");
  if (band > 8 || minute >= 1470) throw Error("Anchor band must be 1–8 and band minute 0–1469.");
  const n = rotation * 11760 + (band - 1) * 1470 + minute + (stamp - epoch);
  integer(n, "Local time");
  return { rotation: Math.floor(n / 11760), band: Math.floor((n % 11760) / 1470) + 1, minute: n % 1470 };
}
module.exports = { SIZE, CONFIG, integer, size, total, parts, format, parseStamp, add, duration, sessionStart, clockNow, actualMinutes, sessionNow, uid, split, join, headings, scenes, resolve, sorted, putScene, importLegacy, assertEditable, initialize, claim, assertActive, closing, commit, completed, release, localTheosis };
