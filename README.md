# AI Security Scanner

AI 기반 웹 취약점 자동 분석 및 공격 유형 예측 시스템

## 목차
- [개요](#개요)
- [주요 기능](#주요-기능)
- [시스템 요구사항](#시스템-요구사항)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [프로젝트 구조](#프로젝트-구조)
- [기술 스택](#기술-스택)

## 개요

AI Security Scanner는 웹 애플리케이션의 보안 취약점을 자동으로 분석하고, AI를 활용하여 공격 유형을 예측하는 통합 보안 분석 도구입니다. Kali Linux 도구들과 AI 모델을 결합하여 CTF 문제나 웹 애플리케이션의 보안 상태를 진단합니다.

### 주요 특징
- GUI 기반의 직관적인 사용자 인터페이스
- Kali Linux 보안 도구 통합 (nmap, gobuster, sqlmap, hydra 등)
- AI 기반 공격 유형 자동 분류
- 취약점 분석 히스토리 관리
- JSON 형식의 상세 분석 결과 제공

## 주요 기능

### 1. 자동 취약점 스캔
- URL 또는 파일 기반 분석 지원
- Trivy를 통한 SBOM 생성 및 CVE 탐지
- 다양한 Kali Linux 도구 자동 실행

### 2. AI 공격 유형 예측
- 시나리오 기반 공격 유형 분류
- 10가지 이상의 공격 유형 지원
- BERT 기반 텍스트 분석 모델

### 3. 결과 리포트 생성
- JSON 형식의 구조화된 결과
- 실행된 도구 및 단계 추적
- Flag, 취약점, 해결 전략 정보 제공

### 4. 히스토리 관리
- 이전 분석 결과 저장
- 빠른 재분석 기능
- 프롬프트 히스토리 관리

## 시스템 요구사항

### 필수 요구사항
- Python 3.8 이상
- Kali Linux (보안 도구 사용 시) 또는 macOS/Linux
- 최소 4GB RAM
- 디스크 여유 공간 2GB 이상

### 권장 요구사항
- Python 3.10 이상
- Kali Linux 최신 버전
- 8GB 이상 RAM
- GPU 지원 (AI 모델 추론 가속)

## 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/your-repo/AI-Service-UI.git
cd AI-Service-UI
```

### 2. 가상 환경 생성 및 활성화
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. 의존성 패키지 설치

#### UI 의존성
```bash
pip install customtkinter
pip install tkinter
```

#### Kali Server 의존성
```bash
cd kali_server
pip install -r requirements.txt
cd ..
```

필수 패키지:
- Flask
- requests
- aiohttp

### 4. Kali Linux 도구 설치 (선택사항)
Kali Linux를 사용하는 경우, 다음 도구들이 설치되어 있어야 합니다:
```bash
sudo apt update
sudo apt install -y nmap gobuster dirb sqlmap hydra john wpscan enum4linux trivy
```

## 사용 방법

### 기본 사용 흐름

#### 1단계: Kali Server 실행 (백엔드)
먼저 보안 도구를 실행할 API 서버를 시작합니다:

```bash
cd kali_server
python kali_server.py
```

옵션:
- `--port <포트번호>`: 서버 포트 지정 (기본: 13680)
- `--debug`: 디버그 모드 활성화

예시:
```bash
python kali_server.py --port 13680 --debug
```

#### 2단계: UI 클라이언트 실행 (프론트엔드)
새 터미널에서 GUI 애플리케이션을 실행합니다:

```bash
cd UI
python client.py
```

### UI 화면 사용법

#### 메인 화면

애플리케이션 실행 시 처음 나타나는 화면입니다.
- **텍스트 박스**: Attack Type 또는 시나리오 입력
- **Input 버튼**: 분석 대상 입력 화면으로 이동
- **History 버튼**: 이전 분석 히스토리 확인
- **Specifications 버튼**: 분석 결과 상세 보기

#### Input 화면
분석 대상을 입력하는 화면입니다.

##### 방법 1: URL 기반 분석
1. **URL 필드**에 분석할 웹사이트 주소 입력
   ```
   예: https://example.com
   ```
2. **Start 버튼** 클릭
3. 자동 생성된 Prompt 확인

##### 방법 2: 파일 기반 분석
1. **File 필드** 옆 **Browse 버튼** 클릭
2. 분석할 파일 선택 (.csv, .txt, .xlsx 지원)
3. **Start 버튼** 클릭
4. 자동 생성된 Prompt 확인

생성되는 Prompt 예시:
```
당신은 입력한 접속 경로와 파일들을 토대로 kali mcp를 사용해서
해당 사이트의 설정 값이나 구성들을 분석해서 예측되는 시나리오를
분석해서 알려주셔야 합니다.

### 접속 정보 : https://example.com
### 파일 구성 : None
### result :
### 시나리오 : 예상되는 시나리오를 입력하면 됩니다.
```

##### 방법 3: Attack Type 입력
1. 메인 화면 텍스트 박스에 공격 유형 입력
   ```
   예: SQL Injection
   ```
2. Input 화면에서 **Start 버튼** 클릭
3. 검증용 Prompt 생성

생성되는 Prompt 예시:
```
입력한 'SQL Injection'를 토대로 실제로 해당 취약점이 있는지
판단 후, 이를 레포트 형태로 만들어주세요.
```

#### History 화면
이전에 생성된 분석 프롬프트 목록을 확인할 수 있습니다.

1. 메인 화면에서 **History 버튼** 클릭
2. 저장된 항목 목록 확인 (Entry #1, Entry #2, ...)
3. 원하는 항목 클릭 시 Specification 화면으로 이동

#### Specifications 화면
분석 결과를 JSON 형식으로 표시합니다.

결과 예시:
```json
{
    "workflow_status": "COMPLETED_SUCCESS",
    "flag": "SF{sf_flag1}",
    "solving_strategy": "secure-compare 라이브러리의 XOR 연산 버그를 이용하여 인증 우회",
    "key_insight": "a.charCodeAt(i) ^ a.charCodeAt(i) 버그로 인해 길이만 같으면 항상 0(true) 반환",
    "execution_summary": {
        "total_time": 420,
        "steps_executed": ["1", "2", "5-1", "5-2", "5-4", "6"],
        "tools_used": ["trivy", "perplexity_search", "curl", "execute_command"],
        "retry_count": 12,
        "critical_finding": "secure-compare 라이브러리의 XOR 연산 구현 버그"
    }
}
```

### 고급 사용법

#### Trivy를 이용한 취약점 스캔
프로젝트에 package-lock.json 파일이 있는 경우:

1. API 엔드포인트 호출:
```bash
curl -X POST http://localhost:13680/api/tools/trivy \
  -H "Content-Type: application/json" \
  -d '{"file_path": "/path/to/project"}'
```

2. SBOM 파일 생성 및 CVE 추출
3. 결과 JSON 응답 확인

#### Nmap 스캔
```bash
curl -X POST http://localhost:13680/api/tools/nmap \
  -H "Content-Type: application/json" \
  -d '{
    "target": "192.168.1.1",
    "scan_type": "-sCV",
    "ports": "80,443,8080",
    "additional_args": "-T4 -Pn"
  }'
```

#### SQL Injection 테스트
```bash
curl -X POST http://localhost:13680/api/tools/sqlmap \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://example.com/login.php",
    "data": "username=admin&password=test",
    "additional_args": "--level=5 --risk=3"
  }'
```

## 프로젝트 구조

```
AI-Service-UI/
├── UI/                          # 프론트엔드 GUI
│   ├── client.py               # CustomTkinter 기반 메인 UI
│   └── __init__.py
│
├── kali_server/                # 백엔드 API 서버
│   ├── kali_server.py          # Flask 기반 보안 도구 API
│   ├── mcp_server.py           # MCP 서버 구현
│   ├── requirements.txt        # 서버 의존성
│   └── __init__.py
│
├── AI/                         # AI 모델
│   ├── model.py                # 공격 유형 분류 모델
│   ├── AI_For_Security_Comment.ipynb  # 모델 학습 노트북
│   ├── flow.html               # 워크플로우 시각화
│   └── readme.md
│
├── mcp_server/                 # MCP 관련 유틸리티
│   └── utils/
│       └── result_writer.py    # 결과 저장 유틸리티
│
├── results/                    # 분석 결과 저장
│   └── sample.json
│
├── venv/                       # Python 가상 환경
├── requirement.txt             # 루트 의존성
└── README.md                   # 이 문서
```

### 주요 파일 설명

#### UI/client.py
- GUI 메인 애플리케이션
- 4개 화면 관리 (Main, Input, History, Specifications)
- Prompt 생성 및 히스토리 관리

#### kali_server/kali_server.py
- Flask 기반 REST API 서버
- 12개 보안 도구 엔드포인트 제공
- 명령 실행 타임아웃 관리

지원 도구:
- `/api/tools/nmap` - 포트 스캔
- `/api/tools/gobuster` - 디렉토리 브루트포싱
- `/api/tools/sqlmap` - SQL Injection 테스트
- `/api/tools/hydra` - 패스워드 크래킹
- `/api/tools/trivy` - 취약점 스캔
- `/api/tools/curl` - HTTP 요청
- `/api/command` - 임의 명령 실행

#### AI/model.py
- BERT 기반 공격 유형 분류
- 10가지 공격 유형 지원

## 기술 스택

### Frontend
- **CustomTkinter**: 모던한 GUI 라이브러리
- **Tkinter**: Python 표준 GUI 프레임워크

### Backend
- **Flask**: 경량 웹 프레임워크
- **Python 3.8+**: 메인 프로그래밍 언어

### Security Tools
- **Nmap**: 네트워크 스캔
- **Gobuster**: 디렉토리/파일 브루트포싱
- **SQLMap**: SQL Injection 자동화
- **Hydra**: 로그인 크래킹
- **Trivy**: 컨테이너/파일시스템 취약점 스캔
- **John the Ripper**: 패스워드 크래킹
- **WPScan**: WordPress 스캔
- **Enum4Linux**: SMB 열거

### AI/ML
- **BERT**: Transformer 기반 텍스트 분류 모델
- **PyTorch/TensorFlow**: 딥러닝 프레임워크 (선택)

## 워크플로우

```
1. 사용자 입력 (URL/File/Attack Type)
   ↓
2. Prompt 자동 생성
   ↓
3. MCP Client → Kali Server API 호출
   ↓
4. 보안 도구 실행 (nmap, trivy, sqlmap 등)
   ↓
5. 스캔 결과 수집
   ↓
6. AI 모델 분석 (공격 유형 예측)
   ↓
7. 결과 JSON 생성 및 표시
```

## 환경 변수

### Kali Server
```bash
export API_PORT=13680          # API 서버 포트
export DEBUG_MODE=1            # 디버그 모드 활성화
export COMMAND_TIMEOUT=3600    # 명령 타임아웃 (초)
```

## 트러블슈팅

### 1. Kali 도구가 없다는 오류
**증상**: "Tool not found" 오류 발생

**해결**:
```bash
# 도구 설치 확인
which nmap gobuster sqlmap

# 없는 도구 설치
sudo apt install <도구명>
```

### 2. 서버 연결 오류
**증상**: UI에서 서버에 연결할 수 없음

**해결**:
1. Kali Server가 실행 중인지 확인
2. 포트 번호 확인 (기본: 13680)
3. 방화벽 설정 확인

### 3. 타임아웃 오류
**증상**: 명령 실행 중 타임아웃 발생

**해결**:
```bash
# 타임아웃 시간 증가
export COMMAND_TIMEOUT=7200
python kali_server.py
```

### 4. Permission Denied
**증상**: 보안 도구 실행 권한 없음

**해결**:
```bash
# sudo 권한으로 서버 실행
sudo python kali_server.py
```

## API 레퍼런스

### Health Check
```http
GET /health
```

응답:
```json
{
  "status": "healthy",
  "message": "Kali Linux Tools API Server is running",
  "tools_status": {
    "nmap": true,
    "gobuster": true,
    "dirb": true,
    "nikto": true
  },
  "all_essential_tools_available": true
}
```

### 일반 명령 실행
```http
POST /api/command
Content-Type: application/json

{
  "command": "ls -la"
}
```

### Nmap 스캔
```http
POST /api/tools/nmap
Content-Type: application/json

{
  "target": "192.168.1.1",
  "scan_type": "-sCV",
  "ports": "80,443",
  "additional_args": "-T4 -Pn"
}
```

### Trivy 스캔
```http
POST /api/tools/trivy
Content-Type: application/json

{
  "file_path": "/path/to/project"
}
```

## 보안 고려사항

이 도구는 보안 교육 및 승인된 테스트 환경에서만 사용해야 합니다.

- 무단 침투 테스트 금지
- CTF 대회 및 교육 목적으로만 사용
- 본인이 소유하거나 명시적 허가를 받은 시스템에만 사용
- 악의적 목적 사용 금지

## 라이선스

이 프로젝트는 교육 목적으로 제공됩니다.

## 기여

버그 리포트나 기능 제안은 Issues를 통해 제출해주세요.

## 참고 자료

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Kali Linux Documentation](https://www.kali.org/docs/)
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 연락처

문의사항이 있으시면 이슈를 생성하거나 프로젝트 관리자에게 연락해주세요.

---

**주의**: 이 도구는 교육 및 합법적인 보안 테스트 목적으로만 사용되어야 합니다.
