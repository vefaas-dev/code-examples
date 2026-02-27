# Hello World (Node.js)

Quick start with veFaaS Sandbox using the Node.js HTTP API. Demonstrates the complete flow: create sandbox, execute code, get result, destroy sandbox.

## What It Does

- Creates a sandbox instance via the `@volcengine/openapi` SDK
- Executes a Python `print()` statement in the sandbox
- Retrieves and displays `stdout` output
- Destroys the sandbox to release resources

```javascript
const resp = await fetch(`${endpoint}/v1/code/execute`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-faas-instance-name": sandboxId },
    body: JSON.stringify({ language: "python", code: "print('Hello!')" }),
});
console.log((await resp.json()).data.stdout);
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

Copy `.env.template` to `.env` and fill in your credentials:

```bash
cp .env.template .env
```

### 4. Run

```bash
npm start
```

## Reference

- [Sandbox API Documentation](https://www.volcengine.com/docs/6662/1806654)
