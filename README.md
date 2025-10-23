# SWE30003 Django scaffold

This folder contains a minimal Django project and an `inventory` app wired to the existing `models` directory.

Quick start

1. Create and activate a virtualenv (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

3. API endpoints
- List/create products: GET/POST /api/products/
- Retrieve/update/delete product: GET/PUT/PATCH/DELETE /api/products/<id>/
- Inventories: /api/inventories/
