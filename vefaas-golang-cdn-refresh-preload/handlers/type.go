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

type TaskKind = string

const (
	Refresh TaskKind = "refresh"
	Preload TaskKind = "preload"
)

type TaskType = string

const (
	File  TaskType = "file"
	Dir   TaskType = "dir"
	Regex TaskType = "regex"
)

// see https://www.volcengine.com/docs/6454/70438
type ContentTask struct {
	TaskKind        TaskKind `json:"TaskKind,omitempty"`
	TaskType        TaskType `json:"TaskType,omitempty"`
	ConcurrentLimit int64    `json:"ConcurrentLimit,omitempty"`
	Urls            string   `json:"Urls,omitempty"`
	HTTPUrlSource   string   `json:"HTTPUrlSource,omitempty"`
}

// See https://www.volcengine.com/docs/6349/128981.
type TosEvents struct {
	Events []TosEvent `json:"events"`
}

type TosEvent struct {
	EventName    string `json:"eventName"`
	EventSource  string `json:"eventSource"`
	EventTime    string `json:"eventTime"`
	EventVersion string `json:"eventVersion"`

	Tos Tos `json:"tos"`
}

type Tos struct {
	TosSchemaVersion string `json:"tosSchemaVersion"`
	RuleId           string `json:"ruleId"`
	Region           string `json:"region"`

	Bucket       Bucket       `json:"bucket,omitempty"`
	Object       Object       `json:"object,omitempty"`
	UserIdentity UserIdentity `json:"userIdentity,omitempty"`
}

type Bucket struct {
	Trn           string `json:"trn,omitempty"`
	Name          string `json:"name,omitempty"`
	OwnerIdentify string `json:"ownerIdentify,omitempty"`
}

type Object struct {
	Etag      string `json:"eTag,omitempty"`
	Key       string `json:"key,omitempty"`
	Size      int64  `json:"size,omitempty"`
	VersionId string `json:"versionId,omitempty"`
}

type RequestParameters struct {
	SourceIPAddress string `json:"sourceIPAddress,omitempty"`
}

type ResponseElements struct {
	TosRequestID string `json:"requestId,omitempty"`
}

type UserIdentity struct {
	PrincipalId string `json:"principalId,omitempty"`
}
