#!/bin/sh
# ---------------------------------------------------------------------------
# Flicket container entrypoint.
#
# config.py reads ./config.json at import time and connects to the database
# during import, so before starting the real command we:
#   1. generate config.json from environment variables (never overwriting an
#      existing / mounted config.json),
#   2. make sure upload directories and default avatars exist,
#   3. wait for the database to accept TCP connections,
#   4. apply Alembic migrations.
# ---------------------------------------------------------------------------
set -eu

APP_DIR=/app
CONFIG_FILE="$APP_DIR/config.json"
UPLOADS_DIR="$APP_DIR/application/flicket/static/flicket_uploads"
AVATARS_DIR="$APP_DIR/application/flicket/static/flicket_avatars"

DB_TYPE=${DB_TYPE:-3}
DB_DRIVER=${DB_DRIVER:-pymysql}
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-3306}
DB_NAME=${DB_NAME:-flicket}
DB_USER=${DB_USER:-flicket}
DB_PASSWORD=${DB_PASSWORD:-flicket}
SECRET_KEY=${SECRET_KEY:-}
NOTIFICATION_USER_PASSWORD=${NOTIFICATION_USER_PASSWORD:-}
ZITADEL_ENABLED=${ZITADEL_ENABLED:-false}
ZITADEL_ISSUER=${ZITADEL_ISSUER:-https://id.exam-studio.com}
ZITADEL_CLIENT_ID=${ZITADEL_CLIENT_ID:-}
ZITADEL_CLIENT_SECRET=${ZITADEL_CLIENT_SECRET:-}
SKIP_DB_UPGRADE=${SKIP_DB_UPGRADE:-0}
SKIP_DB_WAIT=${SKIP_DB_WAIT:-0}

export DB_TYPE DB_DRIVER DB_HOST DB_PORT DB_NAME DB_USER DB_PASSWORD \
       SECRET_KEY NOTIFICATION_USER_PASSWORD ZITADEL_ENABLED ZITADEL_ISSUER \
       ZITADEL_CLIENT_ID ZITADEL_CLIENT_SECRET \
       CELERY_BROKER_URL CELERY_RESULT_BACKEND CELERY_TIMEZONE

random_secret() {
    python -c 'import base64, os; print(base64.urlsafe_b64encode(os.urandom(24)).decode().rstrip("="))'
}

if [ -f "$CONFIG_FILE" ]; then
    echo "==> using existing $CONFIG_FILE"
else
    if [ -z "$SECRET_KEY" ]; then
        SECRET_KEY=$(random_secret)
        export SECRET_KEY
        echo "==> WARNING: SECRET_KEY is empty - generated a temporary value." >&2
        echo "    Set SECRET_KEY in .env so sessions survive restarts." >&2
    fi
    if [ -z "$NOTIFICATION_USER_PASSWORD" ]; then
        NOTIFICATION_USER_PASSWORD=$(random_secret)
        export NOTIFICATION_USER_PASSWORD
    fi

    python - "$CONFIG_FILE" <<'PY'
import json
import os
import sys


def text(name, default=""):
    return os.environ.get(name) or default


def optional(name, default=None):
    return os.environ.get(name) or default


def enabled(value):
    return str(value).strip().lower() in ("1", "true", "yes", "on")


db_type = int(os.environ.get("DB_TYPE", "3"))

config = {
    "db_type": db_type,
    # config.py only uses db_driver for MySQL / PostgreSQL.
    "db_driver": text("DB_DRIVER") if db_type != 1 else None,
    "db_username": text("DB_USER"),
    "db_password": text("DB_PASSWORD"),
    "db_url": text("DB_HOST", "db"),
    "db_port": text("DB_PORT", "3306"),
    "db_name": text("DB_NAME", "flicket"),
    "SECRET_KEY": os.environ["SECRET_KEY"],
    "NOTIFICATION_USER_PASSWORD": os.environ["NOTIFICATION_USER_PASSWORD"],
    "ZITADEL_ENABLED": enabled(os.environ.get("ZITADEL_ENABLED", "false")),
    "ZITADEL_ISSUER": optional("ZITADEL_ISSUER", "https://id.exam-studio.com"),
    "ZITADEL_CLIENT_ID": optional("ZITADEL_CLIENT_ID"),
    "ZITADEL_CLIENT_SECRET": optional("ZITADEL_CLIENT_SECRET"),
    "CELERY_BROKER_URL": optional("CELERY_BROKER_URL", "redis://redis:6379/0"),
    "CELERY_RESULT_BACKEND": optional("CELERY_RESULT_BACKEND", "redis://redis:6379/1"),
    "CELERY_TIMEZONE": optional("CELERY_TIMEZONE", "UTC"),
}

with open(sys.argv[1], "w") as handle:
    json.dump(config, handle, indent=2)
    handle.write("\n")
PY
    echo "==> wrote $CONFIG_FILE from environment"
fi

mkdir -p "$UPLOADS_DIR" "$AVATARS_DIR" 2>/dev/null || true

# A named volume mounted over the avatars directory hides the image's files;
# restore the defaults from the copy kept outside /app.
if [ -n "${AVATAR_DEFAULTS_DIR:-}" ] && [ -d "$AVATAR_DEFAULTS_DIR" ]; then
    for src in "$AVATAR_DEFAULTS_DIR"/*; do
        [ -f "$src" ] || continue
        dst="$AVATARS_DIR/$(basename "$src")"
        if [ ! -e "$dst" ]; then
            cp "$src" "$dst" || echo "==> WARNING: could not restore $(basename "$src")" >&2
        fi
    done
fi

# config.py connects to the DB at import time, so wait before ANY flask
# command (including `flask db upgrade`).
if [ "$DB_TYPE" != "1" ] && [ "$SKIP_DB_WAIT" != "1" ]; then
    python - <<'PY'
import os
import socket
import sys
import time

host = os.environ["DB_HOST"]
port = int(os.environ.get("DB_PORT") or 3306)
deadline = time.monotonic() + 90
while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            print("==> database %s:%s is reachable" % (host, port))
            break
    except OSError:
        if time.monotonic() >= deadline:
            sys.exit("!! database %s:%s did not become reachable in 90s" % (host, port))
        time.sleep(1)
PY
fi

if [ "$SKIP_DB_UPGRADE" != "1" ]; then
    echo "==> applying database migrations"
    flask db upgrade
fi

echo "==> starting: $*"
exec "$@"
