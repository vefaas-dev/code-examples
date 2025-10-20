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
	"errors"
	"fmt"
	"os"

	"github.com/volcengine/vefaas-golang-runtime/events"
	"github.com/volcengine/vefaas-golang-runtime/vefaascontext"
)

func HandleCloudEventRequest(ctx context.Context, ce *events.CloudEvent) (*events.EventResponse, error) {
	switch cloudeventType := ce.Type(); cloudeventType {
	case events.FaasTosEvent:
		return handleTosEvent(ctx, ce)
	default:
		errMsg := fmt.Sprintf("unknown cloudevent type %q, request id: %s, request data: %s",
			cloudeventType,
			vefaascontext.RequestIdFromContext(ctx),
			ce.Data(),
		)
		fmt.Fprintln(os.Stderr, errMsg)
		return nil, errors.New(errMsg)
	}
}
