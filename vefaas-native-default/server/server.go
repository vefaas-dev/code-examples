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
	"context"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/gorilla/mux"
)

// SimpleServer contains necessary components of the server.
type SimpleServer struct {
	httpServer *http.Server
}

func buildSimpleServer(s *SimpleServer) *http.Server {
	port := os.Getenv("_FAAS_RUNTIME_PORT")
	if port == "" {
		log.Fatal("failed to load _FAAS_RUNTIME_PORT")
	}

	return &http.Server{
		Addr:    ":" + port,
		Handler: s.buildHTTPHandler(),
	}
}

func (s *SimpleServer) buildHTTPHandler() http.Handler {
	r := mux.NewRouter()
	r.Path("/").HandlerFunc(helloHandler)

	// NOTE: GET v1/ping should be provided for liveness check by FaaS Platform.
	// Status Code OK denotes that the service is healthy.
	v1Router := r.PathPrefix("/v1").Subrouter()
	v1Router.Path("/ping").Methods(http.MethodGet).HandlerFunc(pingHandler)

	return r
}

// Start starts the server.
func (s *SimpleServer) Start() {
	log.Printf("start simple server, port: %s", s.httpServer.Addr)

	go func() {
		if err := s.httpServer.ListenAndServe(); err != http.ErrServerClosed {
			log.Fatalf("server listen error: %v", err)
		}
	}()
}

// Stop stops the server.
func (s *SimpleServer) Stop() {
	log.Printf("stop simple server...")

	// Get function timeout configuration from env.
	ctx := context.Background()
	if timeout, _ := strconv.ParseInt(os.Getenv("_FAAS_FUNC_TIMEOUT"), 10, 64); timeout != 0 {
		var cancel context.CancelFunc
		ctx, cancel = context.WithTimeout(context.Background(), time.Duration(timeout)*time.Second)
		defer cancel()
	}

	if err := s.httpServer.Shutdown(ctx); err != nil {
		log.Fatalf("failed to shutdown server, error: %v", err)
	}
}

// NewSimpleServer creates a new simple server.
func NewSimpleServer() (s *SimpleServer) {
	s = &SimpleServer{}
	s.httpServer = buildSimpleServer(s)

	return
}
