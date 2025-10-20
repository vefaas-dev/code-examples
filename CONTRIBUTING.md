# 贡献指南

本仓库包含多个语言（Python / Node.js / Go 等）的函数开发模板，用于帮助开发者快速在 [veFaaS 平台](https://www.volcengine.com/product/vefaas) 上构建、部署和调试函数。

本文档说明如何贡献一个新的函数模板，或改进现有模板。

## 目录
1. [贡献流程概览](#贡献流程概览)
2. [命名与规范](#命名与规范)
3. [提交与审核流程](#提交与审核流程)
4. [许可证](#许可证)

## 贡献流程概览

1. Fork 本仓库。
2. 在 `main` 分支上创建你的功能分支：
   ```bash
   git checkout -b feature/add-my-template
   ```
3.	在相应语言目录（如 vefaas-native-python3.13-default）下新增一个子目录。
4.	按照本文档[规范](#命名与规范)编写模板代码与 README.md。
5.	在本地完成功能验证后，请不要直接打包提交 PR。需在与 veFaaS 平台一致的 Linux 环境 下重新构建，确保构建产物可在平台上正常部署和运行。参考 [vefaas-golang-default](./vefaas-golang-default/build.sh) 的构建脚本。
6.  压缩代码包，命名为 `vefaas-<language>-<template-name>.zip` 并放到 zip 目录下。参考 [vefaas-golang-default](./vefaas-golang-default/build_and_zip.sh) 的构建并压缩脚本。
7.	提交 Pull Request，并在描述中说明模板语言、功能和使用场景。

## 命名与规范
1. 模板目录名统一为：
vefaas-<language>-<template-name>
例如：vefaas-python3.13-tos-auto-unzip
2. README.md 中需包含以下信息：
    1. 模板功能介绍
    1. 运行方式（本地与平台）
    1. 构建指令（如 `./build_and_zip.sh`）
    1. 本地测试指令（如 `./run.sh`）
3. 代码遵循语言官方推荐规范：
    1. Go → [Effective Go](https://go.dev/doc/effective_go)
    1. Python → [PEP 8](https://www.python.org/dev/peps/pep-0008/)
    1. Node.js → [Airbnb JS Style Guide](https://github.com/airbnb/javascript)

## 提交与审核流程
1.	提交 PR 前，请确保：
    1. 模板代码已通过基本测试；
    1. 打包构建需在与 veFaaS 平台一致的 Linux 环境下完成，确保产物可正常部署运行。
    1. README 说明完整；
    1. 不包含公司内部域名、凭证或敏感信息；
    1. LICENSE 文件明确。
2.	提交 Pull Request：
    1. 标题格式建议：feat(template): add python38-tos-auto-unzip
    1. 在描述中说明模板功能与适用场景。
3.	代码合并前将由维护者进行：
    1. 技术功能验证；
    1. 安全合规检查；
    1. 许可证扫描。

## 许可证

请参阅 [LICENSE](./LICENSE) 文件了解本项目的许可信息。我们将在您提交贡献时，请您确认所提交内容的许可情况。