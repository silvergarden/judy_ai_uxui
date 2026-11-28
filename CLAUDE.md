# 이 저장소에서 일하는 Claude에게

권정은(kwonjeongeun)의 포트폴리오 저장소입니다. 사용자는 GitHub를 잘 모릅니다. "포트폴리오에 올려 줘", "새 작업 올려 줘"라고만 말해도 아래 순서대로 끝까지 해 주세요.

## 새 작업 올리기

1. 저장소를 처음부터 새로 받는다(`git clone`). 예전 사본은 쓰지 않는다. 이력을 정리한 적이 있어서 옛 사본에서 push하면 지운 사진이 되살아날 수 있다.
2. 새 브랜치를 만든다.
3. 작업 폴더를 만든다. 영문 소문자와 `-`만 쓴다. 결과물은 `index.html`, 설명은 `_template/README.md`를 복사해 채운다.
4. `_template/CHECKLIST.md`의 개인 정보 항목을 확인한다. 실제 집·얼굴·주소·전화번호 사진은 올리지 않는다.
5. 시연 GIF를 폴더에 넣는다(5MB 이하).
6. `works.json`의 `works`에 한 덩어리를 추가한다. 형식은 파일 맨 위 `_사용법`에 있다.
7. `python3 scripts/build_home.py`를 돌려 README와 `index.html`의 작업 목록을 다시 만든다. 이 두 곳의 작업 목록은 손으로 고치지 않는다.
8. PR을 열고 자동 점검이 통과하면 squash로 합친다.
9. 1~2분 뒤 `https://silvergarden.github.io/kwonjeongeun_ai_uxui/폴더이름/`이 열리는지 확인하고, 사용자에게 바로 보기 링크를 알려 준다.

## 지킬 것

- 커밋 작성자 이름은 `kwonjeongeun`, 이메일은 `46354124+silvergarden@users.noreply.github.com`.
- 이메일 주소를 README나 페이지에 글자로 적지 않는다. 사이트 첫 화면의 [이메일 복사] 버튼만 쓴다.
- `room-tour/photos/`는 올리지 않는다(`.gitignore`에 있음).
- 사용자가 GitHub에서 직접 고친 문구는 그대로 둔다. `works.json`과 다르면 사용자 문구에 맞춰 `works.json`을 고친다.
