# Introduction

This repository contains **veFaaS** runtime examples and best practices for various programming languages, covering function triggers, dependency management, event handling, HTTP services, and more.

- [Python Runtime Development Guide](https://www.volcengine.com/docs/6662/107429)
- [Native Python Runtime Development Guide](https://www.volcengine.com/docs/6662/1336107)
- [Node.js Runtime Development Guide](https://www.volcengine.com/docs/6662/116907)
- [Native Node.js Runtime Development Guide](https://www.volcengine.com/docs/6662/1528983)
- [Golang Runtime Development Guide](https://www.volcengine.com/docs/6662/106050)

> **Note:** **Native Runtimes** (e.g., `Native Python`, `Native Nodejs`) have different function entry points compared to **Standard Runtimes** (e.g., `Python 3.8`, `Nodejs 20`). Please choose the appropriate runtime based on your use case.

---

## veFaaS Quick Start Samples

| Sample Name | Runtime | Type | Third-party Services | Description |
| ----------- | ------- | ---- | -------------------- | ----------- |
| vefaas-python38-tos-auto-unzip | Python 3.8 | HTTP Trigger | TOS | Download, extract, and upload files from TOS |
| vefaas-python-tos-stream-unzip | Python 3.9 | Stream Processing | TOS | Stream download and extract files |
| vefaas-golang-tos-trigger | Golang | Event Trigger | TOS | Function responding to TOS upload events |
| vefaas-golang-sns-to-rmq | Golang | EventBridge Trigger | RocketMQ | Push SNS notification events to MQ |
| vefaas-native-microservice-kafka-to-es-exporter | Golang | Stream Processing | Kafka / Elasticsearch | Consume Kafka data and write to ES |
| vefaas-nodejs14-static-server | Nodejs 14 | HTTP Trigger | - | Static file server example |
| vefaas-native-nodejs20-nextjs-chatbot | Nodejs 20 | HTTP Trigger | OpenAI API | Next.js-based Chatbot example |
| vefaas-native-nodejs20-vitepress-default | Nodejs 20 | HTTP Trigger | - | VitePress documentation site example |
| vefaas-golang-default | Golang | HTTP Trigger | - | Hello World example |

---

## Runtime Categories

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

## Important Notes

1. These examples are for reference only. For production environments, please adjust configurations and dependencies according to your business requirements.
2. Native runtimes and standard runtimes have different startup methods. Please refer to the corresponding development documentation.
