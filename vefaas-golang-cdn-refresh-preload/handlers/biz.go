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
	"fmt"
	"net/http"
)

type BizResp struct {
	RequestID string
	Response  interface{}
}

type BizError interface {
	error
	Code() int
	Reason() string
}

type bizErr struct {
	code   int
	reason string
}

func (b *bizErr) Code() int {
	return b.code
}

func (b *bizErr) Reason() string {
	return b.reason
}

func (b *bizErr) Error() string {
	return fmt.Sprintf("status_code: %d, reason: %s", b.code, b.reason)
}

func badRequest(format string, a ...interface{}) *bizErr {
	return &bizErr{
		code:   http.StatusBadRequest,
		reason: fmt.Sprintf(format, a...),
	}
}

func svrError(format string, a ...interface{}) *bizErr {
	return &bizErr{
		code:   http.StatusInternalServerError,
		reason: fmt.Sprintf(format, a...),
	}
}
