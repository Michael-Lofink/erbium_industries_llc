/* Pure parsing and rendering; shared by the Obsidian plugin and its tests. */
'use strict';
const ROOT = 'Worldbuilding/Settled Systems Code';
const INDEX = `${ROOT}/Code Index.md`, INBOX = `${ROOT}/Code Inbox.md`;
const BEGIN = '<!-- ssac:references:start -->', END = '<!-- ssac:references:end -->';
const CBEGIN = '<!-- ssac:catalog:start -->', CEND = '<!-- ssac:catalog:end -->';
const IBEGIN = '<!-- ssac:inbox:start -->', IEND = '<!-- ssac:inbox:end -->';
const TITLES = ['General provisions','Standards and records','Personhood and embodiment','Property and finance','Labor and civic service','Travel and communications','Enforcement and closure','Resources and settlements','Government and citizenship','Emergency authority'];
const sourceExtensions = new Set(['md','txt','json','html']);
function eligible(path) {
  const parts = path.split('/');
  return !parts.some(p => p.startsWith('.') || /(?:^|[-_ ])backups?$/i.test(p) || p === 'node_modules') && sourceExtensions.has(path.split('.').pop().toLowerCase());
}
function clean(text) {
  return text.replace(/<!-- ssac:(references|catalog|inbox):start -->[\s\S]*?<!-- ssac:\1:end -->/g, '')
    .replace(/&amp;/g, '&').replace(/&percnt;/g, '%').replace(/&#37;/g, '%').replace(/&#38;/g, '&');
}
function field(text, key) {
  const fm = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!fm) return '';
  const value = fm[1].match(new RegExp(`^${key}:\\s*(.*?)\\s*$`, 'm'))?.[1] || '';
  return value.replace(/^(["'])(.*)\1$/, '$2');
}
function sortCode(a,b) {
  const x=a.match(/\d+/g).map(Number), y=b.match(/\d+/g).map(Number);
  for(let i=0;i<4;i++) if(x[i]!==y[i]) return x[i]-y[i];
  return 0;
}
function scan(path, text) {
  const own=field(text,'type')==='settled-systems-code' ? field(text,'code') : '';
  const law = own && /^A[0-9]%\d+&\d+-\d+$/.test(own) ? {
    code:own, path, title:field(text,'short-title') || field(text,'formal-title') || own,
    status:field(text,'code-status') || (field(text,'status')==='active'?'established':'unreviewed')
  } : null;
  const hits=[], issues=[];
  let heading='', fence=null;
  clean(text).split(/\r?\n/).forEach((line,index)=>{
    const f=line.match(/^\s*(`{3,}|~{3,})/);
    if(f){if(!fence) fence=f[1][0]; else if(f[1][0]===fence) fence=null; return;}
    if(fence || /<!--\s*ssac:ignore/.test(line)) return;
    const h=line.match(/^#{1,6}\s+(.+?)(?:\s+#+)?$/);
    if(h) heading=h[1].replace(/[*`]/g,'');
    const re=/(?<![A-Za-z0-9_])A(\d+)\s*%\s*(\d+)\s*&\s*(\d+)\s*-\s*(\d+)(?:(\.\.(\d+))|(\.[a-z]+))?(?![A-Za-z0-9_])/g;
    for(const m of line.matchAll(re)) {
      const code=`A${Number(m[1])}%${Number(m[2])}&${Number(m[3])}-${Number(m[4])}`;
      if(Number(m[1])>9){issues.push({path,heading,line:index+1,text:`Unregistered Administrative Title in ${m[0]}.`});continue;}
      if(m[5]) issues.push({path,heading,line:index+1,text:`Range ${m[0]}: only its first clause is indexed. Confirm the other clauses before creating notes.`});
      if(code===own) continue;
      hits.push({code,path,heading,line:index+1,raw:m[0],excerpt:line.trim().slice(0,600),subclause:m[7]||''});
    }
  });
  return {law,hits,issues};
}
function collect(entries) {
  const laws=new Map(), refs=new Map(), issues=[];
  for(const {path,text} of entries) {
    if(!eligible(path)) continue;
    const result=scan(path,text); issues.push(...result.issues);
    if(result.law){
      if(laws.has(result.law.code)) issues.push({path,heading:'',text:`Duplicate law note for ${result.law.code}; kept ${laws.get(result.law.code).path}.`});
      else laws.set(result.law.code,result.law);
    }
    for(const hit of result.hits) {
      if(!refs.has(hit.code)) refs.set(hit.code,[]);
      refs.get(hit.code).push(hit);
    }
  }
  return {laws,refs,issues};
}
function safeLabel(s){return String(s).replace(/[|\r\n]/g,' ').replace(/[\[\]]/g,'');}
function link(path, heading='', label='') {
  const target=path.replace(/\.md$/,'');
  return `[[${target}${heading?'#'+heading.replace(/[\[\]|]/g,''):''}|${safeLabel(label || path.split('/').pop().replace(/\.md$/,''))}]]`;
}
function references(code,state) {
  const rows=[], seen=new Set();
  for(const h of (state.refs.get(code)||[]).slice().sort((a,b)=>a.path.localeCompare(b.path)||a.line-b.line)){
    const key=h.path+'#'+h.heading;if(seen.has(key))continue;seen.add(key);
    rows.push(`- ${link(h.path,h.heading)}${h.heading?' — '+safeLabel(h.heading):''}`);
  }
  return `## Referenced in\n\n${rows.length?rows.join('\n'):'No other current notes cite this provision.'}`;
}
function catalog(state) {
  const rows=[...state.laws.values()].sort((a,b)=>sortCode(a.code,b.code));
  let out='';
  for(let i=0;i<TITLES.length;i++) {
    const group=rows.filter(r=>r.code.startsWith(`A${i}%`));if(!group.length)continue;
    out+=`## A${i} — ${TITLES[i]}\n\n| Code | Provision | Status | Source files |\n| --- | --- | --- | ---: |\n`;
    for(const l of group) out+=`| ${link(l.path,'',l.code).replace(/\|/g, '\\|')} | ${safeLabel(l.title)} | ${safeLabel(l.status)} | ${new Set((state.refs.get(l.code)||[]).map(x=>x.path)).size} |\n`;
    out+='\n';
  }
  return out.trim() || 'No Code notes have been registered.';
}
function inbox(state) {
  const missing=[...state.refs.keys()].filter(c=>!state.laws.has(c)).sort(sortCode);
  const out=['## New citations\n'];
  if(!missing.length)out.push('Every detected citation has a note.');
  for(const code of missing){
    out.push(`### ${code}\n`);
    const seen=new Set();for(const h of state.refs.get(code)){
      if(seen.has(h.path+'#'+h.heading))continue;seen.add(h.path+'#'+h.heading);
      out.push(`- ${link(h.path,h.heading)} — ${safeLabel(h.excerpt).replace(/`/g,'')}`);
    }
    out.push('');
  }
  const review=[...state.laws.values()].filter(l=>l.status!=='established').sort((a,b)=>sortCode(a.code,b.code));
  out.push('\n## Drafts and examples\n');
  out.push(review.length ? review.map(l=>`- ${link(l.path,'',l.title)} — ${l.status}`).join('\n'):'None.');
  out.push('\n## Citation issues\n');
  out.push(state.issues.length ? state.issues.map(i=>`- ${link(i.path,i.heading)} — ${safeLabel(i.text)}`).join('\n'):'No duplicate notes or citation-range issues found.');
  return out.join('\n');
}
function patch(text, begin, end, content) {
  const start=text.indexOf(begin), stop=text.indexOf(end);
  if(start<0 && stop<0)return text.replace(/\s*$/,'')+`\n\n${begin}\n${content}\n${end}\n`;
  if(start<0||stop<start||text.indexOf(begin,start+begin.length)>=0||text.indexOf(end,stop+end.length)>=0) throw new Error('Managed section markers are incomplete or duplicated; repair them before refreshing.');
  return text.slice(0,start)+`${begin}\n${content}\n${end}`+text.slice(stop+end.length);
}
function stub(code) {
  if(!/^A[0-9]%\d+&\d+-\d+$/.test(code))throw new Error('Invalid citation');
  const [title,chapter,section,clause]=code.match(/\d+/g).map(Number);
  return `---\ntype: settled-systems-code\ncode: "${code}"\nshort-title: "${code} — needs a description"\ncode-status: unreviewed\nadministrative-title: A${title}\nchapter: ${chapter}\nsection: ${section}\nclause: ${clause}\ntags:\n  - settled-systems-code\n---\n\n# ${code}\n\nThis citation was found in another note. Its meaning has not been reviewed.\n\n## What it does\n\nAdd a plain-language account based on the source notes below. Leave unspecified powers, penalties, and exemptions unresolved.\n\n${BEGIN}\n## Referenced in\n\nPending scan.\n${END}\n`;
}
module.exports={ROOT,INDEX,INBOX,BEGIN,END,CBEGIN,CEND,IBEGIN,IEND,TITLES,eligible,clean,field,scan,collect,sortCode,link,references,catalog,inbox,patch,stub};
