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

package handlers

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	"github.com/volcengine/vefaas-golang-runtime/events"
	"github.com/volcengine/vefaas-golang-runtime/vefaascontext"
)

func handleTimerEvent(ctx context.Context, ce *events.CloudEvent) (*events.EventResponse, error) {
	// Log incoming request.
	//
	// NOTE: the log here is only for debug purpose. It's recommended to delete those debug/info
	// logs and only print log where error occurs after your business logic is verified and ready to
	// go production, nor the log amount may be too huge.
	fmt.Printf(
		"received timer event, request id: %s, extensions: %+v, payload: %s\n",
		vefaascontext.RequestIdFromContext(ctx),
		ce.Extensions(),
		ce.Data(),
	)

	var contentTask ContentTask
	err := json.Unmarshal(ce.Data(), &contentTask)
	if err != nil {
		errMsg := fmt.Sprintf("failed to unmarshal cloudevent payload, error: %v", err)
		fmt.Fprintln(os.Stderr, errMsg)
		return &events.EventResponse{
			StatusCode: http.StatusBadRequest,
			Body:       []byte(errMsg),
		}, nil
	}

	bizResp, err := processTask(ctx, &contentTask)
	return transformResponse(ctx, bizResp, err)
}
