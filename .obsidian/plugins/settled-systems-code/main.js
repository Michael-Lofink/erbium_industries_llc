'use strict';
const {Plugin, Notice, FuzzySuggestModal, PluginSettingTab, Setting}=require('obsidian');
// Local helpers are bundled: Obsidian loads one plugin entry file.
const C=(()=>{
const module={exports:{}};
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

return module.exports;
})();
class CitationPicker extends FuzzySuggestModal {
  constructor(app,items,choose){super(app);this.items=items;this.choose=choose;this.setPlaceholder('Choose a citation to make an unreviewed note');}
  getItems(){return this.items;}
  getItemText(item){return item;}
  onChooseItem(item){this.choose(item);}
}
module.exports=class SettledCodePlugin extends Plugin {
  async onload(){
    this.settings=Object.assign({notify:true,autoCreate:false},await this.loadData());
    this.state=null;this.running=false;this.dirty=false;this.stopped=false;this.writing=new Set();this.seen=new Set();
    this.addCommand({id:'open-code-index',name:'Open Code index',callback:()=>this.open(C.INDEX)});
    this.addCommand({id:'open-code-inbox',name:'Open new citations and review queue',callback:()=>this.open(C.INBOX)});
    this.addCommand({id:'rescan-code',name:'Refresh Code references',callback:async()=>{await this.refresh();new Notice('Code references refreshed.');}});
    this.addCommand({id:'create-code-note',name:'Create note for a new citation',callback:async()=>{
      await this.refresh();
      const items=[...this.state.refs.keys()].filter(c=>!this.state.laws.has(c)).sort(C.sortCode);
      if(!items.length){new Notice('Every detected citation already has a note.');return;}
      new CitationPicker(this.app,items,async code=>{try{const path=await this.createNote(code);await this.refresh();await this.open(path);}catch(e){this.error(e);}}).open();
    }});
    this.addSettingTab(new CodeSettings(this.app,this));
    this.app.workspace.onLayoutReady(()=>{
      if(this.stopped)return;
      const changed=(file,oldPath)=>{
        if(this.writing.has(file.path)||[C.INDEX,C.INBOX].includes(file.path))return;
        if(C.eligible(file.path)||(oldPath&&C.eligible(oldPath))||!file.extension)this.schedule();
      };
      for(const event of ['create','modify','delete','rename'])this.registerEvent(this.app.vault.on(event,changed));
      this.refresh().catch(e=>this.error(e));
    });
  }
  onunload(){this.stopped=true;clearTimeout(this.timer);}
  error(e){console.error('Settled Systems Code:',e);new Notice(`Code scan could not finish: ${e.message}`,10000);}
  schedule(){
    if(this.stopped)return;
    clearTimeout(this.timer);this.timer=setTimeout(()=>this.refresh().catch(e=>this.error(e)),1000);
  }
  async open(path){await this.app.workspace.openLinkText(path,'',false);}
  async folder(path){
    let built='';for(const bit of path.split('/')){built+=(built?'/':'')+bit;if(!this.app.vault.getAbstractFileByPath(built))await this.app.vault.createFolder(built);}
  }
  async createNote(code){
    // Recheck the vault immediately: a note may have been added since the last scan.
    for(const f of this.app.vault.getMarkdownFiles()){
      if(C.eligible(f.path)&&C.scan(f.path,await this.app.vault.cachedRead(f)).law?.code===code)return f.path;
    }
    const path=`${C.ROOT}/Provisions/${code}.md`;
    if(this.app.vault.getAbstractFileByPath(path))throw Error(`A different file already occupies ${path}. It was not replaced.`);
    await this.folder(`${C.ROOT}/Provisions`);
    await this.app.vault.create(path,C.stub(code));
    return path;
  }
  async managed(path,begin,end,content,initial){
    if(this.stopped)return;
    let f=this.app.vault.getAbstractFileByPath(path);
    if(!f){await this.folder(path.slice(0,path.lastIndexOf('/')));f=await this.app.vault.create(path,initial);}
    if(!f.extension)throw Error(`Expected a note at ${path}`);
    const current=await this.app.vault.read(f);
    const next=C.patch(current,begin,end,content);if(next===current)return;
    this.writing.add(path);
    try{await this.app.vault.process(f,latest=>C.patch(latest,begin,end,content));}
    finally{this.writing.delete(path);}
  }
  async refresh(){
    this.dirty=true;
    if(this.running)return this.pending;
    this.running=true;
    this.pending=(async()=>{
      try{
        do{
          this.dirty=false;
          if(this.stopped)return;
          const files=this.app.vault.getFiles().filter(f=>C.eligible(f.path));
          const entries=[];
          // Limit concurrent reads on mobile and large vaults.
          for(let i=0;i<files.length;i+=8){
            const batch=await Promise.all(files.slice(i,i+8).map(async f=>({path:f.path,text:await this.app.vault.cachedRead(f)})));
            entries.push(...batch);
          }
          this.state=C.collect(entries);
          const missing=[...this.state.refs.keys()].filter(c=>!this.state.laws.has(c));
          const fresh=missing.filter(c=>!this.seen.has(c));
          if(this.settings.autoCreate){
            for(const code of missing){await this.createNote(code);}
            if(missing.length){this.dirty=true;continue;}
          }
          for(const l of this.state.laws.values()){
            await this.managed(l.path,C.BEGIN,C.END,C.references(l.code,this.state),'');
          }
          await this.managed(C.INDEX,C.CBEGIN,C.CEND,C.catalog(this.state),'# Code Index\n\nEach provision has a short explanation and a list of notes that cite it.\n');
          await this.managed(C.INBOX,C.IBEGIN,C.IEND,C.inbox(this.state),'# Code Inbox\n\nNew citations need a description and a status. Use **Settled Systems Code: Create note for a new citation** from the command palette.\n');
          missing.forEach(c=>this.seen.add(c));
          if(fresh.length&&this.settings.notify)new Notice(`${fresh.length} new Code citation${fresh.length===1?'':'s'} found. Open Code Inbox to review.`,8000);
        }while(this.dirty&&!this.stopped);
      }finally{this.running=false;}
    })();
    return this.pending;
  }
};
class CodeSettings extends PluginSettingTab {
  constructor(app,plugin){super(app,plugin);this.plugin=plugin;}
  display(){
    const {containerEl}=this;containerEl.empty();
    containerEl.createEl('h2',{text:'Settled Systems Code'});
    new Setting(containerEl).setName('Notify about new citations').setDesc('Show a notice when a saved note contains a citation without a law note.').addToggle(t=>t.setValue(this.plugin.settings.notify).onChange(async v=>{this.plugin.settings.notify=v;await this.plugin.saveData(this.plugin.settings);}));
    new Setting(containerEl).setName('Create unreviewed notes automatically').setDesc('Off by default. New notes contain the citation and source links only; they do not invent a law or mark it as established.').addToggle(t=>t.setValue(this.plugin.settings.autoCreate).onChange(async v=>{this.plugin.settings.autoCreate=v;await this.plugin.saveData(this.plugin.settings);this.plugin.schedule();}));
    containerEl.createEl('p',{text:'Scans saved Markdown, text, JSON, and HTML files. PDF exports are listed from the initial audit but are not rescanned automatically. Only marked reference, index, and inbox sections are maintained; your law text stays editable.'});
  }
}
