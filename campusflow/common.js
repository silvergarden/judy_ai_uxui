const fs=require('fs'),path=require('path');
exports.fontCss=()=>{let css='';for(const [pkg,ws] of [['hahmlet',[400,500]],['noto-sans-kr',[400,500,700,900]]]){const d=path.join(__dirname,'node_modules/@fontsource',pkg);for(const w of ws){css+=fs.readFileSync(path.join(d,w+'.css'),'utf8').replace(/url\(\.\/files\//g,'url(file://'+d+'/files/')}}return css};
exports.SYL=`강의명: 자료구조\n교수: 김하늘\n요일: 월수\n시간: 09:00~11:00\n강의실: 공학관 201호\n학점: 3\n과제: 연결 리스트 구현 과제 / 2026-11-26\n중간고사: 2026-12-01`;
exports.REST=()=>{S.courses.push(
 {id:"c2",name:"운영체제",days:[2,4],start:10,end:12,room:"공학관 302호",credits:3,color:2},
 {id:"c3",name:"데이터사이언스",days:[1,3],start:13,end:15,room:"정보관 104호",credits:3,color:4},
 {id:"c4",name:"대학 글쓰기",days:[5],start:10,end:12,room:"인문관 205호",credits:3,color:3});
 S.tasks.push({id:"t2",title:"비평 에세이 제출",course:"대학 글쓰기",kind:"과제",due:"2026-11-25",hours:2,done:false},
 {id:"t4",title:"회귀 분석 보고서",course:"데이터사이언스",kind:"과제",due:"2026-11-29",hours:3,done:false},
 {id:"t3",title:"쪽지 시험",course:"운영체제",kind:"시험",due:"2026-11-27",hours:2,done:false});save();render()};
