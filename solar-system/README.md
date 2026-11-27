# 태양계 3D 모형

Fable 5.2와 대화하며 만든 태양계 3D 모형입니다. 코드는 직접 쓰지 않았습니다.

- 바로 보기: https://claude.ai/artifact/STZWnwywuAohy7BuW7hbT6
- 작업 기간: 2026.11.12 ~ 2026.11.13 
- 작업 시간: 약 8시간
- 대상: 초등 6학년~중학생 과학 수업

## 파일

| 파일 | 내용 |
|---|---|
| `index.html` | 모형 전체. 브라우저로 열면 됩니다(인터넷 연결 필요). |
| `fonts/PretendardVariable.woff2` | 한글 글꼴. `index.html`과 같은 위치의 `fonts` 폴더에 두어야 합니다. |
| `DESIGN.md` | 색, 서체, 배치, 움직임, 유니버설 디자인 기준을 정리한 디자인 시스템 문서 |
| `check.py` | 게시 전에 돌린 자동 점검 스크립트(85개 항목). 작업 환경 경로에 맞춰져 있어 그대로는 실행되지 않습니다. |
| `linkedin-post.md` | 작업 후기 |
| `[Fable] 3D solor system_20261113.mp4`, `[Fable] 3D solor system_20261113.gif` | 시연 영상(18초). 지구, 달, 토성을 차례로 선택하는 장면 |

## 사용한 것

- [Three.js](https://threejs.org/) r128 (MIT)
- [Pretendard](https://github.com/orioncactus/pretendard), [Space Mono](https://fonts.google.com/specimen/Space+Mono) (SIL Open Font License)
- 지구 해안선: [Natural Earth](https://www.naturalearthdata.com/) 1:110m (퍼블릭 도메인)
- 궤도 요소: NASA JPL J2000 평균 궤도 요소
