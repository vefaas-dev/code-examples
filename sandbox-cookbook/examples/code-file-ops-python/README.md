# File Operations (Python)

Read, write, append, list directories, and download files in a sandbox.

## What It Does

- **Write file** — Create files via `/v1/file/write`
- **Append** — Append content to existing files
- **Read file** — Read file contents via `/v1/file/read`
- **List directory** — List files and directories via `/v1/file/list`
- **Download** — Download files as base64 via `/v1/file/download`

```python
# Write a file
await client.post(f"{endpoint}/v1/file/write", json={
    "file": "/home/tiger/hello.txt",
    "content": "Hello World!",
})

# Read it back
result = await client.post(f"{endpoint}/v1/file/read", json={
    "file": "/home/tiger/hello.txt",
})

# List directory
result = await client.post(f"{endpoint}/v1/file/list", json={
    "path": "/home/tiger",
    "recursive": False,
    "max_depth": 2,
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
