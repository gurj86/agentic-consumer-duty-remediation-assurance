const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('vehicle_quality.html','utf8').replace(/\r/g,'');
const elements=new Map();
function element(id){if(!elements.has(id))elements.set(id,{value:'',hidden:true,textContent:'',classList:{add(){},remove(){}},addEventListener(){},scrollIntoView(){}});return elements.get(id)}
const decisions=['Approve','Further Investigation','Escalate'].map(decision=>({...element(decision),dataset:{decision}}));
const document={getElementById:element,querySelectorAll:s=>s==='[data-decision]'?decisions:[]};
const context=vm.createContext({document,console,setTimeout});
vm.runInContext(html.match(/<script>([\s\S]*)<\/script>/)[1],context);
const run=code=>vm.runInContext(code,context);
const completed={recommendation:'Uphold',final_response_status:'Draft FRL - upheld',final_response_draft:'Dear Alex',redress_status:'Calculated',redress_principal:'£1,300.32',redress_interest:'£468.11',redress_total:'£1,768.43',redress_methodology_summary:'Fictional'};
run(`currentResult=${JSON.stringify(completed)};updateDownload()`);
assert.equal(element('frlPdf').hidden,true);
decisions[0].onclick();assert.equal(element('frlPdf').hidden,false);
for(const b of decisions.slice(1)){b.onclick();assert.equal(element('frlPdf').hidden,true)}
for(const recommendation of ['Further Investigation','Escalate']){run(`currentResult.recommendation=${JSON.stringify(recommendation)}`);decisions[0].onclick();assert.equal(element('frlPdf').hidden,true)}
run(`currentResult=${JSON.stringify({...completed,recommendation:'Reject',final_response_status:'Draft FRL - not upheld',redress_status:'Not applicable'})}`);decisions[0].onclick();assert.equal(element('frlPdf').hidden,false);
run('resetApproval()');assert.equal(element('frlPdf').hidden,true);assert.equal(run('humanDecision'),'');
console.log('PASS: approval visibility, Uphold/Reject, incomplete outcomes, reset');


const original=fs.readFileSync('complaint_redress.html','utf8').replace(/\r/g,'');
assert.equal(html.match(/<style>([\s\S]*?)<\/style>/)[1],original.match(/<style>([\s\S]*?)<\/style>/)[1]);
const ids=s=>[...s.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);
assert.deepEqual(ids(html),ids(original));
assert.ok(!/interview|walkthrough|simulate fulfilment/i.test(html));
assert.ok(html.includes('/api/vehicle-quality/run'));
assert.ok(html.includes('/api/vehicle-quality/extract'));
assert.ok(html.includes('/api/vehicle-quality/final-response.pdf'));
console.log('PASS: identical styles and control structure; vehicle routes; no walkthrough content');

