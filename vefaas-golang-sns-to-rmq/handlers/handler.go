// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
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

package handlers

import (
	"context"
	"fmt"
	"net/http"
	"os"

	"github.com/apache/rocketmq-client-go/v2"
	"github.com/apache/rocketmq-client-go/v2/primitive"
	"github.com/apache/rocketmq-client-go/v2/producer"
	"github.com/volcengine/vefaas-golang-runtime/events"
)

var p rocketmq.Producer

func Handler(ctx context.Context, payload interface{}) (*events.EventResponse, error) {
	switch event := payload.(type) {
	case *events.HTTPRequest:
		return HandleHttpRequest(ctx, event)
	case *events.CloudEvent:
		return HandleCloudEventRequest(ctx, event)
	default:
		errMsg := fmt.Sprintf("unknown event type, request: %+v", payload)
		fmt.Fprintln(os.Stderr, errMsg)
		return &events.EventResponse{
			StatusCode: http.StatusBadRequest,
			Body:       []byte(errMsg),
		}, nil
	}
}

func Initializer(ctx context.Context) error {
	var (
		accessPoint string
		ak          string
		sk          string
		err         error
	)
	accessPoint = os.Getenv("ACCESS_POINT")
	ak = os.Getenv("AK")
	sk = os.Getenv("SK")

	p, err = rocketmq.NewProducer(
		producer.WithNsResolver(primitive.NewPassthroughResolver([]string{accessPoint})),
		producer.WithRetry(2),
		producer.WithCredentials(primitive.Credentials{
			AccessKey: ak,
			SecretKey: sk,
		}),
	)
	if err != nil {
		return fmt.Errorf("create producer: %v", err)
	}

	err = p.Start()
	if err != nil {
		startErr := fmt.Errorf("start producer: %v", err)
		fmt.Fprintln(os.Stderr, startErr.Error())
		return startErr
	}

	fmt.Println("start producer success")
	return nil
}

func WriteToTopic(ctx context.Context, topic string, data []byte) (*primitive.SendResult, error) {
	if p == nil {
		return nil, fmt.Errorf("producer is not initialized")
	}
	msg := &primitive.Message{
		Topic: topic,
		Body:  data,
	}
	res, err := p.SendSync(ctx, msg)
	if err != nil {
		return nil, err
	}
	return res, nil
}
