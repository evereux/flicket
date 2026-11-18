# syntax=docker/dockerfile:1.7
# ---------------------------------------------------------------------------
# Flicket container image.
#
#   docker build --target development -t flicket:dev .
#   docker build --target production  -t flicket:prod .
#
# The virtualenv lives in /opt/venv (outside /app) so the development bind
# mount of the source tree cannot hide the installed packages. Requirements
# are copied before the source so `pip install` is cached across code edits.
# ---------------------------------------------------------------------------

ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    FLASK_APP=application \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000 \
    AVATAR_DEFAULTS_DIR=/opt/flicket/defaults/avatars

WORKDIR /app

RUN python -m venv /opt/venv \
 && groupadd --system --gid 10001 app \
 && useradd --system --uid 10001 --gid app --home-dir /app app

# --- dependencies first (BuildKit cache mount makes rebuilds cheap) ---------
COPY requirements.txt requirements-development.txt requirements-production.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install -r requirements.txt

# --- application source -----------------------------------------------------
COPY . .
RUN install -m 0755 /app/docker/entrypoint.sh /usr/local/bin/flicket-entrypoint \
 && mkdir -p /opt/flicket/defaults/avatars \
 && cp -a /app/application/flicket/static/flicket_avatars/. /opt/flicket/defaults/avatars/

EXPOSE 5000
ENTRYPOINT ["/usr/local/bin/flicket-entrypoint"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# ---------------------------------------------------------------------------
# Development: Flask dev server with reload, dev deps (pytest, Sphinx).
# Runs as root so the source bind mount in compose.dev.yaml stays writable.
# ---------------------------------------------------------------------------
FROM base AS development

RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install -r requirements-development.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]

# ---------------------------------------------------------------------------
# Production: gunicorn, non-root, no debug .flaskenv.
# ---------------------------------------------------------------------------
FROM base AS production

RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install -r requirements-production.txt \
 && rm -f /app/.flaskenv \
 && chown -R app:app /app /opt/flicket

USER app

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/', timeout=3)" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", \
     "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", \
     "application:app"]
