# ここはビルド用のコンテナ
FROM python:3.11-slim-buster as builder

WORKDIR /opt/app

RUN pip3 install poetry
COPY poetry.lock pyproject.toml poetry.toml ./
RUN poetry install --no-dev

# ここからは実行用コンテナの準備
FROM python:3.11-slim-buster as runner

ENV PYTHONPATH "${PYTHONPATH}:/opt/app/app"
RUN useradd -r -s /bin/false appuser
WORKDIR /opt/app
COPY --from=builder /opt/app/.venv /opt/app/.venv
COPY data ./data
COPY *.py ./
USER appuser
EXPOSE 8000
ENTRYPOINT ["/opt/app/.venv/bin/streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]
