# Stock News Collector

주식 관련 뉴스를 자동으로 수집하고 Google Sheets에 업데이트하는 프로젝트입니다.

## 주요 기능

- 국내 주식 뉴스 수집 (네이버 금융, Google RSS)
- 해외 주식 뉴스 수집 (Yahoo Finance, NewsAPI, Google RSS)
- CNBC 뉴스 수집 및 한국어 번역
- Google Sheets 자동 업데이트
- 띄어쓰기 및 특수문자가 있는 종목명 처리
- 오류 처리 및 재시도 메커니즘

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/vanillefatale/stocknews.git
cd stocknews
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate     # Linux/Mac
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가:
```
GOOGLE_SHEET_ID=your_sheet_id
CLAUDE_API_KEY=your_claude_api_key
NEWSAPI_KEY=your_newsapi_key
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret
```

5. Google Sheets API 설정
- Google Cloud Console에서 프로젝트 생성
- Google Sheets API 활성화
- 서비스 계정 생성 및 키 다운로드
- `creds.json` 파일을 프로젝트 루트에 저장

## 사용 방법

1. 모든 뉴스 수집 실행
```bash
python run.py
```

2. 개별 뉴스 소스 실행
```bash
python news_cnbc.py      # CNBC 뉴스만 수집
python global_news.py    # 해외 뉴스만 수집
python kr_news.py        # 국내 뉴스만 수집
```

## 프로젝트 구조

```
stocknews/
├── run.py                # 메인 실행 파일
├── news_cnbc.py          # CNBC 뉴스 수집
├── global_news.py        # 해외 뉴스 수집
├── kr_news.py            # 국내 뉴스 수집
├── src/
│   ├── collectors/       # 뉴스 수집기
│   │   ├── yahoo.py      # Yahoo Finance 뉴스
│   │   ├── newsapi.py    # NewsAPI 뉴스
│   │   └── naver.py      # 네이버 뉴스
│   ├── config/           # 설정 파일
│   │   ├── sheet.py      # Google Sheets 설정
│   │   ├── env.py        # 환경 변수 설정
│   │   └── settings.py   # 전역 설정
│   └── utils/            # 유틸리티
│       ├── sheets.py     # 시트 관련 유틸리티
│       └── translator.py # 번역 유틸리티
├── requirements.txt      # 의존성 목록
└── .env                 # 환경 변수
```

## 최근 업데이트

- URL 인코딩 추가: 띄어쓰기 및 특수문자가 있는 종목명 처리
- 예외 처리 강화: 한 종목에서 오류가 발생해도 전체 스크립트가 중단되지 않도록 개선
- API 호출 간 간격 추가: 요청 제한에 도달하지 않도록 조정
- CNBC 뉴스 번역 개선: 더 자연스러운 한국어 번역 제공
- 시트 업데이트 방식 개선: 배치 업데이트로 성능 향상

## 라이선스

MIT License

## 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 