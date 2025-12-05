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

	"github.com/volcengine/vefaas-golang-runtime/events"
	"github.com/volcengine/vefaas-golang-runtime/vefaascontext"
)

func HandleCloudEventRequest(ctx context.Context, ce *events.CloudEvent) (*events.EventResponse, error) {
	// Log incoming request.
	//
	// NOTE: the log here is only for debug purpose. It's recommended to delete those debug/info
	// logs and only print log where error occurs after your business logic is verified and ready to
	// go production, nor the log amount may be too huge.
	fmt.Printf(
		"received cloudevent request, request id: %s, cloudevent type: %q, cloudevent extensions: %s, request data: %s\n",
		vefaascontext.RequestIdFromContext(ctx),
		ce.Type(),
		ce.Extensions(),
		ce.Data(),
	)

	// TODO: write your own bussiness logic.

	return &events.EventResponse{StatusCode: http.StatusOK}, nil
}
