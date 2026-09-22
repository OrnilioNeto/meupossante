# AGENTS.md

Flask 3 + SQLAlchemy expense/earnings tracker for app drivers. UI, templates, flash messages, and domain terms are pt-BR.

## Layout

- Entrypoint `main.py` -> `create_app()` in `app/__init__.py` (config, extensions, OAuth wiring).
- All models in `app/models.py`; all routes in `app/main/routes.py` (single `main` blueprint, ~1650 lines); forms in `app/main/forms.py`.
- Templates in `app/templates/`, assets in `app/static/`.
- Alembic migrations in `migrations/`; SQLite DB at `instance/database.db` (gitignored).
- No tests, lint, formatter, or CI. Do not invent commands.

## Setup / run (Windows)

- Use the existing venv at `venv\` (not `.venv`; `aplicacao.md` is stale).
- `pip install -r requirements.txt` (deps unpinned).
- `flask db upgrade` before first run. `flask run` works via `.flaskenv` (`FLASK_APP=main.py`); `python main.py` serves on `0.0.0.0:8080` (`PORT` overrides).

## Config

Loaded by python-dotenv from `.env` (gitignored, not committed): `SECRET_KEY`, `DATABASE_URL`, `PORT`, `ADMIN_EMAILS` (comma-separated), `APP_DOMAIN` (base URL for the Google OAuth redirect), `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`.

- `app/__init__.py:40` deliberately ignores `DATABASE_URL` values starting with `sqlite:////home` and falls back to local SQLite (deploy artifact). Don't "fix" this blindly.

## Auth model

- Registration is invite-only (`/register/<token>`); admins generate links at `/admin/invites`.
- First run: when no users exist, `/login` renders a bootstrap form that creates the first admin.
- Google login (`/login/google` -> `/authorize`) still requires a valid invite for new emails.
- Admin check is `User.is_admin`: role `admin`, or email in `ADMIN_EMAILS` (falls back to user id 1 when unset). Guard admin views with `admin_required` (`app/main/routes.py:47`).

## Gotchas

- Consumption works without full tanks: `_segmentos_consumo()` (exact full-to-full) and `_trechos_abastecimento()` (km since previous fill ÷ liters added, for partial fills) feed `recalcular_medias()` (`app/main/routes.py:1199`/`:1248`), which persists `Abastecimento.media_consumo_calculada` and updates the active `Parametros.media_consumo`/`km_atual`. It commits and runs on every `/abastecimento` GET/POST. Autonomy = liters of the last fill × recent consumption, minus km logged since (ignores residual fuel); falls back to `Parametros.media_consumo` when no estimate exists. Dashboard KPIs/projections come from `_metricas_combustivel()` and are passed to `dashboard.html` as the `operacional` dict.
- The `/` desempenho form posts the car odometer (`kmAtual`), not km driven: `_ultimo_km_conhecido()` (`routes.py:1170`) derives `LancamentoDiario.km_rodado` from the latest reading (previous lancamento, abastecimento, or initial `Parametros.km_atual`). Dashboard extrato shows daily net = day revenue − estimated fuel (km_rodado ÷ recent consumption × recent price) − that day's `CustoVariavel` ("Custos Avulsos" tab), plus `liquido_mes_estimado`.
- `get_parametros_for_date` is defined twice (`routes.py:1138` and `:1153`); the second shadows the first (identical bodies).
- Monthly `RegistroCusto`/`RegistroReceita` rows are created, deduped, and re-priced inside the `dashboard` GET handler, not by migrations or a scheduler.
- `locale.setlocale` targets `pt_BR.UTF-8` with a `C.UTF-8` fallback (Windows may not have pt_BR); currency formatting goes through `format_currency` injected in `app/main/__init__.py`.
- Stray empty files tracked at repo root (`.tables`, `0bc723f851cd,`, `1f4c6312116d,`) are artifacts, not config.
