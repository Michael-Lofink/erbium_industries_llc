// Backwards-compatible entry point for Templates/Advance Stamp.md.
// During play, time belongs to the active session and is committed once at Finish.
module.exports = async function advanceStamp(tp) {
  return tp.user.pes(tp, "advance");
};
