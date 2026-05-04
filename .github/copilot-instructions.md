# GitHub Copilot Instructions for Projeto de RH

## Purpose
This repository is a Django-based Human Resources web application. Use these instructions to guide Copilot toward productive changes without duplicating existing documentation.

## Project overview
- Django 6 web app using a single app: `core`
- Default database: SQLite (`db.sqlite3`)
- Optional database support via environment variables for PostgreSQL or MySQL
- UI built with Bootstrap 5 and `django-crispy-forms`
- Main features: funcionários, departamentos, férias, dashboard, admin metrics

## Key files and directories
- `manage.py` — Django CLI entrypoint
- `requirements.txt` — Python dependencies
- `docker-compose.yml` — PostgreSQL development service
- `rh_system/settings.py` — settings, database selection, static config
- `rh_system/urls.py` — root URL routes
- `core/` — domain app
  - `core/models.py` — `Departamento`, `Funcionario`, `Ferias`
  - `core/forms.py` — form validation and business rules
  - `core/views.py` — CRUD views and dashboard logic
  - `core/urls.py` — app URL patterns
  - `core/templates/core/` — HTML templates and layout
  - `core/admin.py` — Django admin customizations
- `TEMA_SISTEMA.md`, `BANCO_DE_DADOS.md`, `DIAGRAMA_BANCO.md`, `USO_E_EXEMPLOS.md` — project docs

## Recommended development workflow
Use the existing repository conventions and minimal setup.

### Local development
1. Create and activate a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the local server:
   ```bash
   python manage.py runserver
   ```

### Database options
- SQLite: default, works without extra configuration
- PostgreSQL: start with `docker-compose up -d`, then use the environment variable `DJANGO_USE_POSTGRES=1`
- MySQL: use `DJANGO_USE_MYSQL=1`

### Useful commands
- `python manage.py runserver`
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py shell`

## Conventions and best practices
- Keep Portuguese domain terms consistent: `funcionarios`, `departamentos`, `ferias`
- Prefer form-level validation in `core/forms.py` and model validation in `core/models.py`
- Use Bootstrap 5/Crispy forms markup in templates
- Keep front-end changes inside `core/templates/core/` and static files if needed
- Preserve existing dashboard and theme behavior unless the task explicitly changes UI/UX

## What to avoid
- Do not assume a separate frontend framework exists; this is server-rendered Django
- Do not add large new dependencies without necessity
- Avoid changing production settings for this task unless requested
- Do not duplicate documentation already present in markdown files

## When to ask for clarification
- If a feature touches both backend and templates, confirm the desired user flow
- If adding database migrations, confirm whether SQLite compatibility is required
- If a change affects the theme or layout, confirm whether both light/dark modes should be supported

## Example prompts
- "Add an email field to `Funcionario`, update the form, admin, and template views."
- "Fix CPF validation so the form rejects invalid CPF numbers and displays a clear error message."
- "Add an active employee count to the dashboard and show it in the card layout."
- "Enable optional PostgreSQL configuration in `rh_system/settings.py` using environment variables."

## Suggested next customization
- Create a backend-specific instruction file for Django tasks, focusing on models, views, forms, and migrations.
- Create a frontend instruction file for template and Bootstrap improvements.
- Create a `create-prompt` customization for `core/` domain requests to narrow suggestions to this app.
