FROM python:3.12-slim

ENV FLASK_CONTEXT=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV="/home/flaskapp/.venv"
ENV PATH="$VIRTUAL_ENV/bin:/home/flaskapp/.local/bin:$PATH"

RUN useradd --create-home --home-dir /home/flaskapp flaskapp
RUN apt-get update && \
    apt-get install -y build-essential curl \
    libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 \
    libffi-dev libcairo2 libpangoft2-1.0-0 libglib2.0-0 && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/flaskapp

USER flaskapp

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY --chown=flaskapp:flaskapp ./pyproject.toml ./uv.lock ./
RUN uv venv && uv sync --no-cache

COPY --chown=flaskapp:flaskapp ./app ./app
COPY --chown=flaskapp:flaskapp ./wsgi.py .

EXPOSE 5000
CMD ["granian", "--interface", "wsgi", "wsgi:app", "--port", "5000", "--host", "0.0.0.0", "--workers", "4", "--blocking-threads", "4"]
