# Code Execution (Python)

Execute Python, Node.js, and Shell code in a sandbox using the Python SDK.

## What It Does

- **Python execution** — Run Python code via `/v1/code/execute` with `language: "python"`
- **Node.js execution** — Run JavaScript code with `language: "nodejs"`
- **Shell commands** — Execute shell commands via `/v1/shell/exec`

```python
# Python code execution
result = await client.post(f"{endpoint}/v1/code/execute", json={
    "language": "python",
    "code": "print(sum(range(100)))",
})

# Shell command execution
result = await client.post(f"{endpoint}/v1/shell/exec", json={
    "command": "uname -a",
    "timeout": 10,
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
