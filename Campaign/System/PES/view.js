/* Shared Dataview view. Read-only: rendering never advances or commits time. */
const A = dv.app || globalThis.app;
try {
  const module = { exports: {} };
  new Function("module", "exports", await A.vault.adapter.read("Campaign/System/PES/core.js"))(module, module.exports);
  const C = module.exports, mode = input?.mode || "session", page = dv.current();
  const clock = dv.page(C.CONFIG.clock);
  const stamp = n => n == null ? "—" : C.format(n);
  const link = (e, path) => dv.sectionLink(path, e.raw.replace(/[ \t]+#+[ \t]*$/, ""), false, e.title);
  if (mode === "clock") {
    if (!clock) throw Error("Campaign Clock note is missing.");
    dv.header(3, C.format(C.clockNow(clock)));
    dv.paragraph(clock["pes-active-id"] ? `Session in progress: ${clock["pes-active-path"]}. This is its committed starting stamp; the session note shows live time.` : "Committed campaign time.");
    dv.table(["Minutes per lapse", "Last completed session", "Synchronization"], [[C.SIZE, clock["last-session"] ?? 0, clock["sync-status"] ?? "unspecified"]]);
  } else if (mode === "campaign") {
    const pages = dv.pages('"Campaign/Sessions"').where(p => p.type === "session").array().sort((a,b) => Number(a.session) - Number(b.session));
    const rows = [];
    for (const p of pages) {
      try {
        const start = C.sessionStart(p), status = p["stamp-status"] ?? "legacy / uninitialized";
        const planned = C.integer(p["stamp-planned-minutes"] ?? p["elapsed-minutes"] ?? 0, "Planned minutes");
        const actual = p["stamp-actual-minutes"] == null ? null : C.sessionNow(p);
        rows.push([p.file.link, status, stamp(start), stamp(C.add(start, planned)), stamp(actual)]);
      } catch (e) { rows.push([p.file.link, `Invalid: ${e.message}`, "—", "—", "—"]); }
    }
    dv.table(["Session", "Status", "Start", "Planned end", "Actual current / end"], rows);
  } else {
    const start = C.sessionStart(page), now = C.sessionNow(page);
    const path = page.file.path, text = await dv.io.load(path);
    if (typeof text !== "string") throw Error("Session note could not be read.");
    const body = C.split(text, () => ({})).body;
    const events = C.resolve(body, page);
    if (mode !== "timeline") {
      const planned = C.integer(page["stamp-planned-minutes"] ?? page["elapsed-minutes"] ?? 0, "Planned minutes");
      dv.table(["Start", "Planned duration / end", "Actual elapsed / current", "Status"], [[stamp(start), `${planned} min · ${stamp(C.add(start, planned))}`, `${C.actualMinutes(page)} min · ${stamp(now)}`, page["stamp-status"] ?? "legacy / uninitialized"]]);
      const sync = page["stamp-sync-status"] ?? "unspecified";
      dv.paragraph(`Relay status: **${sync}**. Time advances only when you run a PES command.`);
      const lastAuth = sync === "on-stamp" ? now : page["stamp-last-auth-total"];
      if (lastAuth != null) dv.paragraph(`Last authenticated stamp: ${stamp(lastAuth)}.`);
      if (page["stamp-local-calendar"] === "theosis") {
        const config = JSON.parse(await A.vault.adapter.read("Campaign/System/PES/local-time.json"));
        const local = C.localTheosis(now, config.theosis);
        dv.paragraph(local ? `Theosis: rotation ${local.rotation}, band ${local.band}, minute ${local.minute} (relative to your configured anchor).` : "Theosis local display needs an anchor: a known PES stamp paired with a rotation, band, and minute. No local date has been assumed.");
      }
      if (page["stamp-status"] === "closing") dv.paragraph("**Finish was interrupted. Run PES Finish session again to recover.**");
      if (page["stamp-status"] === "prep" && clock && C.clockNow(clock) !== start) dv.paragraph("**This planned start differs from the campaign clock. Reconcile it before starting play.**");
    }
    if (mode !== "summary") {
      dv.header(3, "Planned scenes");
      const planned = C.sorted(events, "planned");
      if (!planned.length) dv.paragraph("No planned scenes. Run PES Plan scene to add one.");
      else dv.table(["PES stamp", "Offset", "Scene", "Timing"], planned.map(e => [stamp(e.planned), `${e.planned-start >= 0 ? "+" : ""}${e.planned-start} min`, link(e,path), e.plan.kind === "after" ? `${e.plan.minutes} min after ${events.find(x=>x.id===e.plan.scene)?.title}` : e.plan.kind === "absolute" ? "Fixed PES stamp" : "Fixed session offset"]));
      dv.header(3, "Actual scenes");
      const actual = C.sorted(events, "actual");
      if (!actual.length) dv.paragraph("No actual scene times recorded yet.");
      else dv.table(["PES stamp", "Scene", "Difference from plan", "Relay status"], actual.map(e => [stamp(e.actual), link(e,path), e.planned == null ? "—" : `${e.actual-e.planned >= 0 ? "+" : ""}${e.actual-e.planned} min`, e.sync ?? "unspecified"]));
    }
  }
} catch (e) {
  dv.paragraph(`**PES error:** ${e.message}`);
}
