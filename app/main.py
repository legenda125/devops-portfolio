"""Минимальный сервис для демонстрации контейнеризации и мониторинга.

/        - ответ сервиса
/healthz - проверка живости (для Docker HEALTHCHECK и Kubernetes probes)
/metrics - метрики в формате Prometheus
"""
from http.server import BaseHTTPRequestHandler, HTTPServer

from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

REQUESTS = Counter("demo_http_requests_total", "Число HTTP-запросов", ["path"])


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/plain; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/metrics":
            self._send(200, generate_latest(), CONTENT_TYPE_LATEST)
            return
        REQUESTS.labels(path=path).inc()
        if path == "/healthz":
            self._send(200, b"ok")
        elif path == "/":
            self._send(200, b"demo service is running\n")
        else:
            self._send(404, b"not found")

    def log_message(self, fmt, *args):
        pass  # не засорять логи контейнера


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
