# Python 3.8 Function Template

## Runtime Environment
- veFaaS (Linux/Debian, Python 3.8)

## Deploy to veFaaS (Platform Dependency Installation)
- If you need additional third-party dependencies, add them to `requirements.txt`, for example:
  ```txt
  requests==2.32.0
  numpy>=1.26
  ```
- Generate deployment package: `./zip.sh`
- Upload the deployment package to the veFaaS console
- If `requirements.txt` contains dependencies, click "Install Dependencies" in the console. The platform will install the dependencies in the Linux Python 3.8 environment to the runtime directory
- Deploy the function and check the logs to confirm successful startup

## Key Files
- `index.py`: Function entry point
- `requirements.txt`: Dependencies file (maintain as needed)
- `zip.sh`: Packaging script (excludes `.venv/`, `site-packages/`, `.wheels/`)
