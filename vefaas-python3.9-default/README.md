# Python 3.9 函数模板

## 运行环境
- veFaaS（Linux/Debian，Python 3.9）

## 部署到 veFaaS（平台安装依赖）
- 如果你需要额外的第三方依赖，请在 `requirements.txt` 中添加，例如：
  ```txt
  requests==2.32.0
  numpy>=1.26
- 生成部署包：`./zip.sh`
- 上传部署包到 veFaaS 控制台
- 如果 `requirements.txt` 包含了依赖，在控制台点击“安装依赖”，平台会在 Linux Python 3.9 环境中将依赖安装到运行目录
- 部署函数，查看日志确认启动成功

## 关键文件
- `index.py`：函数入口
- `requirements.txt`：依赖文件（请根据需要维护）
- `zip.sh`：打包脚本（排除 `.venv/`、`site-packages/`、`.wheels/`）
