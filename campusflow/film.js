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
 await p.goto('file://'+require('path').resolve(__dirname,'index.html'));
 await p.addStyleTag({content:C.fontCss()+`
 #fcur{position:fixed;z-index:99999;left:0;top:0;width:28px;height:28px;pointer-events:none;transform:translate(960px,620px)}
 .app{height:calc(100% - 92px)!important}.scrim{bottom:92px!important}
 #fcap{position:fixed;z-index:99998;left:0;right:0;bottom:0;height:92px;display:flex;align-items:center;gap:22px;padding:0 56px;background:#191919;color:#fff;font:700 28px/36px "Noto Sans KR",sans-serif;letter-spacing:.01em;white-space:nowrap;transition:background .3s}
 #fcap>*{transition:opacity .25s}
 #fcap i{font-style:normal;font-size:20px;font-weight:900;letter-spacing:.14em;padding:8px 16px;background:#FFCE52;color:#191919}
 #fcap small{font-weight:400;font-size:22px;opacity:.72}
 #fcap:not(.story){background:#FFCE52;color:#191919}
 #fcap:not(.story) i{background:#191919;color:#FFCE52}
 #fcap:not(.story) small{opacity:.8}
 #fcap.story{font-weight:500}

 #fring{position:fixed;inset:0;z-index:99996;pointer-events:none}
 #fring path{fill:none;stroke:url(#neon);stroke-width:6;stroke-linecap:round;transition:opacity .5s}
 .frip{position:fixed;z-index:99997;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;background:rgba(1,85,191,.28);pointer-events:none;animation:frip .5s ease-out forwards}
 @keyframes frip{from{transform:scale(.3);opacity:1}to{transform:scale(1.5);opacity:0}}`});
 await p.evaluate(()=>{
  const cur=document.createElement('div');cur.id='fcur';cur.innerHTML='<svg viewBox="0 0 28 28" width="28" height="28"><path d="M5 3l17 10-7.5 1.8L18 22l-3.2 1.5-3.4-7.3L6 21z" fill="#191919" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';document.body.appendChild(cur);
  const cap=document.createElement('div');cap.id='fcap';cap.className='story';document.body.appendChild(cap);const ring=document.createElementNS('http://www.w3.org/2000/svg','svg');ring.id='fring';ring.setAttribute('width',1920);ring.setAttribute('height',1080);document.body.appendChild(ring);
  window.__seg=(g,x1,y1,x2,y2,op)=>{let G=ring.querySelector('#'+g);if(!G){G=document.createElementNS('http://www.w3.org/2000/svg','g');G.id=g;G.style.transition='opacity .6s';ring.appendChild(G)}const l=document.createElementNS('http://www.w3.org/2000/svg','line');l.setAttribute('x1',x1);l.setAttribute('y1',y1);l.setAttribute('x2',x2);l.setAttribute('y2',y2);l.setAttribute('stroke','#FFC629');l.setAttribute('stroke-width',7);l.setAttribute('stroke-linecap',op>=1?'round':'butt');l.setAttribute('stroke-opacity',op);G.appendChild(l)};
  window.__segdone=g=>{const G=ring.querySelector('#'+g);if(!G)return;setTimeout(()=>{G.style.opacity=0},1100);setTimeout(()=>G.remove(),1800)};
  window.__ring=(d,ms)=>{const pth=document.createElementNS('http://www.w3.org/2000/svg','path');pth.setAttribute('d',d);ring.appendChild(pth);const L=pth.getTotalLength();pth.style.strokeDasharray=L;pth.style.strokeDashoffset=L;pth.animate([{strokeDashoffset:L},{strokeDashoffset:0}],{duration:ms,fill:'forwards',easing:'linear'});setTimeout(()=>{pth.style.opacity=0},ms+900);setTimeout(()=>pth.remove(),ms+1500)};
  document.addEventListener('mousemove',e=>{cur.style.transform=`translate(${e.clientX-5}px,${e.clientY-3}px)`},true);
  document.addEventListener('mousedown',e=>{const r=document.createElement('div');r.className='frip';r.style.left=e.clientX+'px';r.style.top=e.clientY+'px';document.body.appendChild(r);setTimeout(()=>r.remove(),600)},true);
  window.__cap=(tag,t,sub)=>{[...cap.children].forEach(c=>c.style.opacity=0);setTimeout(()=>{cap.className=tag?'':'story';cap.innerHTML=(tag?`<i>${tag}</i>`:'')+`<span>${t}</span>`+(sub?`<small>${sub}</small>`:'')},220)};
 });
 await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1200);
 let pos=[960,620];await p.mouse.move(...pos);
 const W=ms=>p.waitForTimeout(ms);
 const cap=(tag,t,sub)=>p.evaluate(([a,b,c])=>window.__cap(a,b,c),[tag,t,sub||'']);
 const mv=async(sel,opt={})=>{const el=p.locator(sel).first();await el.scrollIntoViewIfNeeded();const bb=await el.boundingBox();const x=bb.x+bb.width*(opt.fx??.5),y=bb.y+bb.height*(opt.fy??.5);const d=Math.hypot(x-pos[0],y-pos[1]);const n=Math.max(9,Math.round(d/42));
   for(let i=1;i<=n;i++){const t=i/n,e=t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;await p.mouse.move(pos[0]+(x-pos[0])*e,pos[1]+(y-pos[1])*e);await W(14)}pos=[x,y]};
 const circ=async(sel,o={})=>{const el=p.locator(sel).first();const bb=await el.boundingBox();const pad=o.pad??18;const cx=bb.x+bb.width/2,cy=bb.y+bb.height/2,rx=Math.min(bb.width/2+pad,o.maxrx??900),ry=Math.min(bb.height/2+(o.padY??pad),o.maxry??460);
   // 채점할 때처럼 손으로 그린 원: 왼쪽 위에서 시작해 한 바퀴를 조금 넘기고, 살짝 기울고 끝이 바깥으로 벌어진다
   const a0=-Math.PI*0.62,sweep=Math.PI*2*1.1,tilt=-0.07,ph=(cx*0.013+cy*0.007)%6.28;
   const pt=t=>{const a=a0+sweep*t,k=1+0.03*Math.sin(2*a+ph)+0.02*Math.sin(3*a+ph*1.7)+0.055*t;const x=rx*k*Math.cos(a),y=ry*k*Math.sin(a);return [cx+x*Math.cos(tilt)-y*Math.sin(tilt),cy+x*Math.sin(tilt)+y*Math.cos(tilt)]};
   const [sx,sy]=pt(0);const d0=Math.hypot(sx-pos[0],sy-pos[1]),n0=Math.max(8,Math.round(d0/42));for(let i=1;i<=n0;i++){const t=i/n0,e=t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;await p.mouse.move(pos[0]+(sx-pos[0])*e,pos[1]+(sy-pos[1])*e);await W(14)}
   const N=64,gid='g'+Date.now();let prev=[sx,sy];
   for(let i=1;i<=N;i++){const t=i/N,q=pt(t),tm=(i-.5)/N,op=Math.max(.06,tm<.18?1:1-(tm-.18)/.82*.94);
     await p.evaluate(([g,x1,y1,x2,y2,op])=>window.__seg(g,x1,y1,x2,y2,op),[gid,prev[0],prev[1],q[0],q[1],op]);
     await p.mouse.move(q[0],q[1]);prev=q;await W(15)}
   pos=prev;await p.evaluate(g=>window.__segdone(g),gid);await W(o.after??500)};
 const ck=async(sel,opt)=>{await mv(sel,opt);await W(110);await p.mouse.down();await W(60);await p.mouse.up();await W(opt?.after??500)};
 // screencast
 const cdp=await c.newCDPSession(p);const frames=[];let n=0;
 cdp.on('Page.screencastFrame',async f=>{const name=`frames/${String(n++).padStart(5,'0')}.jpg`;fs.writeFileSync(name,Buffer.from(f.data,'base64'));frames.push([name,f.metadata.timestamp]);cdp.send('Page.screencastFrameAck',{sessionId:f.sessionId}).catch(()=>{})});
 await cdp.send('Page.startScreencast',{format:'jpeg',quality:92,maxWidth:1920,maxHeight:1080,everyNthFrame:1});
 const t0=Date.now();const mark=l=>console.log(l,((Date.now()-t0)/1000).toFixed(1));
 // S0 empty
 await cap('','“처음 열면 아직 아무것도 없어요.”');await W(700);await circ('.grid-empty p',{pad:36,padY:88,after:500});mark('s0');
 await cap('','“메뉴를 먼저 둘러봐요.”');
 for(const v of ['tasks','assistant','planner','focus','prefs'])await ck(`#nav [data-v=${v}]`,{after:260});
 await ck('#nav [data-v=timetable]',{after:700});mark('tour');
 // Task: 일정 넣기
 await cap('TASK 1','공지·강의계획서로 일정 넣기','“붙여 넣기만 해요.”');
 await ck('.grid-empty [data-v=assistant]',{after:900});
 await ck('#draft',{after:300});await p.fill('#draft',C.SYL);await W(1300);
 await ck('#send',{after:1500});
 await mv('[data-act=confirm-apply]');await W(900);
 await p.mouse.down();await W(60);await p.mouse.up();await W(1100);
 await ck('#nav [data-v=timetable]',{after:800});await circ('.blk',{pad:16,after:300});await circ('.rightcol section',{pad:6,after:500});mark('t2');
 // jump
 await cap('','“같은 방법으로 나머지 강의도 넣었어요.”');await W(500);await p.evaluate(C.REST);await W(1100);mark('jump');
 // Task: 공부 계획
 await cap('TASK 2','우선순위로 공부 계획 만들기','“중요도만 골라요.”');
 await ck('#nav [data-v=planner]',{after:900});
 for(const [nm,v] of [['자료구조',5],['운영체제',4],['데이터사이언스',3],['대학 글쓰기',3]])await ck(`[data-act=imp][data-c="${nm}"][data-n="${v}"]`,{after:200});
 await W(400);await ck('[data-act=plan-make]',{after:1300});
 await ck('[data-act=plan-view]',{after:900});await circ('.wk',{pad:-30,maxry:330,after:300});mark('t3');
 // Task: 확인
 await cap('TASK 3','이번 주 일정 확인하기','“열자마자 보여요.”');
 await circ('.col.today',{pad:8,maxry:380,after:300});await circ('.rightcol section',{pad:6,after:400});
 await ck('.rightcol [data-v=tasks]',{after:800});
 await ck('#view .task .cb',{after:800});
 await ck('#nav [data-v=timetable]',{after:700});
 await cap('TASK 4','바뀐 일정에 다시 맞추기','“말하면 다시 맞춰요.”');
 await ck('#nav [data-v=assistant]',{after:600});
 await ck('#draft',{after:200});await p.fill('#draft','수요일은 안 돼. 공부 계획 다시 짜 줘');await W(500);
 await ck('#send',{after:1200});
 await mv('[data-act=confirm-apply]');await W(500);await p.mouse.down();await W(60);await p.mouse.up();await W(800);
 await ck('#nav [data-v=timetable]',{after:500});await circ('.wk',{pad:-30,maxry:330,after:300});mark('t4');
 await cap('','“이제 이번 주가 한눈에 보여요.”');await mv('#title',{fx:1.5});await W(1300);mark('end');
 await cdp.send('Page.stopScreencast');await W(300);
 const end=Date.now()/1000;let out='';
 for(let i=0;i<frames.length;i++){const d=(i+1<frames.length?frames[i+1][1]:frames[i][1]+0.5)-frames[i][1];out+=`file '${frames[i][0]}'\nduration ${Math.max(d,0.001).toFixed(4)}\n`}
 out+=`file '${frames[frames.length-1][0]}'\n`;fs.writeFileSync('list.txt',out);
 console.log('frames',frames.length,'span',(frames[frames.length-1][1]-frames[0][1]).toFixed(1));
 await b.close();
})();
