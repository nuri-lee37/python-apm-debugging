# 도커 앱 빌드
docker build -t local-ddtrace-app .

# 도커 에이전트 실행
docker run -d --name dd-agent \
  --network ddnet \
  -e DD_API_KEY=<YOUR API KEY> \
  -e DD_APM_ENABLED=true \
  -e DD_SITE=datadoghq.com \
  -e DD_HOSTNAME=local-dev \
  -p 8126:8126 \
  gcr.io/datadoghq/agent:latest

# 앱 실행
docker run -p 8080:8080 \
  --network ddnet \
  -e DD_AGENT_HOST=dd-agent \
  -e DD_SERVICE=my-service \
  -e DD_ENV=local \
  -e DD_LOGS_INJECTION=true \
  local-ddtrace-app
  
# 도커 에이전트 status 명령어  
docker exec -it dd-agent agent status

# 도커 에이전트 삭제
docker rm -f dd-agent 
