FROM python:3.14-slim

ENV FLASK_CONTEXT=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/flaskapp/.local/bin:/home/flaskapp/.venv/bin

RUN useradd --create-home --home-dir /home/flaskapp flaskapp
RUN apt-get update && \
    apt-get install -y build-essential curl && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/flaskapp

USER flaskapp

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY --chown=flaskapp:flaskapp ./pyproject.toml ./uv.lock ./
RUN uv sync --locked

COPY --chown=flaskapp:flaskapp ./app ./app
COPY --chown=flaskapp:flaskapp ./wsgi.py .

ENV VIRTUAL_ENV="/home/flaskapp/.venv"

EXPOSE 5000
CMD ["granian", "--interface", "wsgi", "wsgi:app", "--port", "5000", "--host", "0.0.0.0", "--workers", "4", "--blocking-threads", "4"]
