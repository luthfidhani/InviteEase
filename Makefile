# ---------------------------------------------------------------------------
# InviteEase – Makefile
# ---------------------------------------------------------------------------
# Ringkas perintah Docker Compose & Django rutin.
# ---------------------------------------------------------------------------

COMPOSE = docker compose
APP     = $(COMPOSE) exec app
PY      = $(APP) python manage.py

# ---------- Help -----------------------------------------------------------
.PHONY: help
help:
	@echo "🛠  Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ---------- Docker lifecycle ----------------------------------------------
build:            ## Build image
	$(COMPOSE) build

up:               ## Start services
	$(COMPOSE) up -d

down:             ## Stop & remove containers
	$(COMPOSE) down

restart:          ## Restart app container
	$(COMPOSE) restart app

logs:             ## Tail logs
	$(COMPOSE) logs -f --tail=100 app

# ---------- Django helpers -------------------------------------------------
shell:            ## Open Django shell
	$(PY) shell

makemigrations:   ## Create/update migration files
	$(PY) makemigrations

migrate:          ## Apply migrations
	$(PY) migrate

createsuperuser:  ## Create admin user
	$(PY) createsuperuser

collectstatic:    ## Collect static files
	$(PY) collectstatic --no-input

manage:           ## Run arbitrary manage.py command, e.g. make manage cmd="inviteease"
	$(PY) $(cmd)

# ---------- Testing --------------------------------------------------------
test:             ## Run Django tests
	$(PY) test

# ---------- Clean ----------------------------------------------------------
clean:            ## Remove compiled Python files & __pycache__
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Default target
.DEFAULT_GOAL := help
