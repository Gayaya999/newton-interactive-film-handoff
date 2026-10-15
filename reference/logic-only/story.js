(function(root){
  'use strict';
  const nodes={
    welcome:{kind:'welcome',chapter:0,title:'苹果之外'},
    opening:{kind:'video',chapter:0,title:'一个落下的苹果',clips:['opening'],next:'speed'},
    speed:{kind:'choice',chapter:0,title:'让它绕过地面',poster:'speed'},
    low:{kind:'video',chapter:0,title:'这一次，落到了地面',clips:['low'],next:'speed'},
    high:{kind:'video',chapter:0,title:'这一次，飞向了远处',clips:['high'],next:'speed'},
    orbit:{kind:'video',chapter:0,title:'下落，也可以是绕行',clips:['orbit','moon-question'],next:'hypothesis'},
    hypothesis:{kind:'choice',chapter:1,title:'距离，会改变什么？',poster:'hypothesis'},
    accept:{kind:'video',chapter:1,title:'留下一个可以检验的想法',clips:['accept'],next:'research'},
    research:{kind:'video',chapter:1,title:'让记录来回答',clips:['research'],next:'notebook'},
    notebook:{kind:'game',chapter:1,title:'把预测放到证据面前'},
    evidence:{kind:'video',chapter:1,title:'从核对中看见规律',clips:['distance','confirmation'],next:'relation-question'},
    'relation-question':{kind:'video',chapter:2,title:'另一边，也会回应吗？',clips:['relation-question'],next:'reciprocity'},
    reciprocity:{kind:'choice',chapter:2,title:'苹果落下，地球呢？',poster:'reciprocity'},
    'oneway-feedback':{kind:'video',chapter:2,title:'补上遗漏的另一半',clips:['oneway-feedback'],next:'reciprocal-explanation'},
    'mutual-feedback':{kind:'video',chapter:2,title:'相互吸引，不同的变化',clips:['mutual-feedback'],next:'reciprocal-explanation'},
    'reciprocal-explanation':{kind:'video',chapter:2,title:'连接大地与星空',clips:['reciprocal-explanation'],next:'ending'},
    ending:{kind:'video',chapter:2,title:'一个问题，打开更大的世界',clips:['ending'],next:'summary'},
    summary:{kind:'summary',chapter:3,title:'你的发现，已经留在手稿里'}
  };
  function createState(){return {version:1,node:'welcome',attempts:0,tried:[],orbitVerified:false,hypothesis:null,originalHypothesis:null,notebookVerified:false,reciprocity:null};}
  function transition(state,event){
    const s={...state,tried:[...state.tried]};
    if(event.type==='restart')return {...createState(),node:'opening'};
    if(event.type==='start'&&s.node==='welcome')s.node='opening';
    else if(event.type==='ended'&&nodes[s.node]?.kind==='video')s.node=nodes[s.node].next;
    else if(event.type==='choose'){
      if(s.node==='speed'&&[1,2,3].includes(event.value)){
        s.attempts++;if(!s.tried.includes(event.value))s.tried.push(event.value);
        s.node=({1:'low',2:'orbit',3:'high'})[event.value];if(event.value===2)s.orbitVerified=true;
      }else if(s.node==='hypothesis'&&['constant','weakens'].includes(event.value)){
        s.hypothesis=event.value;s.originalHypothesis=event.value;s.node='accept';
      }else if(s.node==='reciprocity'&&['one-way','mutual'].includes(event.value)){
        s.reciprocity=event.value;s.node=event.value==='mutual'?'mutual-feedback':'oneway-feedback';
      }
    }else if(event.type==='revise'&&s.node==='notebook')s.hypothesis='weakens';
    else if(event.type==='notebook-complete'&&s.node==='notebook'&&s.hypothesis==='weakens'){
      s.notebookVerified=true;s.node='evidence';
    }
    return s;
  }
  function restoreState(raw){
    if(!raw||raw.version!==1||!nodes[raw.node]||!Number.isInteger(raw.attempts)||raw.attempts<0||raw.attempts>10000||!Array.isArray(raw.tried)||raw.tried.some(x=>![1,2,3].includes(x)))return createState();
    if(typeof raw.orbitVerified!=='boolean'||typeof raw.notebookVerified!=='boolean')return createState();
    const afterLaunch=['hypothesis','accept','research','notebook','evidence','relation-question','reciprocity','oneway-feedback','mutual-feedback','reciprocal-explanation','ending','summary'];
    const afterEvidence=['evidence','relation-question','reciprocity','oneway-feedback','mutual-feedback','reciprocal-explanation','ending','summary'];
    if(afterLaunch.includes(raw.node)&&!raw.orbitVerified)return createState();
    if(afterLaunch.includes(raw.node)&&raw.node!=='hypothesis'&&!['constant','weakens'].includes(raw.hypothesis))return createState();
    if(afterEvidence.includes(raw.node)&&(!raw.notebookVerified||raw.hypothesis!=='weakens'))return createState();
    if(['oneway-feedback','mutual-feedback','reciprocal-explanation','ending','summary'].includes(raw.node)&&!['one-way','mutual'].includes(raw.reciprocity))return createState();
    return {...createState(),node:raw.node,attempts:raw.attempts,tried:[...new Set(raw.tried)],orbitVerified:raw.orbitVerified,hypothesis:raw.hypothesis,originalHypothesis:raw.originalHypothesis,notebookVerified:raw.notebookVerified,reciprocity:raw.reciprocity};
  }
  const api={nodes,createState,transition,restoreState};
  if(typeof module!=='undefined')module.exports=api;else root.NewtonStory=api;
})(typeof window!=='undefined'?window:globalThis);
