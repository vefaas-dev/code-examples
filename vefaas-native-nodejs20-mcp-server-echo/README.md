# Node.js MCP Server (veFaaS Template · Echo)

A Node.js 20 MCP Server template that can be directly deployed to veFaaS, with built-in basic echo/hello tools.

## Features
- Tools:
  - `hello(name: string)` → `Hello, ${name}!`
  - `echo(text: string)` → Returns `text` as-is
- Transport: Streamable HTTP (HTTP Transport)

## Requirements
- Node.js 20
- veFaaS (Linux/Debian)

## Environment Variables (Defaults)
- `MCP_SERVER_HOST=0.0.0.0`
- `MCP_SERVER_PORT=8000`
- `STREAMABLE_HTTP_PATH=/mcp`

## Local Usage
- Install dependencies: `npm install`
- HTTP (streamable-http): `npm start`
  - Startup logs should show: `Echo MCP Server (HTTP) listening at http://0.0.0.0:8000/mcp`

## Deploy to veFaaS
1) Local preparation (source code + package.json only)
- `./zip.sh` (package and exclude `node_modules/`)

2) Console operations
- Upload zip package
- Click "Install Dependencies" (platform installs `dependencies` from `package.json`)
- Deploy function (platform starts via `run.sh` running `node src/index.js`)
- Check logs to confirm successful startup (should see HTTP startup log `Echo MCP Server (HTTP) listening at http://...`, or fallback to stdio)

## Directory and Scripts
- `src/index.js`: MCP Server implementation (echo/hello)
- `run.sh`: Startup entry point
- `zip.sh`: Packaging script (excludes `node_modules/`)
