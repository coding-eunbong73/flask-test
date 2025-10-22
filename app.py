import os
from flask import Flask
# Application Insights/OpenCensus 설정을 위한 모듈
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler

app = Flask(__name__)

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
    print("Hello")
    return "Hello from Azure Container App with Application Insights!"

@app.route('/health')
def health_check():
    print("health")
    # 헬스 체크 엔드포인트는 보통 추적 대상에서 제외할 수 있지만, 
    # 이 예제에서는 기본 설정으로 모든 요청을 추적합니다.
    return "OK"

@app.route('/bad')
def bad():
    print("bad")
    # 헬스 체크 엔드포인트는 보통 추적 대상에서 제외할 수 있지만, 
    # 이 예제에서는 기본 설정으로 모든 요청을 추적합니다.
    return "bad"

if __name__ == '__main__':
    # Gunicorn 대신 Flask 개발 서버로 간단하게 실행
    app.run(host='0.0.0.0', port=80)