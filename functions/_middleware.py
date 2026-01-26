from flask import Flask
import sys
import os

# Cloudflare Pages Functions에서 Flask 앱을 실행하기 위한 어댑터
# 이 파일은 Cloudflare Pages Functions의 _middleware.py로 사용됩니다

app = Flask(__name__)

# 원본 app.py의 내용을 여기에 통합하거나 import 해야 합니다
# 하지만 Cloudflare Pages Functions는 Flask를 직접 지원하지 않으므로
# 다른 접근이 필요합니다

def on_request(request):
    """Cloudflare Pages Functions 요청 핸들러"""
    # Flask 앱을 직접 실행할 수 없으므로
    # 각 라우트를 별도의 Functions 파일로 분리해야 합니다
    pass
