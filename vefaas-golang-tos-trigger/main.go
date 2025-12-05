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

package main

import (
	"context"
	"fmt"
	"net/http"
	"os"

	"vefaas-golang-tos-trigger/handlers"

	"github.com/volcengine/vefaas-golang-runtime/events"
	"github.com/volcengine/vefaas-golang-runtime/vefaas"
)

func main() {
	// Start your vefaas function =D.
	vefaas.Start(handler)
}

func handler(ctx context.Context, payload interface{}) (*events.EventResponse, error) {
	switch event := payload.(type) {
	case *events.HTTPRequest:
		return handlers.HandleHttpRequest(ctx, event)
	case *events.CloudEvent:
		return handlers.HandleCloudEventRequest(ctx, event)
	default:
		errMsg := fmt.Sprintf("unknown event type, request: %+v", payload)
		fmt.Fprintln(os.Stderr, errMsg)
		return &events.EventResponse{
			StatusCode: http.StatusBadRequest,
			Body:       []byte(errMsg),
		}, nil
	}
}
