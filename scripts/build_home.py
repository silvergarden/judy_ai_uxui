"""works.json을 읽어 README.md와 index.html의 작업 목록 부분을 다시 쓴다.

- 최신 작업: 날짜가 가장 최근인 3개 (GIF 카드)
- 전체 작업: 모든 작업을 최신순 표로

각 파일의 <!-- works:latest:start --> ~ end, <!-- works:all:start --> ~ end 사이만 바꾸고 나머지는 건드리지 않는다.
실행: python3 scripts/build_home.py          (파일을 고침)
      python3 scripts/build_home.py --check  (고칠 것이 있으면 실패, 자동 점검용)
"""
import html, json, os, re, sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://silvergarden.github.io/kwonjeongeun_ai_uxui/"
REPO = "https://github.com/silvergarden/kwonjeongeun_ai_uxui"
LATEST = 3
NEED = ["folder", "title", "date", "summary", "oneLine", "hours", "roles", "gif", "gifAlt", "docs"]


def load():
    with open(os.path.join(ROOT, "works.json"), encoding="utf-8") as f:
        works = json.load(f)["works"]
    errs = []
    for i, w in enumerate(works):
        miss = [k for k in NEED if k not in w]
        if miss:
            errs.append("%d번째 작업(%s)에 빠진 칸: %s" % (i + 1, w.get("title", "?"), ", ".join(miss)))
            continue
        if not re.fullmatch(r"\d{4}-\d\d-\d\d", w["date"]):
            errs.append("%s: date는 YYYY-MM-DD 모양이어야 합니다" % w["title"])
        for p in [w["gif"]] + [d["file"] for d in w["docs"]] + ["index.html"]:
            if not os.path.exists(os.path.join(ROOT, w["folder"], p)):
                errs.append("%s: %s/%s 파일이 없습니다" % (w["title"], w["folder"], p))
    if errs:
        sys.exit("works.json 오류\n- " + "\n- ".join(errs))
    return sorted(works, key=lambda w: w["date"], reverse=True)


def dot(d, spaced):
    y, m, dd = d.split("-")
    return "%s. %s. %s." % (y, m, dd) if spaced else "%s.%s.%s" % (y, m, dd)


def url(folder, name=""):
    return quote(folder) + "/" + quote(name)


def readme_latest(works):
    out = []
    for w in works[:LATEST]:
        f = w["folder"]
        links = ["[바로 보기](%s%s/)" % (SITE, f), "[작업 설명](%s/)" % f]
        links += ["[%s](%s)" % (d["label"], url(f, d["file"])) for d in w["docs"]]
        out.append("### %s (%s)\n\n%s\n\n내가 한 일: %s\n\n%s\n\n![%s](%s)"
                   % (w["title"], dot(w["date"], False), w["summary"], w["roles"], " · ".join(links), w["gifAlt"], url(f, w["gif"])))
    return "\n\n".join(out)


def readme_all(works):
    rows = ["| 날짜 | 작업 | 한 줄 설명 | 작업 시간 | 링크 |", "|---|---|---|---|---|"]
    for w in works:
        f = w["folder"]
        # 작업 이름에 작업 설명(폴더) 링크를 걸고, 링크 칸에는 바로 보기만 둔다. &nbsp;로 짧은 칸이 두 줄로 깨지지 않게 한다.
        rows.append("| %s | [%s](%s/) | %s | %s | [바로&nbsp;보기](%s%s/) |"
                    % (dot(w["date"], False), w["title"], f, w["oneLine"], w["hours"].replace(" ", "&nbsp;"), SITE, f))
    return "\n".join(rows)


def page_latest(works):
    e = html.escape
    out = []
    for w in works[:LATEST]:
        f = w["folder"]
        out.append("""    <li>
      <img loading="lazy" src="%s" alt="%s">
      <div class="body">
        <span class="date">%s</span>
        <h2>%s</h2>
        <p>%s</p>
        <p class="role"><b>내가 한 일</b> %s</p>
        <div class="links"><a class="btn go" href="%s/">바로 보기</a><a class="btn doc" href="%s/tree/main/%s">작업 설명</a></div>
      </div>
    </li>""" % (e(url(f, w["gif"])), e(w["gifAlt"]), dot(w["date"], True), e(w["title"]), e(w["summary"]), e(w["roles"]), e(f), REPO, e(f)))
    return "\n".join(out)


def page_all(works):
    e = html.escape
    return "\n".join('          <tr><td class="date">%s</td><td><a href="%s/">%s</a></td><td>%s</td><td>%s</td></tr>'
                     % (dot(w["date"], False), e(w["folder"]), e(w["title"]), e(w["oneLine"]), e(w["hours"])) for w in works)


def put(text, name, body, path):
    a, b = "<!-- works:%s:start -->" % name, "<!-- works:%s:end -->" % name
    pat = re.compile(re.escape(a) + r".*?" + re.escape(b), re.S)
    if len(pat.findall(text)) != 1:
        sys.exit("%s에 %s ~ %s 표시가 한 쌍 있어야 합니다" % (path, a, b))
    return pat.sub(lambda m: a + "\n" + body + "\n" + b, text)


def main():
    works = load()
    plan = {
        "README.md": [("latest", readme_latest(works)), ("all", readme_all(works))],
        "index.html": [("latest", page_latest(works)), ("all", page_all(works))],
    }
    changed = []
    for path, parts in plan.items():
        full = os.path.join(ROOT, path)
        with open(full, encoding="utf-8") as f:
            old = f.read()
        new = old
        for name, body in parts:
            new = put(new, name, body, path)
        if new != old:
            changed.append(path)
            if "--check" not in sys.argv:
                with open(full, "w", encoding="utf-8") as f:
                    f.write(new)
    if "--check" in sys.argv and changed:
        sys.exit("works.json과 맞지 않는 파일: " + ", ".join(changed))
    print("바뀐 파일: " + (", ".join(changed) if changed else "없음"))


if __name__ == "__main__":
    main()
