#!/usr/bin/env python3
"""우리 집 3D 룸 투어 점검 스크립트.
게시 전에 이 폴더에서 실행한다: python3 check.py
필요한 것: playwright(pip install playwright)와 크롬. 크롬 위치는 환경 변수 CHROME으로 바꿀 수 있다.
페이지에 나오면 안 되는 낱말(단지 이름 등)은 저장소에 적지 않고 환경 변수로 넘긴다.
  예) ROOM_TOUR_FORBIDDEN="낱말1,낱말2" python3 check.py
실패가 하나라도 있으면 종료 코드 1."""
import os, re, sys, glob, socket, threading, functools, http.server
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")
FORBID = [w.strip() for w in os.environ.get("ROOM_TOUR_FORBIDDEN", "").split(",") if w.strip()]
ARGS = ["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--no-sandbox",
        "--disable-background-networking", "--disable-sync"]
VIEWPORTS = (("desktop", 1440, 900, False), ("laptop", 1200, 760, False), ("mid", 800, 760, False), ("narrow", 700, 760, False),
             ("tablet", 820, 1180, True), ("phone", 390, 844, True), ("land", 844, 390, True))

fails, notes = [], []
def check(ok, msg):
    (notes if ok else fails).append(("OK   " if ok else "FAIL ") + msg)

def static():
    s = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    check("**마을 ***** *차 37평" in s, "부제는 가린 표기 그대로")
    check(not re.search(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", s), "이메일 주소 없음")
    for w in FORBID: check(w not in s, "금지 낱말 없음: " + w[:1] + "*" * (len(w) - 1))
    check(not re.search(r"https?://(?!www\.w3\.org)", s), "외부 주소 없음(인터넷 없이 열림)")
    check('name="robots" content="noindex' in s, "검색 제외 표시 있음")
    m = re.search(r"const PHOTOS=\{.*?\};", s, re.S)
    used = set(re.findall(r"'(\d\d)'", m.group(0))) if m else set()
    have = set(os.path.basename(f)[:-4] for f in glob.glob(os.path.join(HERE, "photos", "*.jpg")))
    check(bool(used) and used <= have, "쓰는 사진 %d장이 모두 폴더에 있음" % len(used))
    check(have <= used, "안 쓰는 사진 파일 없음")
    check(all(re.fullmatch(r"\d\d", n) for n in have), "사진 파일 이름은 번호뿐")
    meta = [n for n in sorted(have) if any(t in open(os.path.join(HERE, "photos", n + ".jpg"), "rb").read() for t in (b"Exif", b"http://ns.adobe.com/xap"))]
    check(not meta, "사진에 촬영 정보(EXIF, XMP) 없음" + (" → " + ",".join(meta) if meta else ""))

LAYOUT = """(()=>{const vis=e=>{if(!e)return false;const c=getComputedStyle(e);return c.display!=='none'&&c.visibility!=='hidden'&&!e.hidden};
const R={};['head','side','photos','help','stick','dock'].forEach(id=>{const e=document.getElementById(id);if(vis(e)){const r=e.getBoundingClientRect();R[id]=[r.left,r.top,r.right,r.bottom]}});
const ov=[],off=[];const k=Object.keys(R);for(let i=0;i<k.length;i++){const a=R[k[i]];if(a[0]<-0.5||a[1]<-0.5||a[2]>innerWidth+0.5||a[3]>innerHeight+0.5)off.push(k[i]);for(let j=i+1;j<k.length;j++){const b=R[k[j]];if(a[0]<b[2]&&b[0]<a[2]&&a[1]<b[3]&&b[1]<a[3])ov.push(k[i]+'×'+k[j])}}
const hs=[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&!b.closest('#light')&&!b.closest('#thumbs')).map(b=>Math.round(b.getBoundingClientRect().height));
return {ov,off,minH:Math.min(...hs)}})()"""

def behave(base):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=ARGS)
        pg = b.new_page(viewport={"width": 1200, "height": 760}); errs, bad = [], []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("response", lambda r: bad.append(r.url) if r.status >= 400 else None)
        pg.goto(base); pg.wait_for_timeout(2500)
        check(pg.evaluate("!!window.THREE && !!document.querySelector('canvas#view')"), "3D 화면이 뜸")
        names = pg.evaluate("[...document.querySelectorAll('#chips button')].map(b=>b.textContent)")
        check(len(names) == 13, "방 이름 버튼 13개")
        broken = 0
        for i, n in enumerate(names):
            pg.evaluate("document.querySelectorAll('#chips button')[%d].click()" % i); pg.wait_for_timeout(600)
            check(pg.evaluate("document.getElementById('roomName').textContent") == n, "방 이름 버튼 → 그 방 안에 섬: " + n)
            check(not pg.evaluate("(()=>{const T=window.__tour;return T.blocked(T.pl.x,T.pl.z)})()"), "서는 자리가 벽·가구와 겹치지 않음: " + n)
            broken += pg.evaluate("[...document.querySelectorAll('#thumbs img')].filter(i=>!(i.complete&&i.naturalWidth>0)).length")
        check(broken == 0, "방마다 사진이 모두 뜸")
        seg = pg.evaluate("(()=>{const T=window.__tour;let bad=[];for(let i=0;i<T.TOUR.length-1;i++){const a=T.TOUR[i],b=T.TOUR[i+1];for(let t=0;t<=1;t+=0.02){if(T.blocked(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)){bad.push(i);break;}}}return bad})()")
        check(not seg, "자동 투어 경로가 막히지 않음" + (" → 구간 %s" % seg if seg else ""))
        w0 = pg.evaluate("document.getElementById('bTour').getBoundingClientRect().width")
        pg.evaluate("document.getElementById('bTour').click()"); pg.wait_for_timeout(400)
        check(abs(pg.evaluate("document.getElementById('bTour').getBoundingClientRect().width") - w0) < 0.6, "자동 투어 버튼: 글자가 바뀌어도 너비 그대로")
        check(not pg.evaluate("document.getElementById('tourCtl').hidden"), "투어 중에는 이전 방·다음 방·속도 버튼이 보임")
        pg.evaluate("document.getElementById('bTour').click()")
        w0 = pg.evaluate("document.getElementById('bTop').getBoundingClientRect().width")
        pg.evaluate("document.getElementById('bTop').click()"); pg.wait_for_timeout(400)
        check(abs(pg.evaluate("document.getElementById('bTop').getBoundingClientRect().width") - w0) < 0.6, "위에서 보기 버튼: 글자가 바뀌어도 너비 그대로")
        check(pg.evaluate("document.getElementById('bTop').getAttribute('aria-pressed')") == "true", "위에서 보기 켜짐")
        pg.evaluate("document.querySelectorAll('#chips button')[2].click()"); pg.wait_for_timeout(400)
        check(pg.evaluate("document.getElementById('bTop').getAttribute('aria-pressed')") == "true", "방 이름 버튼을 눌러도 위에서 보기 유지")
        pg.evaluate("document.getElementById('bHome').click()"); pg.wait_for_timeout(700)
        check(pg.evaluate("document.getElementById('roomName').textContent") == "전실" and pg.evaluate("document.getElementById('bTop').getAttribute('aria-pressed')") == "false", "홈 버튼 → 처음 상태")
        pg.evaluate("document.querySelector('#thumbs button').click()"); pg.wait_for_timeout(400)
        check(pg.evaluate("getComputedStyle(document.getElementById('light')).display") != "none", "실제 사진 크게 보기 열림")
        p0 = pg.evaluate("document.getElementById('lPage').textContent"); pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(200)
        check(pg.evaluate("document.getElementById('lPage').textContent") != p0 or p0.startswith("1 / 1"), "화살표 키로 사진 넘김")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
        check(pg.evaluate("getComputedStyle(document.getElementById('light')).display") == "none", "Esc로 닫힘")
        check(not errs, "실행 중 오류 없음" + (" → " + errs[0][:120] if errs else ""))
        check(not bad, "불러오기 실패 없음" + (" → " + bad[0] if bad else ""))
        for name, vw, vh, touch in VIEWPORTS:
            b.close(); b = p.chromium.launch(executable_path=CHROME, args=ARGS)   # 창 크기마다 브라우저를 새로 띄움(소프트웨어 렌더링에서 멈춤 방지)
            ctx = b.new_context(viewport={"width": vw, "height": vh}, has_touch=touch, is_mobile=touch); q = ctx.new_page()
            q.goto(base, wait_until="domcontentloaded", timeout=60000); q.wait_for_timeout(2500); states = [("기본", q.evaluate(LAYOUT))]
            if q.evaluate("getComputedStyle(document.getElementById('dock')).display") != "none":
                q.evaluate("document.getElementById('dSide').click()"); q.wait_for_timeout(300); states.append(("평면도 열림", q.evaluate(LAYOUT)))
                q.evaluate("document.getElementById('dPhotos').click()"); q.wait_for_timeout(300); states.append(("사진 열림", q.evaluate(LAYOUT)))
                q.evaluate("document.getElementById('dPhotos').click()")
            q.evaluate("document.getElementById('bHelp').click()"); q.wait_for_timeout(200); states.append(("안내 열림", q.evaluate(LAYOUT)))
            for st, r in states:
                check(not r["ov"] and not r["off"], "%s %dx%d %s: 겹침·화면 밖 없음" % (name, vw, vh, st) + (" → %s %s" % (r["ov"], r["off"]) if r["ov"] or r["off"] else ""))
            if touch: check(states[0][1]["minH"] >= 44, "%s: 터치 버튼 높이 44px 이상(최소 %d)" % (name, states[0][1]["minH"]))
            ctx.close()
        b.close()

if __name__ == "__main__":
    static()
    sock = socket.socket(); sock.bind(("127.0.0.1", 0)); port = sock.getsockname()[1]; sock.close()
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    H = functools.partial(Quiet, directory=HERE)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
    try: behave("http://127.0.0.1:%d/index.html" % port)
    finally: srv.shutdown()
    print("\n".join(notes + fails)); print("\n%d개 통과, %d개 실패" % (len(notes), len(fails)))
    sys.exit(1 if fails else 0)
