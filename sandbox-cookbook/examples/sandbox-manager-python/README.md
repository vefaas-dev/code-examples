# Sandbox Manager (Python)

Full sandbox lifecycle management using the Python SDK.

## What It Does

- **Create** — `CreateSandbox` with configurable CPU, memory, and timeout
- **Describe** — `DescribeSandbox` to get sandbox status and resource info
- **List** — `ListSandboxes` to view all sandbox instances
- **Extend** — `SetSandboxTimeout` to extend the sandbox TTL
- **Destroy** — `KillSandbox` to release resources

```python
api = VEFAASApi(ApiClient(config))

sandbox_id = api.create_sandbox(CreateSandboxRequest(
    function_id=fid, cpu_milli=500, memory_mb=1024,
    timeout=1800, timeout_unit="second",
)).sandbox_id

info = api.describe_sandbox(DescribeSandboxRequest(function_id=fid, sandbox_id=sandbox_id))
api.set_sandbox_timeout(SetSandboxTimeoutRequest(function_id=fid, sandbox_id=sandbox_id, timeout=60))
api.kill_sandbox(KillSandboxRequest(function_id=fid, sandbox_id=sandbox_id))
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
