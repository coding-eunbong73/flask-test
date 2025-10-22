import os
from flask import Flask
# Application Insights/OpenCensus 설정을 위한 모듈
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler
import logging # Python의 기본 로깅 모듈
# logging.StreamHandler를 사용하기 위해 logging 모듈에서 import합니다.
from logging import StreamHandler

app = Flask(__name__)

# ----------------- 로깅 설정 강화 -----------------

# 1. Flask 로거의 레벨을 DEBUG로 설정합니다.
app.logger.setLevel(logging.DEBUG)

# 2. Werkzeug 로거의 레벨도 DEBUG로 설정하여 HTTP 요청/응답 로그도 자세히 봅니다.
logging.getLogger('werkzeug').setLevel(logging.DEBUG)


# **중요**: Flask의 기본 핸들러(콘솔)를 가져와 레벨을 설정합니다.
# Azure Container App 환경에서는 이 기본 핸들러의 레벨이 자동으로 높아질 수 있습니다.
# 기존 핸들러를 제거하고 새 핸들러를 추가하거나, 기존 핸들러를 수정할 수 있습니다.

# A. 기존 핸들러가 있다면 레벨을 DEBUG로 설정
for handler in app.logger.handlers:
    handler.setLevel(logging.DEBUG)

# B. (선택 사항) 만약 핸들러가 없거나, 명시적으로 제어하고 싶다면 StreamHandler를 추가합니다.
if not app.logger.handlers:
    # 콘솔 출력을 담당하는 StreamHandler 생성
    console_handler = StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # 포맷터 설정 (선택 사항)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    console_handler.setFormatter(formatter)
    
    # Flask 로거에 핸들러 추가
    app.logger.addHandler(console_handler)

    
# Application Insights 연결 문자열 가져오기
# 이 환경 변수는 Container App 배포 시 설정할 것입니다.
CONNECTION_STRING = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")


# Application Insights 미들웨어 설정
# 연결 문자열이 있을 때만 추적을 활성화합니다.
if CONNECTION_STRING:
    middleware = FlaskMiddleware(
        app,
        exporter=AzureExporter(connection_string=CONNECTION_STRING),
        sampler=ProbabilitySampler(1.0) # 모든 요청을 추적 (100%)
    )

@app.route('/')
def hello():
    app.logger.info("Hello")
    return "Hello from Azure Container App with Application Insights!"

@app.route('/health')
def health_check():
    app.logger.info("health")
    
    # 헬스 체크 엔드포인트는 보통 추적 대상에서 제외할 수 있지만, 
    # 이 예제에서는 기본 설정으로 모든 요청을 추적합니다.
    return "OK"

@app.route('/bad')
def bad():
    app.logger.info("bad")

    return "bad"

@app.route('/baaa')
def baaa():
    app.logger.info("baaa")
 
    return "baaa"

if __name__ == '__main__':
    # Gunicorn 대신 Flask 개발 서버로 간단하게 실행
    app.run(host='0.0.0.0', port=80)