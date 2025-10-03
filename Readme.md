# Qubono

A Backend for Web Application Development for Marketplace.

## Features

- [Feature 1]

## Prerequisites

- Python 3.11+
- pip
- virtualenv (recommended)
- PostgreSQL/MySQL/SQLite (depending on your database choice)

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/vijay-petu/qubono.git
cd qubono
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic
```

## Running the Application

**Development server:**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Configuration

Key settings in `.env`:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` in production
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## Project Structure

```
qubono/
```

## Deployment


## Contributing


## License


## Contact



## Acknowledgments