# Hello World (Python)

Quick start with veFaaS Sandbox using the Python SDK. Demonstrates the complete flow: create sandbox, execute code, get result, destroy sandbox.

## What It Does

- Creates a sandbox instance via the veFaaS SDK
- Executes a Python `print()` statement in the sandbox
- Retrieves and displays `stdout` output
- Destroys the sandbox to release resources

```python
resp = await client.post(f"{endpoint}/v1/code/execute", json={
    "language": "python",
    "code": "print('Hello from veFaaS Sandbox!')",
})
print(resp.json()["data"]["stdout"])
```

## Setup & Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a Sandbox application

If you don't have one yet, [create a Code Sandbox application](https://console.volcengine.com/vefaas/region:vefaas+cn-beijing/sandbox/create?imageGroup=Code&quickStart=true) in the veFaaS console, and note the **Function ID** and **Endpoint**.

> 📖 See the full [Prerequisites](../../README.md#2-prerequisites) guide for details.

### 3. Configure environment

Copy `.env.template` to `.env` and fill in your credentials:

```bash
cp .env.template .env
```

- `VOLC_ACCESS_KEY` / `VOLC_SECRET_KEY` — [Volcengine AccessKey](https://console.volcengine.com/iam/keymanage/)
- `SANDBOX_APP_ID` — Function ID from the veFaaS console
- `SANDBOX_ENDPOINT` — Sandbox APIG endpoint URL

### 4. Run

```bash
python main.py
```

## Reference

- [Sandbox API Documentation](https://www.volcengine.com/docs/6662/1806654)
