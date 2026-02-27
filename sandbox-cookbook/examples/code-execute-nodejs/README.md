# Code Execution (Node.js)

Execute Python, Node.js, and Shell code in a sandbox using the Node.js HTTP API.

## What It Does

- **Python execution** — Run Python code via `/v1/code/execute` with `language: "python"`
- **Node.js execution** — Run JavaScript code with `language: "nodejs"`
- **Shell commands** — Execute shell commands via `/v1/shell/exec`

```javascript
const resp = await fetch(`${endpoint}/v1/code/execute`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-faas-instance-name": sandboxId },
    body: JSON.stringify({ language: "python", code: "print(sum(range(100)))" }),
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

```bash
cp .env.template .env
```

### 4. Run

```bash
npm start
```

## Reference

- [Sandbox API Documentation](https://www.volcengine.com/docs/6662/1806654)
