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
	"context"
	"fmt"
	"runtime/debug"

	"strings"

	"github.com/confluentinc/confluent-kafka-go/kafka"
)

var consumer *kafka.Consumer

func StartConsumer(ctx context.Context, config *Conf, handleMsgFunc func(message *kafka.Message)) {
	fmt.Printf("kafka config:%+v\n", *config)
	configMap := &kafka.ConfigMap{
		"bootstrap.servers":        config.BootstrapServers,
		"security.protocol":        config.Protocol,
		"group.id":                 config.ConsumerGroupId,
		"go.events.channel.enable": true,
	}

	if config.Debug {
		// Enable debug
		configMap.SetKey("debug", "ALL")
	}

	if config.Sasl.Enabled {
		// Set SASL configurations
		configMap.SetKey("sasl.mechanism", config.Sasl.Mechanism)
		configMap.SetKey("sasl.username", config.Sasl.UserName)
		configMap.SetKey("sasl.password", config.Sasl.Password)
	}

	// Create a new consumer
	var err error
	consumer, err = kafka.NewConsumer(configMap)
	if err != nil {
		panic(err)
	}

	topics := strings.Split(config.Topics, ",")

	// Subscribe topics
	err = consumer.SubscribeTopics(topics, nil)
	if err != nil {
		panic(err)
	}

	for {
		select {
		case event := <-consumer.Events():
			switch msg := event.(type) {
			case *kafka.Message:
				// Handle one message.
				// NOTICE: message handler SHOULD NOT take too longer time that would make consumer failed.
				go func() {
					panicErr := recover()
					if panicErr != nil {
						fmt.Printf("handleMsgFunc panic, %v, %v\n", panicErr, debug.Stack())
					}
					handleMsgFunc(msg)
				}()
			case *kafka.Error:
				fmt.Printf("consumer met error: %s\n", msg.Error())
			}
		case <-ctx.Done():
			return
		}

	}
}

func StopConsumer() error {
	return consumer.Close()
}
