# Sandbox Manager (Node.js)

Full sandbox lifecycle management using the Node.js OpenAPI SDK.

## What It Does

- **Create** — `CreateSandbox` with configurable CPU, memory, and timeout
- **Describe** — `DescribeSandbox` to get sandbox status and resource info
- **List** — `ListSandboxes` to view all sandbox instances
- **Extend** — `SetSandboxTimeout` to extend the sandbox TTL
- **Destroy** — `KillSandbox` to release resources

```javascript
const createResp = await service.fetchOpenAPI({
    Action: "CreateSandbox", Version: "2024-06-06", method: "POST",
    data: { FunctionId: fid, CpuMilli: 500, MemoryMB: 1024, Timeout: 1800, TimeoutUnit: "second" },
});
const sandboxId = createResp.Result.SandboxId;

await service.fetchOpenAPI({ Action: "DescribeSandbox", data: { FunctionId: fid, SandboxId: sandboxId } });
await service.fetchOpenAPI({ Action: "SetSandboxTimeout", method: "POST", data: { FunctionId: fid, SandboxId: sandboxId, Timeout: 60 } });
await service.fetchOpenAPI({ Action: "KillSandbox", method: "POST", data: { FunctionId: fid, SandboxId: sandboxId } });
```

## Setup & Run

### 1. Install dependencies

```bash
npm install
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
npm start
```

## Reference

- [Sandbox API Documentation](https://www.volcengine.com/docs/6662/1806654)
