# Cloudflare Pages 빌드 설정 가이드

## 현재 상황
이 프로젝트는 Flask (Python) 웹 애플리케이션입니다. Cloudflare Pages는 주로 정적 사이트를 위한 플랫폼이지만, Python Functions를 통해 서버리스 함수를 실행할 수 있습니다.

## Cloudflare Pages 빌드 설정

### 기본 설정
- **Framework preset**: `None` (또는 `Python`이 있다면 선택)
- **Build command**: (비워둠)
- **Build output directory**: `/` 또는 `/public` (정적 파일이 있는 경우)

### 주의사항
⚠️ **중요**: Flask 앱은 Cloudflare Pages에서 직접 실행할 수 없습니다. 다음 옵션을 고려하세요:

## 옵션 1: Cloudflare Pages Functions 사용
각 Flask 라우트를 별도의 Functions 파일로 변환해야 합니다:
- `functions/api/generate_problem/[topic_name].py`
- `functions/topic/[topic_name].py`
- 등등...

## 옵션 2: Cloudflare Workers 사용
Flask 앱을 Cloudflare Workers로 배포 (Python Workers 지원 필요)

## 옵션 3: 다른 플랫폼 사용 (권장)
Flask 앱을 배포하기에 더 적합한 플랫폼:
- **Render**: https://render.com (무료 플랜 제공)
- **Railway**: https://railway.app
- **Fly.io**: https://fly.io
- **Heroku**: https://heroku.com

## Render 배포 예시
1. GitHub에 코드 푸시
2. Render에서 새 Web Service 생성
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python app.py`

## Cloudflare Pages에서 정적 파일만 배포
만약 정적 파일만 배포하고 싶다면:
- **Build command**: (비워둠)
- **Build output directory**: `/static` 또는 `/public`

하지만 이 경우 API 엔드포인트는 작동하지 않습니다.
