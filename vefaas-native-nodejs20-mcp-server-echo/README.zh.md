# Node.js MCP Server（veFaaS 模板 · Echo）

一个可直接部署到 veFaaS 的 Node.js 20 MCP Server 模板，内置最基础的 echo/hello 工具

## 功能
- 工具：
  - `hello(name: string)` → `Hello, ${name}!`
  - `echo(text: string)` → 原样返回 `text`
- 传输：Streamable HTTP（HTTP Transport）。

## 环境要求
- Node.js 20
- veFaaS（Linux/Debian）

## 环境变量（默认值）
- `MCP_SERVER_HOST=0.0.0.0`
- `MCP_SERVER_PORT=8000`
- `STREAMABLE_HTTP_PATH=/mcp`

## 本地使用
- 安装依赖：`npm install`
- HTTP（streamable-http）：`npm start`
  - 启动日志应类似：`Echo MCP Server (HTTP) listening at http://0.0.0.0:8000/mcp`

## 部署到 veFaaS
1) 本地准备（仅源代码 + package.json）
- `./zip.sh`（打包且排除 `node_modules/`）

2) 控制台操作
- 上传 zip 包
- 点击“安装依赖”（平台根据 `package.json` 安装 `dependencies`）
- 部署函数（平台通过 `run.sh` 启动 `node src/index.js`）
- 查看日志，确认启动成功（应看到 http 启动日志 `Echo MCP Server (HTTP) listening at http://...`，或回退至 stdio）

## 目录与脚本
- `src/index.js`：MCP Server 实现（echo/hello）
- `run.sh`：启动入口
- `zip.sh`：打包脚本（排除 `node_modules/`）

