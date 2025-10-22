# 🧠 MCP 기반 로컬 웹 보안 헬스 체크러 — Tier A (Sklearn Model) Process Readme

## 📌 개요
본 문서는 MCP Server와 Kali 환경을 기반으로 로컬 HTTP 응답 메타데이터를 수집하고,  
Scikit-learn 모델을 통해 웹 보안 헬스 점수를 자동 판정하는 과정과 구조를 정리한 문서입니다.  
UI 출력은 Tkinter로 구현되며, 모든 동작은 로컬 환경에서 수행됩니다.

---

## ⚙️ 시스템 아키텍처

### 전체 흐름
```
Local URL / File  →  Claude MCP Client ↔ Kali MCP Server  
                      →  Result (JSON) →  Sklearn AI 모델 추론  
                      →  Tkinter UI 표시
```

| 구성요소 | 역할 |
|-----------|-------|
| **MCP Client (Claude Desktop)** | 사용자의 입력(로컬 URL 또는 파일)을 전송 및 명령 제어 |
| **MCP Server (Kali)** | HTTP 요청 실행, 응답 헤더/쿠키 수집, JSON 결과 생성 |
| **AI 모듈 (Scikit-learn)** | 수집된 헤더 피처 기반 보안 규칙별 자동 판정 및 헬스 스코어 예측 |
| **Tkinter UI** | JSON 결과 렌더링 및 시각화(상태 요약, 스코어 게이지 등) |

---

## 🔍 보안 진단 기준 (Reference)

| 출처 | 주요 참고 항목 |
|------|----------------|
| **KISA 소프트웨어 보안약점 진단 가이드** | 응답 헤더 · CSP · 쿠키 보안 항목 기준 정의 |
| **OWASP HTTP Security Headers Cheat Sheet** | X-Frame-Options, CSP, HSTS 권장 값 |
| **OWASP WSTG v4 – Test for Header Misconfigurations** | 보안 헤더 미설정/오구성 테스트 방법 |
| **ResearchGate (HTTP Header Adoption 연구)** | 실제 웹사이트 헤더 채택 비율 및 보안 수준 분석 |

---

## 🧩 데이터셋 설계

- **형식:** `JSONL`  
- **필드:** `id`, `url`, `headers`, `status_code`, `body_snippet`, `rule_labels`, `health_score`
- **라벨 생성:** MCP 서버 내 `rules_engine.py` 에서 자동 생성  
- **샘플 수:** 권장 ≥ 500 (목표 1,000)

### 규칙 라벨 예시 (총 10개)
| 항목 | 기준 |
|------|------|
| `csp_ok` | Content-Security-Policy 존재 및 적절 여부 |
| `x_frame_ok` | X-Frame-Options 설정(DENY/SAMEORIGIN) |
| `x_content_type_ok` | X-Content-Type-Options: nosniff |
| `hsts_ok` | HTTPS + Strict-Transport-Security 존재 |
| `referrer_policy_ok` | Referrer-Policy 설정 권장값 |
| `cookie_secure_ok` / `cookie_httponly_ok` / `cookie_samesite_ok` | Set-Cookie 속성 점검 |
| `no_mixed_content_ok` | HTTP 자원 혼합 사용 금지 |
| `powered_by_leak_ok` | 서버정보 노출 금지 |

### 헬스 스코어 계산
```
score = (Σ(rule_i · weight_i) / Σ(weight_i)) × 100
```
> 기본 weight = 1, CSP/쿠키 관련 항목은 1.5 배 가중치.

---

## 🧠 Tier A 모델 (Sklearn 구성)

### 모델 구성요소
| 구분 | 내용 |
|------|------|
| 입력 피처 | 헤더 존재 여부 + 값 매핑 + 쿠키 속성 + 프로토콜/상태 정보 |
| 모델1 | `OneVsRestClassifier(LogisticRegression)` → 규칙별 OK/Not-OK 판정 |
| 모델2 | `Ridge Regression` → 헬스 점수 회귀 예측 |
| 지표 | 규칙별 F1-macro ≥ 0.70 , RMSE ≤ 10.0 |
| 데이터 분할 | train 70 % / val 15 % / test 15 % |

### 주요 코드 경로
```
ml_training/
 ├── feature_extractor.py   # 헤더/쿠키 → 수치 피처 변환
 ├── train_sklearn.py       # LogReg · Ridge 모델 학습 및 평가
 ├── models/                # 저장된 .pkl 파일
 └── data/                  # MCP 수집 JSON 결과
```

---

## 🧮 학습 프로세스

1. **데이터 빌드** — `results/*.json` → `build_dataset.py` 실행  
2. **특징 추출** — 헤더/쿠키 존재 여부 + 값 분석 → numpy feature vector 화  
3. **라벨 생성** — 룰엔진 기준으로 OK/Not-OK + Health Score 자동 주입  
4. **모델 학습** — `train_sklearn.py` 에서 LogReg/Ridge 모델 학습  
5. **성능 평가** — F1, RMSE 출력 → 결과 저장(`models/*.pkl`)  
6. **통합** — MCP `scan_url` 결과 JSON 내 AI 추론값 추가 필드
   ```json
   "ai": {
     "rules_pred": { "csp_ok": 1, "x_frame_ok": 0, ... },
     "score_pred": 83.5,
     "model": "ovr_logreg_v1"
   }
   ```

---

## 💡 Tkinter UI 표시

- AI 결과 탭 추가 : 규칙별 체크 상태 + Health Score 게이지  
- 결과 저장 : CSV 및 PNG 익스포트  
- 불일치 항목 하이라이트 : `rule vs ai pred` 비교 색상 표시

---

## 🧱 프로젝트 디렉터리 (최종 형태)

```
project_root/
 ├── mcp_server.py
 ├── kali_server.py
 ├── rules_engine.py
 ├── ml_training/
 │    ├── feature_extractor.py
 │    ├── train_sklearn.py
 │    ├── models/
 │    └── data/
 ├── ui/
 │    ├── main_view.py     # Tkinter UI
 │    ├── assets/
 │    └── style.css
 ├── results/
 │    └── *.json
 ├── docs/
 │    └── process_readme.md (← 현재 문서)
 ├── requirements.txt
 └── README.md
```

---

## 🔎 성과 및 확장 방향

| 구분 | 설명 |
|------|------|
| 단기 목표 | 로컬 웹앱 보안 헬스 점검 자동화 및 시각화 완성 |
| 중기 목표 | 데이터셋 확대 (≥ 1,000) 및 모델 성능 향상 (F1 > 0.75) |
| 장기 확장 | CNN/RNN 모델 (Tier B/C) 적용 및 LLM 기반 설정 추천 모듈 추가 |

---

## 📚 참고 문헌 / Reference

- **KISA.** 「소프트웨어 보안약점 진단가이드 v2.0」, 2023. 한국인터넷진흥원.  
- **OWASP.** *HTTP Security Headers Cheat Sheet*, 2024. [cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)  
- **OWASP.** *Web Security Testing Guide v4*, 2024.  
- **ResearchGate.** “Analysis of the Adoption of Security Headers in HTTP”, 2017.  
- **Scikit-learn Documentation.** Logistic Regression, One-Vs-Rest, Ridge Regression API Guide.  

---

## 🧾 작성 정보
- **작성자:** 이정민 (정보보호학과 / SecurityFirst 회장)  
- **파일명:** `docs/process_readme.md`  
- **버전:** v1.0.0 (2025-10 기준)
