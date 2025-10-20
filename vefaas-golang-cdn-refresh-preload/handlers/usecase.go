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
	"io"
	"net/http"
	"strings"
	"time"

	"github.com/volcengine/volc-sdk-golang/service/cdn"
)

func fillUrls(c *ContentTask) error {
	if len(c.Urls) != 0 {
		return nil
	}
	if len(c.HTTPUrlSource) == 0 {
		return badRequest("either Urls or HTTPUrlSource should be specified")
	}
	cli := &http.Client{Timeout: 5 * time.Second}
	r, err := cli.Get(c.HTTPUrlSource)
	if err != nil {
		return svrError("failed to request source url %q, %s", c.HTTPUrlSource, err)
	}
	defer r.Body.Close()
	content, err := io.ReadAll(r.Body)
	if err != nil {
		return svrError("failed to read body from source url %q, %s", c.HTTPUrlSource, err)
	}
	c.Urls = strings.TrimSpace(string(content))
	return nil
}

func doRefresh(ctx context.Context, contentTask *ContentTask) (interface{}, error) {
	var reqID string
	ft := File
	if contentTask.TaskType != "" {
		ft = contentTask.TaskType
	}
	req := &cdn.SubmitRefreshTaskRequest{
		Type: &ft,
		Urls: contentTask.Urls,
	}
	resp, err := cdn.DefaultInstance.SubmitRefreshTask(req)
	if resp.ResponseMetadata != nil {
		reqID = resp.ResponseMetadata.RequestId
	}
	if err != nil {
		return nil, svrError("failed to submit refresh task, error: %s, api_request_id: %s", err, reqID)
	}
	return resp, nil
}

func doPreload(ctx context.Context, contentTask *ContentTask) (interface{}, error) {
	req := &cdn.SubmitPreloadTaskRequest{
		Urls: contentTask.Urls,
	}
	if contentTask.ConcurrentLimit != 0 {
		req.ConcurrentLimit = &contentTask.ConcurrentLimit
	}
	var reqID string
	resp, err := cdn.DefaultInstance.SubmitPreloadTask(req)
	if resp.ResponseMetadata != nil {
		reqID = resp.ResponseMetadata.RequestId
	}
	if err != nil {
		return nil, svrError("failed to submit preload task, error: %s, api_request_id: %s", err, reqID)
	}
	return resp, nil
}

func processTask(ctx context.Context, contentTask *ContentTask) (*BizResp, error) {
	var (
		respData interface{}
		err      error
	)
	err = fillUrls(contentTask)
	if err != nil {
		return nil, err
	}
	switch contentTask.TaskKind {
	case Refresh:
		respData, err = doRefresh(ctx, contentTask)
		if err != nil {
			return nil, err
		}
	case Preload:
		respData, err = doPreload(ctx, contentTask)
		if err != nil {
			return nil, err
		}
	default:
		return nil, badRequest("unrecognized task kind: %s", contentTask.TaskKind)
	}

	return &BizResp{
		Response: respData,
	}, nil
}
