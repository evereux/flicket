# ---------------------------------------------------------------------------
# Flicket developer Makefile
#
# Built to be cheap to re-run: the virtualenv is created once and `pip install`
# only runs again when a requirements file changes (stamp files live in
# tmp/.make/, which is gitignored via tmp/.gitignore). Run `make` or `make help`
# for the target list. Nothing here ever overwrites config.json or your database.
# ---------------------------------------------------------------------------

SHELL := /bin/bash
.DEFAULT_GOAL := help

PYTHON      ?= python3
VENV        ?= env
VENV_PY     := $(VENV)/bin/python
VENV_PIP    := $(VENV)/bin/pip
FLASK       := $(VENV)/bin/flask
SPHINX      := $(VENV)/bin/sphinx-build
PYBABEL     := $(VENV)/bin/pybabel
FLASKAPP    := FLASK_APP=application
PIPFLAGS    := --disable-pip-version-check -q

REQ         := requirements.txt
DEV_REQ     := requirements-development.txt
STAMP_DIR   := tmp/.make

HOST        ?= 127.0.0.1
PORT        ?= 5000
LOCALE      ?= de
MSG         ?= update
TEST_DIR    ?= tests
PYTEST      ?= $(VENV_PY) -m pytest
PYTEST_ARGS ?= -q

DOCKER       ?= docker
COMPOSE      ?= $(DOCKER) compose
COMPOSE_BASE := $(COMPOSE) -f compose.yaml
COMPOSE_DEV  := $(COMPOSE_BASE) -f compose.dev.yaml
COMPOSE_PROD := $(COMPOSE_BASE) -f compose.prod.yaml
BUILDKIT     := DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1

.PHONY: help bootstrap venv install install-dev check-deps config check-config \
        require-config db-upgrade db-current db-migrate setup run dev shell \
        check lint test smoke ci build docs docs-clean \
        i18n-compile i18n-extract i18n-update i18n-init \
        freeze clean distclean
.PHONY: require-stack docker-init docker-config docker-build docker-build-prod \
        docker-up docker-dev docker-prod docker-down docker-ps docker-logs \
        docker-restart docker-migrate docker-setup docker-shell docker-check \
        docker-test docker-ci docker-clean docker-reset

help:  ## Show this help (default target)
	@echo "Flicket - developer targets"
	@echo
	@grep -hE '^[a-zA-Z0-9_-]+:.*## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}' | sort
	@echo
	@echo "Configurable: VENV=$(VENV)  PYTHON=$(PYTHON)  HOST=$(HOST)  PORT=$(PORT)"
	@echo "              LOCALE=$(LOCALE)  MSG=$(MSG)  TEST_DIR=$(TEST_DIR)"
	@echo "Tip:      PYTHON=python3.11 make install   # use a different interpreter"
	@echo "Example: make run PORT=8080      make i18n-init LOCALE=es"
	@echo "          make docker-init && make docker-up && make docker-setup"

# --- environment (incremental) ---------------------------------------------

$(VENV_PY):
	@echo "==> creating virtualenv in $(VENV)/"
	$(PYTHON) -m venv $(VENV)

$(STAMP_DIR):
	@mkdir -p $(STAMP_DIR)

$(STAMP_DIR)/deps: $(REQ) | $(VENV_PY) $(STAMP_DIR)
	@echo "==> installing runtime requirements"
	$(VENV_PIP) install $(PIPFLAGS) -r $(REQ)
	@touch $@

$(STAMP_DIR)/dev-deps: $(DEV_REQ) $(STAMP_DIR)/deps | $(STAMP_DIR)
	@echo "==> installing development requirements"
	$(VENV_PIP) install $(PIPFLAGS) -r $(DEV_REQ)
	@touch $@

venv: $(VENV_PY)  ## Create the virtualenv (once)

install: $(STAMP_DIR)/deps  ## Install runtime deps (skipped unless requirements.txt changed)

install-dev: $(STAMP_DIR)/dev-deps  ## Install runtime + dev deps (pytest, Sphinx)

check-deps: install-dev  ## Verify installed packages are consistent (pip check)
	$(VENV_PIP) check

# --- configuration ----------------------------------------------------------

config: install  ## Interactively generate config.json (never overwrites an existing file)
	@if [ -f config.json ]; then \
		echo "==> config.json already exists - leaving it untouched"; \
	else \
		$(VENV_PY) -m scripts.create_json; \
	fi

require-config:
	@test -f config.json || { echo "config.json not found - run 'make config' first"; exit 1; }

check-config:  ## Validate config.json without starting the app
	@if [ ! -f config.json ]; then \
		echo "  SKIP: config.json not found (run 'make config')"; \
	else \
		$(PYTHON) -m json.tool config.json > /dev/null && \
		$(PYTHON) -c "import json;d=json.load(open('config.json'));r=('db_type','db_driver','db_username','db_password','db_url','db_port','db_name','SECRET_KEY','NOTIFICATION_USER_PASSWORD');m=[k for k in r if k not in d];assert not m and d.get('db_type') in (1,2,3),'invalid config.json: '+', '.join(m);print('  config.json OK (db_type=%s)' % d['db_type'])"; \
	fi

bootstrap: install-dev config check-config  ## One-shot dev setup: venv + deps + config.json
	@echo "==> next: make db-upgrade && make setup && make run"

# --- database / application -------------------------------------------------

db-upgrade: install require-config  ## Apply database migrations (flask db upgrade)
	$(FLASKAPP) $(FLASK) db upgrade

db-current: install require-config  ## Show the current migration revision
	$(FLASKAPP) $(FLASK) db current

db-migrate: install require-config  ## Create a migration: make db-migrate MSG="add column"
	$(FLASKAPP) $(FLASK) db migrate -m "$(MSG)"

setup: install require-config db-upgrade  ## Initialise defaults + admin user (interactive)
	$(FLASKAPP) $(FLASK) run-set-up

run: install require-config  ## Run the dev server (make run PORT=8080)
	$(FLASKAPP) $(FLASK) run --host=$(HOST) --port=$(PORT)

celery-worker: install require-config  ## Run a Celery worker for background tasks
	$(VENV_PY) -m celery -A application.celery_app:celery worker -l info

celery-beat: install require-config  ## Run the Celery beat scheduler (periodic tasks)
	$(VENV_PY) -m celery -A application.celery_app:celery beat -l info

dev: run  ## Alias for run

shell: install require-config  ## Open a Flask shell
	$(FLASKAPP) $(FLASK) shell

# --- checks / tests ---------------------------------------------------------

check: check-config  ## Fast syntax check of all Python sources
	$(PYTHON) -m compileall -q application scripts config.py
	@echo "==> syntax check passed"

lint: check  ## Alias for check

smoke: install  ## Import-check the full app (skipped when config.json is absent)
	@if [ ! -f config.json ]; then \
		echo "  SKIP smoke: no config.json (run 'make config' first)"; \
	else \
		$(VENV_PY) -c "import application; print('  import OK - Flicket %s, %d routes' % (application.__version__, len(list(application.app.url_map.iter_rules()))))"; \
	fi

test: install-dev check  ## Run pytest, or a smoke check when no tests/ dir exists
	@if [ -d "$(TEST_DIR)" ]; then \
		$(PYTEST) $(PYTEST_ARGS) $(TEST_DIR); \
	else \
		echo "==> no $(TEST_DIR)/ directory - running smoke check instead"; \
		$(MAKE) --no-print-directory smoke; \
	fi

ci: check test  ## Fast CI gate: syntax + tests
	@echo "==> CI checks passed"

build: install check  ## Fast incremental build: dependencies + syntax check
	@echo "==> build complete (run 'make i18n-compile' to refresh translations)"

# --- documentation / translations ------------------------------------------

docs: install-dev  ## Build Sphinx HTML docs into docs/_build/html
	$(SPHINX) -b html -q docs docs/_build/html
	@echo "==> docs: docs/_build/html/index.html"

docs-clean:  ## Remove built documentation
	rm -rf docs/_build

i18n-compile: install  ## Compile .po catalogues into .mo files
	$(PYBABEL) compile -d application/translations

i18n-extract: install  ## Rebuild messages.pot from the sources
	$(PYBABEL) extract -F babel.cfg -o messages.pot .

i18n-update: install  ## Merge messages.pot into the .po catalogues
	$(PYBABEL) update -i messages.pot -d application/translations

i18n-init: install  ## Add a new locale: make i18n-init LOCALE=es
	$(PYBABEL) init -i messages.pot -d application/translations -l $(LOCALE)

# --- housekeeping -----------------------------------------------------------

freeze: install-dev  ## Print the installed package versions
	$(VENV_PIP) freeze

clean:  ## Remove caches and build output (keeps venv, config.json and the DB)
	@find . -path './$(VENV)' -prune -o -type d -name '__pycache__' -print0 | xargs -0 -r rm -rf
	rm -rf .pytest_cache docs/_build test.db
	@echo "==> cleaned (env/, config.json and your database were kept)"

distclean: clean  ## Also remove the virtualenv and install stamps
	rm -rf $(VENV) $(STAMP_DIR)
	@echo "==> removed $(VENV)/ and install stamps (config.json kept)"

# --- docker / compose -------------------------------------------------------
# Fast rebuilds: BuildKit + a pip cache mount in the Dockerfile, and the
# requirements files are copied before the source so code edits never
# invalidate the dependency layer.

require-stack:
	@$(COMPOSE_BASE) ps --status running --services | grep -qx app || \
		{ echo "==> stack is not running - run 'make docker-up' first"; exit 1; }

docker-init:  ## Create .env from .env.example with random secrets (never overwrites)
	@if [ -f .env ]; then \
		echo "==> .env already exists - leaving it untouched"; \
	else \
		cp .env.example .env; \
		$(PYTHON) -c "import pathlib,re,secrets; p=pathlib.Path('.env'); p.write_text(re.sub('__GENERATED__', lambda m: secrets.token_hex(24), p.read_text()))"; \
		echo "==> wrote .env with random secrets - review it before deploying"; \
	fi

docker-config:  ## Validate/render all compose file combinations
	$(COMPOSE_DEV) config > /dev/null
	$(COMPOSE_PROD) config > /dev/null
	@echo "==> compose files OK"

docker-build:  ## Build the development image (BuildKit, cached layers)
	$(BUILDKIT) $(COMPOSE_DEV) build

docker-build-prod:  ## Build the production image (gunicorn, non-root)
	$(BUILDKIT) $(COMPOSE_PROD) build

docker-up: docker-init  ## Start the dev stack in the background
	$(BUILDKIT) $(COMPOSE_DEV) up -d --build

docker-dev: docker-up  ## Alias for docker-up, then follow the app logs
	$(COMPOSE_BASE) logs -f app

docker-prod: docker-init  ## Start the production stack (gunicorn, non-root)
	$(BUILDKIT) $(COMPOSE_PROD) up -d --build

docker-down:  ## Stop the stack (keeps volumes, database and uploads)
	$(COMPOSE_BASE) down --remove-orphans

docker-ps:  ## Show container status
	$(COMPOSE_BASE) ps

docker-logs:  ## Follow app + database logs
	$(COMPOSE_BASE) logs -f

docker-restart:  ## Restart the running stack
	$(COMPOSE_BASE) restart

docker-migrate: require-stack  ## Apply migrations in the running app container
	$(COMPOSE_BASE) exec app flask db upgrade

docker-setup: require-stack  ## Interactive first-run setup (admin user, site URL; needs a TTY)
	$(COMPOSE_BASE) exec app flask run-set-up

docker-shell: require-stack  ## Open a shell in the app container
	$(COMPOSE_BASE) exec app sh

docker-check: require-stack  ## Fast syntax check inside the container
	$(COMPOSE_BASE) exec app python -m compileall -q application scripts config.py
	@echo "==> syntax check passed (container)"

docker-test: require-stack  ## pytest (dev stack) or an import smoke test
	@if [ -d "$(TEST_DIR)" ]; then \
		$(COMPOSE_BASE) exec app python -m pytest $(PYTEST_ARGS) $(TEST_DIR); \
	else \
		echo "==> no $(TEST_DIR)/ - running smoke check in container"; \
		$(COMPOSE_BASE) exec app python -c "import application; print('  import OK - Flicket %s, %d routes' % (application.__version__, len(list(application.app.url_map.iter_rules()))))"; \
	fi

docker-ci: docker-check docker-test  ## CI gate in the container (run against the dev stack)
	@echo "==> docker CI checks passed"

docker-clean:  ## Remove containers and Flicket images (volumes/data are kept)
	$(COMPOSE_BASE) down --remove-orphans
	-$(DOCKER) image rm flicket:dev flicket:prod 2>/dev/null

docker-reset:  ## DESTRUCTIVE: stop the stack and delete the DB + uploads volumes
	@echo "==> WARNING: this deletes the MariaDB database and all uploaded files"
	$(COMPOSE_BASE) down -v --remove-orphans
