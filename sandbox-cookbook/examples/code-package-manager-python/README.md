# Package Management (Python)

List, install, and verify pip/npm packages in a sandbox.

## What It Does

- **List installed packages** — Query pre-installed Python packages via `/v1/sandbox/packages/python`
- **Install packages** — Install new packages with `pip install` via `/v1/shell/exec`
- **Verify installation** — Execute code that imports the newly installed package

```python
# List pre-installed Python packages
packages = await client.get(f"{endpoint}/v1/sandbox/packages/python")

# Install a new package
await client.post(f"{endpoint}/v1/shell/exec", json={
    "command": "pip install cowsay",
    "timeout": 120,
})

# Verify by running code that uses the package
result = await client.post(f"{endpoint}/v1/code/execute", json={
    "language": "python",
    "code": "import cowsay; cowsay.cow('Hello from sandbox!')",
})
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

```bash
cp .env.template .env
```

### 4. Run

```bash
python main.py
```

## Reference

- [Sandbox API Documentation](https://www.volcengine.com/docs/6662/1806654)
