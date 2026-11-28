const {chromium}=require('playwright');const C=require('./common');const fs=require('fs');
(async()=>{
 fs.rmSync('frames',{recursive:true,force:true});fs.mkdirSync('frames');
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--force-device-scale-factor=1']});
 const c=await b.newContext({viewport:{width:1920,height:1080},timezoneId:'Asia/Seoul',locale:'ko-KR'});
 const p=await c.newPage();await p.clock.install({time:new Date('2026-11-23T10:00:00+09:00')});
 p.on('pageerror',e=>console.log('ERR',e.message));
 await p.addInitScript(()=>{const wait=ms=>new Promise(r=>setTimeout(r,ms));
  const f=async()=>{await wait(700);return {text:"중요도가 높고 마감이 가까운 자료구조부터 넣었어요. 나머지 과목은 남은 평일 빈 시간에 이어서 넣었어요."}};
  f.json=async(q)=>{await wait(900);if(q&&q.includes('수요일은 안 돼'))return {reply:"수요일을 비우고 공부 계획을 다시 맞출게요. 확인해 주세요.",source:"다시 맞추기",items:[{type:"다시 맞추기",avoid:[{day:3,from:9,to:19}]}]};return {reply:"강의계획서에서 강의 1개와 마감 2건을 찾았어요. 확인하고 반영해 주세요.",source:"강의계획서 · 자료구조",items:[
   {type:"강의",name:"자료구조",days:[1,3],start:9,end:11,room:"공학관 201호",credits:3},
   {type:"과제",title:"연결 리스트 구현 과제",course:"자료구조",date:"2026-11-26",hours:3},
   {type:"시험",title:"중간고사",course:"자료구조",date:"2026-12-01",hours:5}]}};
  f.limits=async()=>({images:true});window.claude={use:async()=>f}});

 await p.goto('file://'+require('path').resolve(__dirname,'stage.html'));
 await p.addStyleTag({content:C.fontCss()});
 const fr=p.frame({name:'app'});await fr.waitForSelector('#nav');
 const IW=1360,IH=910;
 await fr.addStyleTag({content:C.fontCss()+`
 #fcur{position:fixed;z-index:99999;left:0;top:0;width:40px;height:40px;pointer-events:none;transform:translate(680px,520px)}
 #fring{position:fixed;inset:0;z-index:99996;pointer-events:none}
 .frip{position:fixed;z-index:99997;width:60px;height:60px;margin:-30px 0 0 -30px;border-radius:50%;background:rgba(255,198,41,.5);pointer-events:none;animation:frip .5s ease-out forwards}
 @keyframes frip{from{transform:scale(.3);opacity:1}to{transform:scale(1.5);opacity:0}}`});
 await fr.evaluate(([IW,IH])=>{
  const cur=document.createElement('div');cur.id='fcur';cur.innerHTML='<svg viewBox="0 0 28 28" width="40" height="40"><path d="M5 3l17 10-7.5 1.8L18 22l-3.2 1.5-3.4-7.3L6 21z" fill="#191919" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';document.body.appendChild(cur);
  const ring=document.createElementNS('http://www.w3.org/2000/svg','svg');ring.id='fring';ring.setAttribute('width',IW);ring.setAttribute('height',IH);document.body.appendChild(ring);
  window.__seg=(g,x1,y1,x2,y2,op)=>{let G=ring.querySelector('#'+g);if(!G){G=document.createElementNS('http://www.w3.org/2000/svg','g');G.id=g;G.style.transition='opacity .6s';ring.appendChild(G)}const l=document.createElementNS('http://www.w3.org/2000/svg','line');l.setAttribute('x1',x1);l.setAttribute('y1',y1);l.setAttribute('x2',x2);l.setAttribute('y2',y2);l.setAttribute('stroke','#FFC629');l.setAttribute('stroke-width',10);l.setAttribute('stroke-linecap',op>=1?'round':'butt');l.setAttribute('stroke-opacity',op);G.appendChild(l)};
  window.__segdone=g=>{const G=ring.querySelector('#'+g);if(!G)return;setTimeout(()=>{G.style.opacity=0},1100);setTimeout(()=>G.remove(),1800)};
  document.addEventListener('mousemove',e=>{cur.style.transform=`translate(${e.clientX-7}px,${e.clientY-4}px)`},true);
  document.addEventListener('mousedown',e=>{const r=document.createElement('div');r.className='frip';r.style.left=e.clientX+'px';r.style.top=e.clientY+'px';document.body.appendChild(r);setTimeout(()=>r.remove(),600)},true);
 },[IW,IH]);
 await p.evaluate(()=>document.fonts.ready);await fr.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1200);
 const fb=await p.locator('#appf').boundingBox();const S=fb.width/IW,OX=fb.x,OY=fb.y;console.log('frame',JSON.stringify(fb),S.toFixed(4),await fr.locator('#title').innerText().catch(()=>''));
 const inn=(x,y)=>[(x-OX)/S,(y-OY)/S];
 let pos=[OX+fb.width/2,OY+fb.height*.6];await p.mouse.move(...pos);
 const W=ms=>p.waitForTimeout(ms);
 const step=(chip,head,sub,cur,done)=>p.evaluate(a=>window.__step(...a),[chip,head,sub||'',cur,done]);
 const strip=(tag,t,q)=>p.evaluate(a=>window.__strip(...a),[tag,t,q||'']);
 const glide=async(x,y)=>{const d=Math.hypot(x-pos[0],y-pos[1]);const n=Math.max(8,Math.round(d/34));for(let i=1;i<=n;i++){const t=i/n,e=t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;await p.mouse.move(pos[0]+(x-pos[0])*e,pos[1]+(y-pos[1])*e);await W(14)}pos=[x,y]};
 const mv=async(sel,opt={})=>{const el=fr.locator(sel).first();await el.scrollIntoViewIfNeeded();const bb=await el.boundingBox();await glide(bb.x+bb.width*(opt.fx??.5),bb.y+bb.height*(opt.fy??.5))};
 const circ=async(sel,o={})=>{const el=fr.locator(sel).first();const bb=await el.boundingBox();const pad=(o.pad??18)*S,padY=(o.padY??o.pad??18)*S;const cx=bb.x+bb.width/2,cy=bb.y+bb.height/2,rx=Math.min(bb.width/2+pad,(o.maxrx??900)*S),ry=Math.min(bb.height/2+padY,(o.maxry??420)*S);
   const a0=-Math.PI*0.62,sweep=Math.PI*2*1.1,tilt=-0.07,ph=(cx*0.013+cy*0.007)%6.28;
   const pt=t=>{const a=a0+sweep*t,k=1+0.03*Math.sin(2*a+ph)+0.02*Math.sin(3*a+ph*1.7)+0.055*t;const x=rx*k*Math.cos(a),y=ry*k*Math.sin(a);return [cx+x*Math.cos(tilt)-y*Math.sin(tilt),cy+x*Math.sin(tilt)+y*Math.cos(tilt)]};
   const [sx,sy]=pt(0);await glide(sx,sy);
   const N=56,gid='g'+Date.now();let prev=[sx,sy];
   for(let i=1;i<=N;i++){const t=i/N,q=pt(t),tm=(i-.5)/N,op=Math.max(.06,tm<.18?1:1-(tm-.18)/.82*.94);
     await fr.evaluate(([g,a,b,op])=>window.__seg(g,a[0],a[1],b[0],b[1],op),[gid,inn(...prev),inn(...q),op]);
     await p.mouse.move(q[0],q[1]);prev=q;await W(14)}
   pos=prev;await fr.evaluate(g=>window.__segdone(g),gid);await W(o.after??500)};
 const press=async()=>{await p.mouse.down();await W(60);await p.mouse.up()};
 const ck=async(sel,opt)=>{await mv(sel,opt);await W(110);await press();await W(opt?.after??500)};
 // screencast
 const cdp=await c.newCDPSession(p);const frames=[];let n=0;
 cdp.on('Page.screencastFrame',async f=>{const name=`frames/${String(n++).padStart(5,'0')}.jpg`;fs.writeFileSync(name,Buffer.from(f.data,'base64'));frames.push([name,f.metadata.timestamp]);cdp.send('Page.screencastFrameAck',{sessionId:f.sessionId}).catch(()=>{})});
 await step('시작','처음 열면<br>비어 있어요','강의도 마감도 아직 없어요',0,0);await strip('','“처음 열면 아직 아무것도 없어요.”');await W(500);
 await cdp.send('Page.startScreencast',{format:'jpeg',quality:92,maxWidth:1920,maxHeight:1080,everyNthFrame:1});
 const t0=Date.now();const mark=l=>console.log(l,((Date.now()-t0)/1000).toFixed(1));
 // 시작
 await W(900);await circ('.grid-empty p',{pad:30,padY:70,after:500});mark('s0');
 await step('시작','메뉴를 먼저<br>둘러봐요','메뉴 6개',0,0);await strip('','“메뉴를 먼저 둘러봐요.”');
 for(const v of ['tasks','assistant','planner','focus','prefs'])await ck(`#nav [data-v=${v}]`,{after:230});
 await ck('#nav [data-v=timetable]',{after:500});mark('tour');
 // TASK 1
 await strip('TASK 1','공지·강의계획서로 일정 넣기','“붙여 넣기만 해요.”');
 await step('TASK 1','AI 도우미를<br>열어요','빈 시간표의 버튼 하나',1,0);
 await ck('.grid-empty [data-v=assistant]',{after:800});
 await step('TASK 1','강의계획서를<br>붙여 넣어요','자료구조 강의계획서',1,0);
 await ck('#draft',{after:250});await fr.fill('#draft',C.SYL);await W(800);
 await ck('#send',{after:500});
 await step('TASK 1','AI가 일정을<br>정리해요','강의 1개 · 마감 2건',1,0);await W(1300);
 await mv('[data-act=confirm-apply]');await W(700);
 await step('TASK 1','확인하고<br>반영해요','고른 것만 들어가요',1,0);await W(500);
 await press();await W(1200);
 await ck('#nav [data-v=timetable]',{after:300});
 await step('TASK 1','시간표에<br>들어갔어요','강의와 다가오는 마감',1,0);await W(500);
 await circ('.rightcol section',{pad:6,after:600});mark('t1');
 // 이어서
 await strip('','“같은 방법으로 나머지 강의도 넣었어요.”');await step('이어서','나머지 강의도<br>넣었어요','같은 방법으로 3과목 더',0,1);
 await W(450);await fr.evaluate(C.REST);await W(1500);mark('jump');
 // TASK 2
 await strip('TASK 2','우선순위로 공부 계획 만들기','“중요도만 골라요.”');
 await step('TASK 2','중요도를<br>골라요','과목마다 1~5',2,1);
 await ck('#nav [data-v=planner]',{after:700});
 for(const [nm,v] of [['자료구조',5],['운영체제',4],['데이터사이언스',3],['대학 글쓰기',3]])await ck(`[data-act=imp][data-c="${nm}"][data-n="${v}"]`,{after:200});
 await W(300);await step('TASK 2','계획서를<br>만들어요','빈 시간에 자동으로 배치',2,1);
 await ck('[data-act=plan-make]',{after:1100});
 await ck('[data-act=plan-view]',{after:300});
 await step('TASK 2','점선 블록으로<br>들어갔어요','시간표에서 바로 확인',2,1);await W(500);
 await circ('.wk',{pad:-30,maxry:300,after:500});mark('t2');
 // TASK 3
 await strip('TASK 3','이번 주 일정 확인하기','“열자마자 보여요.”');
 await step('TASK 3','오늘 수업과<br>마감이 보여요','첫 화면에서 5초 안에',3,2);
 await circ('.col.today',{pad:8,maxry:300,after:500});
 await ck('.rightcol [data-v=tasks]',{after:300});
 await step('TASK 3','끝낸 과제를<br>체크해요','완료로 바뀌어요',3,2);await W(500);
 await ck('#view .task .cb',{after:1200});mark('t3');
 // TASK 4
 await strip('TASK 4','바뀐 일정에 다시 맞추기','“말하면 다시 맞춰요.”');
 await step('TASK 4','바뀐 사정을<br>말해요','“수요일은 안 돼”',4,3);
 await ck('#nav [data-v=assistant]',{after:500});
 await ck('#draft',{after:200});await fr.fill('#draft','수요일은 안 돼. 공부 계획 다시 짜 줘');await W(600);
 await ck('#send',{after:1000});
 await step('TASK 4','새 계획을<br>반영해요','수요일을 비우고 다시 배치',4,3);
 await mv('[data-act=confirm-apply]');await W(900);await press();await W(1000);
 await ck('#nav [data-v=timetable]',{after:300});
 await step('TASK 4','수요일이<br>비었어요','공부 계획이 다시 맞춰졌어요',4,3);await W(500);
 await circ('.wk',{pad:-30,maxry:300,after:700});mark('t4');
 // 끝
 await strip('','“조금 더 여유로운 대학 생활”');await step('v3.0','CampusFlow','수업, 마감, 공부 시간을 한눈에',0,4);
 await glide(OX+fb.width*.93,OY+fb.height*.2);await W(2200);mark('end');
 await cdp.send('Page.stopScreencast');await W(300);
 let out='';
 for(let i=0;i<frames.length;i++){const d=(i+1<frames.length?frames[i+1][1]:frames[i][1]+0.5)-frames[i][1];out+=`file '${frames[i][0]}'\nduration ${Math.max(d,0.001).toFixed(4)}\n`}
 out+=`file '${frames[frames.length-1][0]}'\n`;fs.writeFileSync('list.txt',out);
 console.log('frames',frames.length,'span',(frames[frames.length-1][1]-frames[0][1]).toFixed(1));
 await b.close();
})();
