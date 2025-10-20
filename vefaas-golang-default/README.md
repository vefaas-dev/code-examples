# Golang 函数模板

本仓库提供可直接部署到 veFaaS 的 Golang 函数模板。

## 运行环境
- veFaaS（Linux/Debian，Golang 环境）
- 平台运行 main 二进制（如何生成适用于 Linux 系统的可执行文件，请参考 build.sh）

## 部署到 veFaaS
- 生成部署包：执行 `./build_and_zip.sh`
- 上传部署包到 veFaaS 控制台
- 部署函数，查看日志确认启动成功