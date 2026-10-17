devops-portfolio
Небольшой учебный проект: контейнеризация сервиса, мониторинг и деплой в Kubernetes через Helm.
Состав

app/ — HTTP-сервис на Python (/, /healthz, /metrics) и multi-stage Dockerfile (запуск не от root, HEALTHCHECK).
docker-compose.yml — сервис + Prometheus + Grafana с готовым datasource.
monitoring/ — конфиг Prometheus и правило алерта DemoAppDown с указанием действия.
helm/demo-app/ — Helm-чарт: Deployment (2 реплики, readiness/liveness probes, resources), Service.
- `.gitlab-ci.yml` — пайплайн GitLab CI: lint (py_compile, yamllint, hadolint) → сборка образа и smoke-тест `/healthz`. Проект в GitLab: <https://gitlab.com/legenda125/devops-portfolio>

Запуск локально
docker compose up --build
# сервис:      http://localhost:8000
# метрики:     http://localhost:8000/metrics
# Prometheus:  http://localhost:9090
# Grafana:     http://localhost:3000 (admin / admin при первом входе)
Деплой в Kubernetes
docker build -t demo-app:1.0.0 ./app
helm lint helm/demo-app
helm template demo helm/demo-app        # посмотреть итоговые манифесты
helm install demo helm/demo-app
Что планирую добавить

- В пайплайн GitLab CI: `helm lint`, публикация образа в registry, деплой.
Ingress и ConfigMap/Secret в чарте.
Alertmanager и дашборд в Grafana.

