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

package server

import (
	"fmt"
	"net/http"

	"github.com/alioygur/gores"
)

const (
	requestIdHeaderKey = "X-Faas-Request-Id"
)

// SimpleMessage contains a simple message for return.
type SimpleMessage struct {
	Message string `json:"Message"`
}

func pingHandler(w http.ResponseWriter, _ *http.Request) {
	_ = gores.JSON(w, http.StatusOK, SimpleMessage{Message: "All is well."})
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
	// Log incoming request.
	//
	// NOTE: the log here is only for debug purpose. It's recommended to delete those debug/info
	// logs and only print log where error occurs after your business logic is verified and ready to
	// go production, nor the log amount may be too huge.
	fmt.Printf(
		"received http request: %s %s, request id: %s\n",
		r.Method,
		r.URL.Path,
		r.Header.Get(requestIdHeaderKey),
	)

	_ = gores.JSON(w, http.StatusOK, SimpleMessage{Message: "Hello world from FaaS Native XD"})
}
