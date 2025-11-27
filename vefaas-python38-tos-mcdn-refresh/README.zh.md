# Python 3.8 TOS MCDN 刷新 函数模板

本仓库提供可直接部署到 veFaaS 的 Python 函数模板。推荐流程：
- 本地开发用 venv
- 部署时由 veFaaS 平台基于 `requirements.txt` 安装依赖

## 运行环境
- veFaaS（Linux/Debian，Python 3.8）

## 本地开发（基于 venv）
- 在项目根目录执行：
  - `python -m venv .venv`
  - `source .venv/bin/activate`
  - `python -m pip install -U pip`
  - `pip install -r requirements.txt`
- 运行：
  - `python index.py`

## 部署到 veFaaS（平台安装依赖）
- 确认 `requirements.txt` 已包含完整依赖（如有新增，请写入该文件，例如 `requests==2.32.3`）
- 生成部署包：`./zip.sh`
- 上传部署包到 veFaaS 控制台
- 在控制台点击“安装依赖”，平台会在 Linux Python 3.8 环境中将依赖安装到运行目录
- 部署函数，查看日志确认启动成功

## 关键文件
- `index.py`：函数入口
- `requirements.txt`：依赖文件（请根据需要维护）
- `zip.sh`：打包脚本（排除 `.venv/`、`site-packages/`、`.wheels/`）
