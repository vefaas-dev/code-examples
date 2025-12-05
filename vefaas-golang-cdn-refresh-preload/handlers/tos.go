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
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"os"
	"strings"

	"github.com/volcengine/vefaas-golang-runtime/events"
	"github.com/volcengine/vefaas-golang-runtime/vefaascontext"
)

func normalizeBaseUrl(baseUrlList []string) {
	for i := range baseUrlList {
		baseUrlList[i] = strings.TrimSpace(baseUrlList[i])
		if !strings.HasSuffix(baseUrlList[i], "/") {
			baseUrlList[i] += "/"
		}
	}
}

func transformError(err error) (*events.EventResponse, error) {
	var be BizError
	if errors.As(err, &be) {
		return &events.EventResponse{
			StatusCode: be.Code(),
			Body:       []byte(be.Reason()),
		}, nil
	}
	return &events.EventResponse{
		StatusCode: http.StatusInternalServerError,
		Body:       []byte(err.Error()),
	}, nil
}

func transformResponse(ctx context.Context, br *BizResp, err error) (*events.EventResponse, error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, err.Error())
		return transformError(err)
	}
	br.RequestID = vefaascontext.RequestIdFromContext(ctx)
	b, _ := json.Marshal(br)
	fmt.Printf("response: %s\n", b)
	return &events.EventResponse{
		StatusCode: http.StatusOK,
		Body:       b,
	}, nil
}

type envInfo struct {
	baseUrls    []string
	tosTaskKind TaskKind
}

func getEnvInfo() (*envInfo, error) {
	BASE_URL_STR := os.Getenv("BASE_URL_LIST")
	if len(BASE_URL_STR) == 0 {
		return nil, fmt.Errorf("no 'BASE_URL_LIST' found in faas environment")
	}
	baseUrlList := strings.Split(BASE_URL_STR, ",")
	normalizeBaseUrl(baseUrlList)

	tosTaskKind := os.Getenv("TOS_EVENT_TASK_KIND")
	switch tosTaskKind {
	case "", Refresh:
		tosTaskKind = Refresh
	case Preload:
	default:
		return nil, fmt.Errorf("invalid 'TOS_EVENT_TASK_KIND' specified in faas environment")
	}

	return &envInfo{
		baseUrls:    baseUrlList,
		tosTaskKind: tosTaskKind,
	}, nil
}

func constructUrls(te *TosEvents, ei *envInfo) []string {
	var urls []string
	for _, e := range te.Events {
		for _, b := range ei.baseUrls {
			// assume the final url is the key joint with env specified base url
			urls = append(urls, b+e.Tos.Object.Key)
		}
	}
	return urls
}

func handleTosEvent(ctx context.Context, ce *events.CloudEvent) (*events.EventResponse, error) {
	// Log incoming request.
	//
	// NOTE: the log here is only for debug purpose. It's recommended to delete those debug/info
	// logs and only print log where error occurs after your business logic is verified and ready to
	// go production, nor the log amount may be too huge.
	fmt.Printf(
		"received tos event, request id: %s, extensions: %+v, payload: %s\n",
		vefaascontext.RequestIdFromContext(ctx),
		ce.Extensions(),
		ce.Data(),
	)

	envInfo, err := getEnvInfo()
	if err != nil {
		return nil, err
	}

	var tosEvents TosEvents
	err = json.Unmarshal(ce.Data(), &tosEvents)
	if err != nil {
		errMsg := fmt.Sprintf("failed to unmarshal cloudevent payload, error: %v", err)
		fmt.Fprintln(os.Stderr, errMsg)
		return &events.EventResponse{
			StatusCode: http.StatusBadRequest,
			Body:       []byte(errMsg),
		}, nil
	}

	urls := constructUrls(&tosEvents, envInfo)

	ct := ContentTask{
		TaskKind: envInfo.tosTaskKind,
		TaskType: File,
		Urls:     strings.Join(urls, "\n"),
	}

	bizResp, err := processTask(ctx, &ct)
	return transformResponse(ctx, bizResp, err)
}
