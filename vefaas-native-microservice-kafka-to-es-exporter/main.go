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

package main

import (
	"context"
	"encoding/json"
	"fmt"
	"kafka-to-es/es"
	"kafka-to-es/kafka"
	"log"
	"os"
	"os/signal"
	"syscall"

	confluentKafka "github.com/confluentinc/confluent-kafka-go/kafka"
)

type Config struct {
	Kafka *kafka.Conf `json:"kafka"`
	ES    *es.Conf    `json:"elasticsearch"`
}

func LoadConfig(configPath string) (*Config, error) {
	file, err := os.Open(configPath)
	if err != nil {
		return nil, fmt.Errorf("load configuration filed. %s", err.Error())
	}

	defer file.Close()

	config := &Config{
		Kafka: kafka.NewKafkaConf(),
		ES:    &es.Conf{},
	}
	decoder := json.NewDecoder(file)
	err = decoder.Decode(config)
	if err != nil {
		return nil, fmt.Errorf("parse configuration failed. %s", err.Error())
	}

	err = config.Kafka.Validate()
	if err != nil {
		return nil, err
	}
	err = config.ES.Validate()
	if err != nil {
		return nil, err
	}

	return config, nil
}

func main() {
	conf, err := LoadConfig("config/config.json")
	if err != nil {
		fmt.Printf("load config file met error: %s\n", err.Error())
		return
	}
	es.InitESClient(conf.ES)
	ctx, cancelFunc := context.WithCancel(context.Background())
	handler := func(message *confluentKafka.Message) {
		document := map[string]interface{}{
			"key":       string(message.Key),
			"value":     string(message.Value),
			"topic":     *message.TopicPartition.Topic,
			"partition": message.TopicPartition.Partition,
			"offset":    message.TopicPartition.Offset,
			"timestamp": message.Timestamp.String(),
		}
		headers := make(map[string]string)
		for _, h := range message.Headers {
			headers[h.Key] = string(h.Value)
		}
		document["header"] = headers
		err := es.CreateESDocument(document)
		if err != nil {
			fmt.Printf("create es document met error: %s", err.Error())
		}
	}
	go kafka.StartConsumer(ctx, conf.Kafka, handler)

	sigterm := make(chan os.Signal, 1)
	signal.Notify(sigterm, syscall.SIGINT, syscall.SIGTERM)
	<-sigterm
	log.Println("terminating: via signal")
	cancelFunc()
	if err = kafka.StopConsumer(); err != nil {
		log.Panicf("Error closing client: %v", err)
	}
}
