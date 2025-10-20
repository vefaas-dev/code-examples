# Golang TOS trigger 函数模板

本仓库提供可直接部署到 veFaaS 的 Golang TOS trigger 函数模板。

## 运行环境
- veFaaS（Linux/Debian，Golang 环境）
- 平台调用函数入口 `handler`

## 部署到 veFaaS
- 生成部署包：执行 `./build_and_zip.sh`
- 上传部署包到 veFaaS 控制台
- 部署函数，查看日志确认启动成功