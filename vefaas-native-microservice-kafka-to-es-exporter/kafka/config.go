// Copyright (c) 2024 Bytedance Ltd. and/or its affiliates
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package kafka

import (
	"fmt"
)

// KafkaConf Kafka配置定义
type Conf struct {
	// 客户端启动时，初始链接的服务端地址
	BootstrapServers string `json:"bootstrap.servers"`
	// 访问服务端使用的安全协议，当前只支持 PLAINTEXT, SASL_PLAINTEXT 或 SASL_SSL，根据访问地址选择，默认为 SASL_PLAINTEXT
	Protocol string `json:"security.protocol"`
	// 开启DEBUG模式
	Debug bool `json:"debug"`
	// 执行消费的Topic名称，使用","分隔
	Topics string `json:"topics"`
	// 消费组
	ConsumerGroupId string `json:"consumer.group.id"`
	// Sasl 认证相关配置
	Sasl struct {
		Enabled bool `json:"enabled"`
		// 认证算法，当前只支持 PLAIN 或 SCRAM-SHA-256，根据用户类型选择
		Mechanism string `json:"mechanism"`
		// 认证用户名
		UserName string `json:"username"`
		// 认证密码
		Password string `json:"password"`
	} `json:"sasl"`
}

func NewKafkaConf() *Conf {
	conf := &Conf{}
	conf.Sasl.Enabled = false
	conf.Protocol = "SASL_PLAINTEXT"
	conf.Debug = false
	return conf
}

func (c *Conf) Validate() error {
	if !c.Sasl.Enabled {
		return nil
	}

	if c.Sasl.Mechanism != "PLAIN" && c.Sasl.Mechanism != "SCRAM-SHA-256" {
		return fmt.Errorf("unsupported mechanism(%s). only PLAIN or SCRAM-SHA-256 is supported currently", c.Sasl.Mechanism)
	}

	return nil
}
