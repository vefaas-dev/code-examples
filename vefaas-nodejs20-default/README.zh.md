# Node.js 20 函数模板

本仓库提供可直接部署到 veFaaS 的 Node.js 函数模板。

## 运行环境
- veFaaS（Linux/Debian，Node.js 20 环境）
- 通过`exports.handler(event, context)` 暴露 handler 作为平台的调用入口

## 部署到 veFaaS（平台安装依赖）
- 确认 `package.json` 已包含所需的依赖
- 生成部署包：执行 `./zip.sh`
- 上传部署包到 veFaaS 控制台
- 在控制台，如果使用了依赖，点击“安装依赖”，平台会在 Node.js 20 环境中将依赖安装到运行目录
- 部署函数，查看日志确认启动成功