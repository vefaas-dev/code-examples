# Python 3.8 TOS File Extraction Function Template

## Runtime Environment
- veFaaS (Linux/Debian, Python 3.8)

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
