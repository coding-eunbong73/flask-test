# Python 3.10 기반의 경량 이미지 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY app.py .

# 컨테이너가 80번 포트를 리슨하도록 설정
EXPOSE 80

# 컨테이너 실행 명령어
# Gunicorn과 같은 프로덕션용 WSGI 서버를 사용하는 것이 일반적이지만,
# 이 예제에서는 간단하게 직접 Python 스크립트를 실행합니다.
CMD ["python", "app.py"]