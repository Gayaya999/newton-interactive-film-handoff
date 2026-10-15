const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const file=path.join(__dirname,'../story.js');
let api={};
if(fs.existsSync(file)){const box={module:{exports:{}}};vm.runInNewContext(fs.readFileSync(file,'utf8'),box);api=box.module.exports;}
test('a new story waits for a user start before playing media',()=>{
  assert.equal(typeof api.createState,'function');
  assert.equal(api.createState().node,'welcome');
  assert.equal(api.transition(api.createState(),{type:'start'}).node,'opening');
});
test('both failed launches return to controls and never unlock the hypothesis',()=>{
  let s=api.transition(api.transition(api.createState(),{type:'start'}),{type:'ended'});
  assert.equal(s.node,'speed');
  s=api.transition(s,{type:'choose',value:1});assert.equal(s.node,'low');
  s=api.transition(s,{type:'ended'});assert.equal(s.node,'speed');
  s=api.transition(s,{type:'choose',value:3});assert.equal(s.node,'high');
  s=api.transition(s,{type:'ended'});assert.equal(s.node,'speed');
  assert.equal(s.orbitVerified,false);assert.equal(s.attempts,2);
});
test('both hypotheses enter notebook; only revised supported prediction may finish it',()=>{
  let s=api.createState();
  for(const e of [{type:'start'},{type:'ended'},{type:'choose',value:2},{type:'ended'},{type:'choose',value:'constant'},{type:'ended'},{type:'ended'}])s=api.transition(s,e);
  assert.equal(s.node,'notebook');assert.equal(s.hypothesis,'constant');
  assert.equal(api.transition(s,{type:'notebook-complete'}).node,'notebook');
  s=api.transition(s,{type:'revise'});assert.equal(s.hypothesis,'weakens');
  s=api.transition(s,{type:'notebook-complete'});assert.equal(s.node,'evidence');
  assert.equal(s.notebookVerified,true);
});
test('both final answers are acknowledged then rejoin the same explanation',()=>{
  for(const value of ['one-way','mutual']){
    let s={...api.createState(),node:'reciprocity',orbitVerified:true,notebookVerified:true,hypothesis:'weakens'};
    s=api.transition(s,{type:'choose',value});assert.equal(s.node,value==='mutual'?'mutual-feedback':'oneway-feedback');
    s=api.transition(s,{type:'ended'});assert.equal(s.node,'reciprocal-explanation');
    s=api.transition(s,{type:'ended'});assert.equal(s.node,'ending');
    s=api.transition(s,{type:'ended'});assert.equal(s.node,'summary');
  }
});
test('invalid events cannot skip choices and replay clears prior progress',()=>{
  let s={...api.createState(),node:'speed'};
  assert.equal(api.transition(s,{type:'ended'}).node,'speed');
  assert.equal(api.transition(s,{type:'choose',value:99}).node,'speed');
  s=api.transition({...s,attempts:8},{type:'restart'});
  assert.equal(s.node,'opening');assert.equal(s.attempts,0);assert.equal(s.hypothesis,null);
});
test('restoring malformed or inconsistent saves starts safely',()=>{
  assert.equal(api.restoreState({node:'summary'}).node,'welcome');
  assert.equal(api.restoreState({node:'notebook',hypothesis:'bad'}).node,'welcome');
  assert.equal(api.restoreState(null).node,'welcome');
  let s=api.createState();for(const e of [{type:'start'},{type:'ended'},{type:'choose',value:2},{type:'ended'}])s=api.transition(s,e);
  assert.equal(api.restoreState(JSON.parse(JSON.stringify(s))).node,'hypothesis');
});
