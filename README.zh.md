# 简介

本仓库包含 **veFaaS** 各语言运行时（Runtime） 的示例与最佳实践，涵盖函数触发、依赖管理、事件处理、HTTP 服务等场景。

- [Python 运行时代码开发指南](https://www.volcengine.com/docs/6662/107429)
- [Native Python 运行时代码开发指南](https://www.volcengine.com/docs/6662/1336107)
- [Node.js 运行时代码开发指南](https://www.volcengine.com/docs/6662/116907)
- [Native Node.js 运行时代码开发指南](https://www.volcengine.com/docs/6662/1528983)
- [Golang 运行时代码开发指南](https://www.volcengine.com/docs/6662/106050)


> 注意：**Native 运行时**（如 `Native Python`、`Native Nodejs`） 与 **普通运行时**（如 `Python 3.8`、`Nodejs 20`）的函数启动入口所不同。请根据场景选择合适运行时。

---

## veFaaS 快速开始示例（Quick Start Samples）

| 示例名称 | 运行时 | 类型 | 第三方服务 | 说明 |
| -------- | ------- | ------- | ----------- | -------- |
| vefaas-python38-tos-auto-unzip | Python 3.8 | HTTP 触发器 | TOS | 从 TOS 下载压缩包、解压并上传文件示例 |
| vefaas-python-tos-stream-unzip | Python 3.9 | Stream 处理 | TOS | 流式下载并解压文件 |
| vefaas-golang-tos-trigger | Golang | Event 触发器 | TOS | 响应 TOS 上传事件的函数示例 |
| vefaas-golang-sns-to-rmq | Golang | EventBridge 触发器 | RocketMQ | SNS 通知事件推送至 MQ |
| vefaas-native-microservice-kafka-to-es-exporter | Golang | Stream 处理 | Kafka / Elasticsearch | 消费 Kafka 数据并写入 ES |
| vefaas-nodejs14-static-server | Nodejs 14 | HTTP 触发器 | - | 静态文件服务示例 |
| vefaas-native-nodejs20-nextjs-chatbot | Nodejs 20 | HTTP 触发器 | OpenAI API | 基于 Next.js 的 Chatbot 示例 |
| vefaas-native-nodejs20-vitepress-default | Nodejs 20 | HTTP 触发器 | - | VitePress 文档网站示例 |
| vefaas-golang-default | Golang | HTTP 触发器 | - | Hello World 示例 |

---

## 运行时分类

### Python
- **vefaas-native-python3.8-default**  
- **vefaas-native-python3.9-default**  
- **vefaas-native-python3.10-default**  
- **vefaas-native-python3.12-default**

### Node.js
- **vefaas-nodejs14-default**  
- **vefaas-nodejs20-default**  
- **vefaas-native-nodejs20-default**  
- **vefaas-native-nodejs20-nextjs**  
- **vefaas-native-nodejs20-react-default**  
- **vefaas-native-nodejs20-vitepress-default**  
- **vefaas-native-nodejs20-vue-default**

### Golang
- **vefaas-golang-default**  
- **vefaas-golang-tos-trigger**  
- **vefaas-golang-sns-to-rmq**
- **vefaas-native-microservice-kafka-to-es-exporter**

---

## 注意事项

1. 本示例仅供参考，生产环境请根据业务需求调整配置与依赖。
2. Native 运行时与普通运行时的启动方式不同，请参考对应开发文档。
