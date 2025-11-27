# Python 3.8 TOS MCDN Refresh Function Template

This repository provides a Python function template that can be directly deployed to veFaaS. Recommended workflow:
- Use venv for local development
- Let the veFaaS platform install dependencies based on `requirements.txt` during deployment

## Runtime Environment
- veFaaS (Linux/Debian, Python 3.8)

## Local Development (Based on venv)
- Execute in the project root directory:
  - `python -m venv .venv`
  - `source .venv/bin/activate`
  - `python -m pip install -U pip`
  - `pip install -r requirements.txt`
- Run:
  - `python index.py`

## Deploy to veFaaS (Platform Dependency Installation)
- Ensure `requirements.txt` contains all dependencies (if adding new ones, write them to this file, e.g., `requests==2.32.3`)
- Generate deployment package: `./zip.sh`
- Upload the deployment package to the veFaaS console
- Click "Install Dependencies" in the console. The platform will install the dependencies in the Linux Python 3.8 environment to the runtime directory
- Deploy the function and check the logs to confirm successful startup

## Key Files
- `index.py`: Function entry point
- `requirements.txt`: Dependencies file (maintain as needed)
- `zip.sh`: Packaging script (excludes `.venv/`, `site-packages/`, `.wheels/`)
