This vefaas function consumes ark sns events and send them to a rocketmq topic.

Required environment variables:
- AK (rocketmq AccessKey ID)
- SK (rocketmq AccessKey Secret)
- ACCESS_POINT (rocketmq cluster access endpoint, e.g. http://rocketmq-xxxxx.rocketmq.ivolces.com:9876)
- TOPIC (rocketmq topic name to write to)

# 中文翻译
这个 vefaas 函数会消费 ark 的 SNS 事件，并将其发送到 RocketMQ topic。

所需的环境变量：
- AK (rocketmq AccessKey ID)
- SK（rocketmq AccessKey Secret）
- ACCESS_POINT（rocketmq 集群 TCP 接入点，例如 http://rocketmq-xxxxx.rocketmq.ivolces.com:9876 ）
- TOPIC（要写入的 rocketmq 主题名称）