# Native Python 3.10 函数模板

本仓库提供可直接部署到 veFaaS 的 Native Python 3.10 模板。推荐流程：
- 本地开发用 venv
- 部署时由 veFaaS 平台基于 `requirements.txt` 安装依赖

## 运行环境
- veFaaS（Linux/Debian，Python 3.10）
- 服务监听 `0.0.0.0:8000`
- 平台通过 `run.sh` 启动

## 本地开发（基于 venv）
- 在项目根目录执行：
  - `python -m venv .venv`
  - `source .venv/bin/activate`
  - `python -m pip install -U pip`
  - `pip install -r requirements.txt`
- 运行：
  - `python main.py` 或 `./run.sh`

## 部署到 veFaaS（平台安装依赖）
- 确认 `requirements.txt` 已包含完整依赖（包含可能的原生扩展包，如 `fastapi`、`uvicorn` 等）
- 生成部署包：`./zip.sh`
- 上传部署包到 veFaaS 控制台
- 在控制台点击“安装依赖”，平台会在 Linux Python 3.10 环境中将依赖安装到运行目录
- 部署函数，查看日志确认启动成功

## 关键文件
- `run.sh`：启动入口（会在本地自动激活 `.venv`）
- `zip.sh`：打包脚本（排除 `.venv/`、`site-packages/`、`.wheels/`）
