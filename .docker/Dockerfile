
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ADD . /app
WORKDIR /app

RUN uv sync --frozen

CMD ["uv", "run", "main.py"]