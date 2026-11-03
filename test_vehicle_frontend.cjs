const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const elements=new Map();
function element(id){if(!elements.has(id))elements.set(id,{value:'',disabled:false,hidden:true,textContent:'',readOnly:false,children:[],classList:{remove(){},toggle(){}},addEventListener(type,fn){this[type]=fn},scrollIntoView(){},replaceChildren(){this.children=[]},append(...items){this.children.push(...items)}});return elements.get(id)}
element('mode').value='walkthrough';element('scenario').value='complete';
const document={getElementById:element,querySelectorAll:()=>[],createElement:()=>element('new-'+Math.random()),createTextNode:t=>t};
const context=vm.createContext({document,console,Date,setTimeout,fetch:()=>new Promise(()=>{})});
const script=fs.readFileSync('vehicle_quality.html','utf8').match(/<script>([\s\S]*?)<\/script>/)[1];vm.runInContext(script,context);
const run=code=>vm.runInContext(code,context);
const complete={mode:'walkthrough',recommendation:'Uphold',summary:'Example',execution_note:'Scripted',tools_executed:[],chronology:[],steps:[],missing_evidence:[],proposed_remedy:'Example',redress_ready:true,redress_explanation:'£655',final_response_draft:'Draft'};
run(`render(${JSON.stringify(complete)})`);
assert.equal(element('fulfil').disabled,true);
element('approve').onclick();assert.equal(run('decision'),null);
element('reviewNote').value='Reviewed the evidence and illustrative proposal';element('approve').onclick();assert.equal(element('fulfil').disabled,false);
element('fulfil').onclick();assert.equal(run('fulfilled'),true);
element('reviewNote').oninput();assert.equal(run('decision'),null);assert.equal(element('fulfil').disabled,true);assert.equal(run('fulfilled'),false);
run(`render(${JSON.stringify({...complete,recommendation:'Further Investigation',redress_ready:false,final_response_draft:''})})`);
assert.equal(element('approve').disabled,true);element('approve').onclick();assert.equal(run('decision'),null);
run(`render(${JSON.stringify(complete)})`);element('reviewNote').value='Approved';element('approve').onclick();run('reset()');assert.equal(run('decision'),null);assert.equal(element('results').hidden,true);assert.equal(element('fulfil').disabled,true);
console.log('PASS: approval rationale, fulfilment gate, rationale edits, incomplete case block, case reset');

