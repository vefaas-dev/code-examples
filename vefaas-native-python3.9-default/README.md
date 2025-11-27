# Native Python 3.9 Function Template

This repository provides a Native Python 3.9 template that can be directly deployed to veFaaS. Recommended workflow:
- Use venv for local development
- Let the veFaaS platform install dependencies based on `requirements.txt` during deployment

## Runtime Environment
- veFaaS (Linux/Debian, Python 3.9)
- Service listens on `0.0.0.0:8000`
- Platform starts via `run.sh`

## Local Development (Based on venv)
- Execute in the project root directory:
  - `python -m venv .venv`
  - `source .venv/bin/activate`
  - `python -m pip install -U pip`
  - `pip install -r requirements.txt`
- Run:
  - `python main.py` or `./run.sh`

## Deploy to veFaaS (Platform Dependency Installation)
- Ensure `requirements.txt` contains all dependencies (including possible native extension packages like `fastapi`, `uvicorn`, etc.)
- Generate deployment package: `./zip.sh`
- Upload the deployment package to the veFaaS console
- Click "Install Dependencies" in the console. The platform will install the dependencies in the Linux Python 3.9 environment to the runtime directory
- Deploy the function and check the logs to confirm successful startup

## Key Files
- `run.sh`: Startup entry point (automatically activates `.venv` locally)
- `zip.sh`: Packaging script (excludes `.venv/`, `site-packages/`, `.wheels/`)
