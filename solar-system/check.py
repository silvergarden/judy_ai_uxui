#!/usr/bin/env python3
"""태양계 3D 모형 점검 스크립트.
게시 전에 실행한다: python3 check.py
헤드리스 크롬(소프트웨어 렌더링)으로 페이지를 열어 세 가지 창 크기에서 동작을 확인하고,
캡처를 /tmp/check/ 에 남긴다. 실패가 하나라도 있으면 종료 코드 1."""
import re, os, sys, json
from playwright.sync_api import sync_playwright

SRC = "/home/claude/solar-system.html"
OUT = "/tmp/check"
LIB = "/tmp/test/lib"          # three.js r128과 examples/js 사본
FONT = "/tmp/fnt/node_modules/@fontsource/space-mono"
os.makedirs(OUT, exist_ok=True)

def build():
    s = open(SRC).read()
    t = s.replace("https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js", LIB + "/three.min.js")
    t = re.sub(r"https://cdn\.jsdelivr\.net/npm/three@0\.128\.0/examples/js/\w+/(\w+\.js)", LIB + r"/\1", t)
    t = re.sub(r'<link href="https://fonts.googleapis.com[^>]*>',
               "".join('<link rel="stylesheet" href="%s/%s.css">' % (FONT, w) for w in ("400", "700")), t)
    t = t.replace('url("fonts/PretendardVariable.woff2")', 'url("/home/claude/fonts/PretendardVariable.woff2")')
    # 측정용 계측: 프레임마다 갱신(JS) 시간과 전체 시간, 그리고 렌더러 통계
    t = t.replace("  function frame(now) {", "  function frame(now) { var __a = performance.now();", 1)
    t = t.replace("    if (useBloom) composer.render(dt); else renderer.render(scene, camera);",
                  "    var __b = performance.now();\n    if (useBloom) composer.render(dt); else renderer.render(scene, camera);\n    var __c = performance.now();", 1)
    t = t.replace("    requestAnimationFrame(frame);\n  }",
                  "    (window.__perf = window.__perf || []).push([__b - __a, __c - __b, performance.now() - __c]);\n"
                  "    window.__info = { calls: renderer.info.render.calls, tris: renderer.info.render.triangles, points: renderer.info.render.points, lines: renderer.info.render.lines, geos: renderer.info.memory.geometries, texs: renderer.info.memory.textures };\n"
                  "    requestAnimationFrame(frame);\n  }", 1)
    assert "__perf" in t and "__b" in t
    p = OUT + "/index.html"
    open(p, "w").write(t)
    return p

fails, notes = [], []
def check(ok, msg):
    (notes if ok else fails).append(("OK   " if ok else "FAIL ") + msg)

def run():
    page_path = build()
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
                                                      "--ignore-gpu-blocklist", "--allow-file-access-from-files"])
        for (w, h) in ((1100, 680), (800, 860), (390, 760), (393, 615), (1920, 1080)):
            tag = "%dx%d" % (w, h)
            pg = b.new_page(viewport={"width": w, "height": h})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.add_init_script("window.__z=[];(function f(){var e=document.getElementById('zoomPct');if(e&&e.textContent!=='100%'||window.__z.length)window.__z.push(parseInt(e.textContent));requestAnimationFrame(f)})()")
            pg.goto("file://" + page_path); pg.wait_for_timeout(6500)
            z = pg.evaluate("window.__z")
            seq = [v for i, v in enumerate(z) if i == 0 or v != z[i - 1]]
            check(len(seq) > 1 and seq[0] == 30 and seq[-1] == 50 and all(a <= b_ for a, b_ in zip(seq, seq[1:])),
                  "%s 도입 연출 30%%→50%% 한 방향 (%s…%s, %d단계)" % (tag, seq[:2], seq[-1:], len(seq)))
            pg.screenshot(path="%s/%s_home.png" % (OUT, tag))
            fonts = pg.evaluate("[...document.fonts].filter(f=>f.status=='loaded').map(f=>f.family).filter((v,i,a)=>a.indexOf(v)==i)")
            check("Space Mono" in fonts and "Pretendard KR" in fonts, "%s 글꼴 로딩 %s" % (tag, fonts))
            check(pg.get_attribute("#fx", "aria-pressed") == "false", "%s 빛 번짐 기본 꺼짐" % tag)
            w1 = pg.evaluate("document.getElementById('play').offsetWidth"); pg.click("#play")
            w2 = pg.evaluate("document.getElementById('play').offsetWidth")
            check(w1 == w2, "%s 재생/일시정지 버튼 폭 동일 (%s, %s)" % (tag, w1, w2))
            before = pg.evaluate("document.querySelectorAll('.label')[8].style.transform")
            ob = pg.evaluate("(function(){var r=document.getElementById('orb').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()")
            pg.mouse.move(ob[0], ob[1]); pg.mouse.down(); pg.mouse.move(ob[0] + 30, ob[1] - 12, steps=5); pg.mouse.up(); pg.wait_for_timeout(400)
            after = pg.evaluate("document.querySelectorAll('.label')[8].style.transform")
            check(before != after, "%s 회전 구를 끌면 시점이 돈다" % tag)
            shown = pg.evaluate("document.getElementById('orbReset').classList.contains('on')")
            pg.click("#orbReset"); pg.wait_for_timeout(1600)
            back = pg.evaluate("document.querySelectorAll('.label')[8].style.transform")
            nums = lambda t: [float(x) for x in re.findall(r"-?\d+\.?\d*", t)][-2:]
            close = all(abs(a - b_) < 3 for a, b_ in zip(nums(before), nums(back)))
            hid = not pg.evaluate("document.getElementById('orbReset').classList.contains('on')")
            check(shown and close and hid, "%s 되돌리기 버튼: 돌리면 나타나고, 누르면 처음 방향으로 돌아가고 숨는다 (%s → %s)" % (tag, nums(before), nums(back)))
            pg.click("#moreBtn"); pg.wait_for_timeout(300)
            r = pg.evaluate("(function(){var m=document.getElementById('more').getBoundingClientRect(),z=document.getElementById('zoom').getBoundingClientRect();return [m.right,z.left,m.bottom,z.top,z.bottom,m.top]})()")
            overlap = r[0] > r[1] and not (r[2] <= r[3] or r[5] >= r[4])
            check(not overlap, "%s 설정 판과 줌 UI 겹치지 않음" % tag)
            pg.screenshot(path="%s/%s_settings.png" % (OUT, tag))
            pg.click("#chips button >> nth=6"); pg.wait_for_timeout(3200)
            if w <= 640 and not pg.evaluate("document.getElementById('more').hidden"): pg.click("#moreBtn")
            g = pg.evaluate("(function(){var c=document.getElementById('card').getBoundingClientRect(),r=document.getElementById('retC');return {hidden:document.getElementById('card').hidden,cl:c.left,ct:c.top,cx:+r.getAttribute('cx'),cy:+r.getAttribute('cy'),disp:document.getElementById('retG').style.display,zoom:document.getElementById('zoomPct').textContent}})()")
            check(not g["hidden"] and g["disp"] != "none", "%s 천체 선택 시 카드와 조준 표시" % tag)
            ov = pg.evaluate("(function(){function R(q){return document.querySelector(q).getBoundingClientRect()}function hit(a,b){return !(a.right<=b.left||b.right<=a.left||a.bottom<=b.top||b.bottom<=a.top)}var z=R('#zoom'),c=R('#card'),h=R('.about summary'),r=document.getElementById('retC'),cy=+r.getAttribute('cy'),rr=+r.getAttribute('r');return {zc:hit(z,c),top:Math.round(cy-rr-15),hb:Math.round(h.bottom),bot:Math.round(cy+rr+15),ct:Math.round(c.top)}})()")
            check(not ov["zc"], "%s 줌 UI와 정보 카드 겹치지 않음" % tag)
            if w <= 640: check(ov["top"] >= ov["hb"] - 2 and ov["bot"] <= ov["ct"] + 2, "%s 조준 표시가 머리글과 카드 사이에 들어옴 (표시 %d~%d, 빈자리 %d~%d)" % (tag, ov["top"], ov["bot"], ov["hb"], ov["ct"]))
            if w > 640:
                ld = pg.evaluate("(function(){var p=document.getElementById('retL').getAttribute('points')||'';var n=p.split(/[ ,]+/).map(Number);var s=document.getElementById('scrim').getBoundingClientRect();return {pts:p.length>0,x:n[2]||0,y:n[3]||0,sr:s.right,sb:s.bottom}})()")
                check(ld["pts"] and (ld["x"] > ld["sr"] * 0.62 or ld["y"] > ld["sb"] - 40), "%s 천체와 카드를 잇는 선이 보인다 (꺾이는 점 x=%d, y=%d / 받침 오른쪽 %d, 아래 %d)" % (tag, ld["x"], ld["y"], ld["sr"], ld["sb"]))
            if w > 640: check(g["cx"] < g["cl"], "%s 선택한 천체 중심이 카드 왼쪽 (중심 x=%d, 카드 왼쪽=%d)" % (tag, g["cx"], g["cl"]))
            else: check(g["cy"] < g["ct"], "%s 선택한 천체 중심이 카드 위 (중심 y=%d, 카드 위=%d)" % (tag, g["cy"], g["ct"]))
            check(g["zoom"] == "100%", "%s 선택 직후 줌 100%% (%s)" % (tag, g["zoom"]))
            pg.screenshot(path="%s/%s_focus.png" % (OUT, tag))
            if not pg.evaluate("document.getElementById('more').hidden") is False: pg.click("#moreBtn")
            pg.click("#chips button >> nth=10"); pg.wait_for_timeout(2600)
            mo = pg.evaluate("[document.querySelector('#card h2').textContent, (document.getElementById('liveP')||{}).textContent||'', document.getElementById('speedOut').textContent]")
            check(mo[0].startswith("달") and len(mo[1]) > 0 and mo[2] != "1초에 31일", "%s 달 선택: 카드, 위상, 느려진 시간 흐름 %s" % (tag, mo))
            qz = pg.evaluate("(function(){var q=document.querySelector('#cardBody .quiz');if(!q)return [0,''];q.open=true;var t=document.querySelector('#cardBody .term');t.click();return [document.querySelectorAll('#cardBody .quiz').length, document.getElementById('tip').hidden?'':document.getElementById('tipD').textContent]})()")
            hh = pg.evaluate("(function(){var c=document.getElementById('card'),q=c.querySelectorAll('.quiz'),i;for(i=0;i<q.length;i++)q[i].open=false;var a=c.offsetHeight;for(i=0;i<q.length;i++)q[i].open=true;return [a,c.offsetHeight]})()")
            check(hh[0] == hh[1] and hh[0] > 0, "%s 질문을 펼쳐도 카드 크기가 그대로 %s" % (tag, hh))
            check(qz[0] >= 1 and len(qz[1]) > 5, "%s 카드에 탐구 질문이 있고 낱말을 누르면 풀이가 뜬다 %s" % (tag, qz))
            pg.keyboard.press("Escape")
            pg.click("#home"); pg.wait_for_timeout(2200)
            st = pg.evaluate("[document.getElementById('card').hidden, document.getElementById('zoomPct').textContent, document.getElementById('play').dataset.state]")
            check(st == [True, "50%", "playing"], "%s 홈으로 되돌리기 %s" % (tag, st))
            check(not errs, "%s 콘솔 오류 없음 %s" % (tag, errs[:2]))
            if w == 1100:
                perf = pg.evaluate("window.__perf.slice(-120)"); info = pg.evaluate("window.__info")
                avg = [sum(x[i] for x in perf) / len(perf) for i in range(3)]
                notes.append("PERF 프레임당 평균: 갱신(JS) %.1fms, 그리기 호출 %.1fms(소프트웨어 렌더링이라 참고용), 라벨·DOM %.1fms" % tuple(avg))
                notes.append("PERF 장면 총량: 그리기 호출 %(calls)d회, 삼각형 %(tris)d, 점 %(points)d, 선 %(lines)d, 지오메트리 %(geos)d, 텍스처 %(texs)d" % info)
                json.dump({"avg_ms": avg, "info": info}, open(OUT + "/perf.json", "w"))
            pg.close()
        b.close()

run()
print("\n".join(notes + fails))
print("\n결과: %s (통과 %d, 실패 %d)" % ("실패" if fails else "통과", len([n for n in notes if n.startswith("OK")]), len(fails)))
sys.exit(1 if fails else 0)
