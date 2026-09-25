/* Templater entry point. Templates preserve selection and defer writes until insertion finishes. */
module.exports = async function pes(tp, action = "menu") {
  const app = tp.app;
  const { Notice, parseYaml, stringifyYaml, MarkdownView } = tp.obsidian;
  const origin = tp.config.target_file;
  const loader = { exports: {} };
  new Function("module", "exports", await app.vault.adapter.read("Campaign/System/PES/core.js"))(loader, loader.exports);
  const C = loader.exports;
  let fired = false;
  tp.hooks.on_all_templates_executed(async () => {
    if (fired) return; fired = true;
    if (app.__pesBusy) { new Notice("Another PES command is open. Complete or cancel it first."); return; }
    app.__pesBusy = true;
    try { await run(action); } catch (e) { console.error("PES", e); new Notice(`PES: ${e.message}`, 10000); }
    finally { app.__pesBusy = false; }
  });
  function file(path) {
    const f = app.vault.getAbstractFileByPath(path);
    if (!f || f.extension !== "md") throw Error(`Markdown note not found: ${path}`);
    return f;
  }
  async function read(f) { const text = await app.vault.read(f); return { ...C.split(text, parseYaml), text }; }
  async function write(f, before, fm, body = before.body) {
    const result = C.join({ ...before, body }, fm, stringifyYaml);
    await app.vault.process(f, current => {
      if (current !== before.text) throw Error(`Note changed while the command was open: ${f.path}. Run it again.`);
      return result;
    });
  }
  async function clock() { return read(file(C.CONFIG.clock)); }
  async function changeClock(fn) {
    const f = file(C.CONFIG.clock), d = await read(f); await write(f, d, fn(d.fm));
  }
  async function prompt(label, initial = "") { const v = await tp.system.prompt(label, initial); return v == null ? null : v; }
  async function choose(label, items) { return tp.system.suggester(items.map(x => x.label), items, false, label); }
  function snippet(mode) { return '```dataviewjs\nawait dv.view("Campaign/System/PES/view", {mode: "' + mode + '"});\n```'; }
  function upgradeViews(body) {
    let changed = false;
    body = body.replace(/```dataviewjs\r?\n[\s\S]*?```/g, block => {
      if (!block.includes('dv.page("Campaign/System/Campaign Clock")') || !block.includes("const session = dv.current()")) return block;
      changed = true;
      return snippet(block.includes("headingPattern") ? "timeline" : "summary");
    });
    if (!changed && !body.includes('dv.view("Campaign/System/PES/view"')) body += '\n\n## PES Clock and Timeline\n\n' + snippet("session") + '\n';
    return body;
  }
  async function session(requireActive = false) {
    if (!origin || !origin.path.startsWith(C.CONFIG.sessions)) throw Error(`Open a session note inside ${C.CONFIG.sessions} first.`);
    const d = await read(origin);
    if (!d.fm["stamp-session-id"]) throw Error("Run Initialize session first.");
    C.sessionStart(d.fm);
    if (requireActive) C.assertActive((await clock()).fm, d.fm, origin.path);
    return d;
  }
  async function initialize() {
    if (!origin || !origin.path.startsWith(C.CONFIG.sessions)) throw Error(`Create/open a note in ${C.CONFIG.sessions} first.`);
    const d = await read(origin), c = await clock();
    if (d.fm.type && d.fm.type !== "session") throw Error("This note has a different type property.");
    const n = d.fm.session ?? await prompt("Session number (positive whole number)");
    if (n === null) return;
    const fm = C.initialize({ ...d.fm, session: C.integer(n, "Session number", 1) }, c.fm);
    const body = upgradeViews(C.importLegacy(d.body)); C.resolve(body, fm);
    await write(origin, d, fm, body);
    new Notice(`Session initialized at ${C.format(C.sessionStart(fm))}. Actual elapsed time: ${C.actualMinutes(fm)} minutes.`);
  }
  async function start() {
    const d = await session();
    await changeClock(c => C.claim(c, d.fm, origin.path));
    await write(origin, d, { ...d.fm, "stamp-status": "active" });
    new Notice("Session active. Advance time here; the campaign clock is committed at Finish session.");
  }
  function metadata(e) {
    const out = { id: e?.id || C.uid() };
    if (e?.plan) out.plan = e.plan;
    if (e?.actual != null) out.actual = e.actual;
    if (e?.sync) out.sync = e.sync;
    return out;
  }
  async function pickHeading(d, allowNew = true) {
    const hs = C.headings(d.body);
    const items = hs.map(h => ({ label: `${h.level} ${h.title}`, h }));
    if (allowNew) items.unshift({ label: "+ Add a new scene at the end of this note", add: true });
    const selected = await choose("Choose a scene heading", items);
    if (!selected) return null;
    if (!selected.add) return { body: d.body, h: selected.h };
    const title = await prompt("New scene heading");
    if (title === null) return null;
    if (!title.trim() || /[\r\n]|<!--|\[stamp-offset::/.test(title)) throw Error("Enter a plain, non-empty scene title.");
    const nl = d.newline, body = d.body + `${nl}${nl}## ${title.trim()}${nl}`;
    return { body, h: C.headings(body).at(-1) };
  }
  async function planScene() {
    const d = await session(); C.assertEditable(d.fm);
    const target = await pickHeading(d); if (!target) return;
    const existing = C.scenes(target.body).find(e => e.line === target.h.line);
    const m = metadata(existing);
    const kind = await choose("How is this scene timed?", [
      { label: "Offset from session start (e.g. 133, 2h; negative offsets allowed)", kind: "offset" },
      { label: "Absolute PES stamp (fixed timestamp)", kind: "absolute" },
      { label: "Minutes after another scene (moves with that scene)", kind: "after" },
      { label: "Remove planned timing (keep actual record)", kind: "clear" }
    ]); if (!kind) return;
    if (kind.kind === "clear") delete m.plan;
    else if (kind.kind === "absolute") {
      const value = await prompt("PES stamp", existing?.plan?.kind === "absolute" ? C.format(existing.plan.total) : C.format(C.sessionStart(d.fm)));
      if (value === null) return; m.plan = { kind: "absolute", total: C.parseStamp(value) };
    } else if (kind.kind === "offset") {
      const value = await prompt("Offset from session start (minutes, h, d, band, rotation)", String(existing?.plan?.kind === "offset" ? existing.plan.minutes : 0));
      if (value === null) return; m.plan = { kind: "offset", minutes: C.duration(value, true) };
    } else {
      const refs = C.resolve(target.body, d.fm).filter(e => e.id !== m.id && e.planned !== null);
      if (!refs.length) throw Error("Stamp a reference scene first.");
      const ref = await choose("Choose the scene this one follows", refs.map(e => ({ label: `${e.title} — ${C.format(e.planned)}`, e })));
      if (!ref) return;
      const value = await prompt("Duration after that scene's planned START (0 means simultaneous)", "0");
      if (value === null) return;
      m.plan = { kind: "after", scene: ref.e.id, minutes: C.duration(value) };
    }
    const body = C.putScene(target.body, target.h.line, m); C.resolve(body, d.fm);
    await write(origin, d, d.fm, body); new Notice("Planned timeline updated.");
  }
  async function advance(set = false) {
    const d = await session(true), current = C.actualMinutes(d.fm);
    const value = await prompt(set ? "Set actual elapsed time since session start" : "Time elapsed in the fiction (e.g. 10, 2h, 1d)", set ? String(current) : "10");
    if (value === null) return;
    const amount = C.duration(value), elapsed = set ? amount : C.integer(current + amount, "Actual elapsed minutes");
    const fm = { ...d.fm, "stamp-actual-minutes": elapsed };
    C.resolve(d.body, fm); C.assertActive((await clock()).fm, d.fm, origin.path);
    await write(origin, d, fm); new Notice(`Session time: ${C.format(C.sessionNow(fm))}`);
  }
  async function record() {
    const d = await session(true), target = await pickHeading(d); if (!target) return;
    const e = C.scenes(target.body).find(e => e.line === target.h.line), m = metadata(e);
    const selection = await choose("Record actual scene time", [
      { label: `Now — ${C.format(C.sessionNow(d.fm))}`, mode: "now" },
      { label: "Earlier in this session — enter elapsed time", mode: "earlier" },
      { label: "Clear this scene's actual time", mode: "clear" }
    ]); if (!selection) return;
    if (selection.mode === "clear") { delete m.actual; delete m.sync; }
    else {
      let n = C.actualMinutes(d.fm);
      if (selection.mode === "earlier") {
        const v = await prompt("Elapsed time from session start", "0"); if (v === null) return;
        n = C.duration(v); if (n > C.actualMinutes(d.fm)) throw Error("Advance the session clock before recording a future event.");
      }
      m.actual = C.add(C.sessionStart(d.fm), n);
      if (selection.mode === "earlier") {
        const sync = await choose("Synchronization status when this earlier event happened", ["unspecified", "on-stamp", "off-stamp"].map(v => ({label:v})));
        if (!sync) return; m.sync = sync.label;
      } else m.sync = d.fm["stamp-sync-status"] ?? "unspecified";
    }
    const body = C.putScene(target.body, target.h.line, m); C.resolve(body, d.fm);
    C.assertActive((await clock()).fm, d.fm, origin.path);
    await write(origin, d, d.fm, body); new Notice("Actual scene record updated.");
  }
  async function finish() {
    let d = await session();
    const owner = (await clock()).fm;
    if (owner["pes-active-id"] === d.fm["stamp-session-id"] && owner["pes-active-path"] !== origin.path) throw Error("This appears to be a copy of the active session. Open the original session note.");
    if (d.fm["stamp-status"] === "completed") {
      await changeClock(c => C.release(c, d.fm)); new Notice("Session already finished. No time added."); return;
    }
    if (d.fm["stamp-status"] !== "closing") {
      C.assertActive((await clock()).fm, d.fm, origin.path);
      const fm = C.closing(d.fm, d.body);
      const ok = await choose(`Finish with ${C.actualMinutes(fm)} actual minutes at ${C.format(C.sessionNow(fm))}?`, [{label:"Finish session", yes:true},{label:"Cancel",yes:false}]);
      if (!ok?.yes) return;
      C.assertActive((await clock()).fm, d.fm, origin.path);
      await write(origin, d, fm); d = await read(origin);
    }
    // Durable intent is written before the campaign clock. Retrying Finish recovers interrupted writes.
    await changeClock(c => C.commit(c, d.fm));
    await write(origin, d, C.completed(d.fm));
    await changeClock(c => C.release(c, d.fm));
    new Notice(`Session finished at ${C.format(C.sessionNow(d.fm))}. You can initialize the next session.`);
  }
  async function synchronization() {
    const d = await session(true);
    const result = await choose("Relay synchronization status", ["on-stamp", "off-stamp", "unspecified"].map(label => ({label})));
    if (!result) return;
    const fm = { ...d.fm, "stamp-sync-status": result.label };
    if (d.fm["stamp-sync-status"] === "on-stamp" && result.label !== "on-stamp") fm["stamp-last-auth-total"] = C.sessionNow(d.fm);
    C.assertActive((await clock()).fm, d.fm, origin.path);
    await write(origin, d, fm); new Notice(`Synchronization: ${result.label}. Elapsed time is unchanged.`);
  }
  async function insert() {
    const d = await session(); const view = app.workspace.getActiveViewOfType(MarkdownView);
    if (!view || view.file?.path !== origin.path) throw Error("Return to the session editor and run the command again.");
    if (d.fm["stamp-status"] === "prep") throw Error("Start the session before inserting its current actual stamp.");
    view.editor.replaceSelection(C.format(C.sessionNow(d.fm)));
  }
  async function plannedDuration() {
    const d = await session(); C.assertEditable(d.fm);
    const v = await prompt("Planned session duration", String(d.fm["stamp-planned-minutes"] ?? 0));
    if (v === null) return;
    await write(origin, d, { ...d.fm, "stamp-planned-minutes": C.duration(v) });
  }
  async function upgrade() {
    const f = file(C.CONFIG.clock), d = await read(f);
    C.clockNow(d.fm);
    let body = d.body.replace(/```dataviewjs\r?\n[\s\S]*?```/g, block => block.includes("const clock = dv.current()") ? snippet("clock") : block);
    if (!body.includes('dv.view("Campaign/System/PES/view"')) body += '\n\n' + snippet("clock") + '\n';
    body = body.replace(/^-(?: \*\*(?:Current lapse|Current minute|Minutes per lapse|Last completed session):\*\*).*\r?\n?/gm, "");
    await write(f, d, d.fm, body);
    const tf = file("Campaign/Campaign Timeline.md"), td = await read(tf);
    let tb = td.body.replace(/```dataviewjs\r?\n[\s\S]*?```/g, block => block.includes('dv.pages(\'"Campaign/Sessions"\')') && block.includes("function endStamp") ? snippet("campaign") : block);
    if (!tb.includes('dv.view("Campaign/System/PES/view"')) tb += '\n\n' + snippet("campaign") + '\n';
    await write(tf, td, td.fm, tb);
    new Notice("Campaign Clock and Campaign Timeline now use the shared PES view.");
  }
  async function check() {
    const d = await session(), c = await clock(); const events = C.resolve(d.body, d.fm);
    C.clockNow(c.fm);
    if (d.fm["stamp-status"] === "active") C.assertActive(c.fm, d.fm, origin.path);
    new Notice(`PES valid: ${events.length} scenes; ${C.format(C.sessionStart(d.fm))} → ${C.format(C.sessionNow(d.fm))}. Status: ${d.fm["stamp-status"]}.`, 10000);
  }
  async function run(selectedAction) {
    const commands = [
      ["initialize", "Initialize session / upgrade existing prep"], ["plan", "Add or edit planned scene"],
      ["start", "Start session"], ["advance", "Advance time"], ["record", "Record actual scene time"],
      ["insert", "Insert current stamp"], ["set", "Correct actual elapsed time"],
      ["sync", "Set synchronization status"], ["duration", "Set planned session duration"],
      ["finish", "Finish session / recover interrupted finish"], ["check", "Check session"],
      ["upgrade", "Upgrade campaign clock and timeline displays"]
    ];
    if (selectedAction === "menu") {
      const result = await choose("PES timekeeping", commands.map(([id,label]) => ({id,label})));
      if (!result) return; selectedAction = result.id;
    }
    const handlers = { initialize, plan:planScene, start, advance:()=>advance(), set:()=>advance(true), record, insert, sync:synchronization, duration:plannedDuration, finish, check, upgrade };
    if (!handlers[selectedAction]) throw Error(`Unknown PES command: ${selectedAction}`);
    await handlers[selectedAction]();
  }
};
