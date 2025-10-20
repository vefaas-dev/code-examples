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

import "encoding/json"

type SnsEvents struct {
	Records []SnsEvent `json:"Records"`
}

type SnsEvent struct {
	EventSource          string `json:"EventSource"`
	EventVersion         string `json:"EventVersion"`
	EventSubscriptionArn string `json:"EventSubscriptionArn"`
	Sns                  Sns    `json:"Sns"`
}

type Sns struct {
	Type             string `json:"Type"`
	MessageId        string `json:"MessageId"`
	TopicTrn         string `json:"TopicTrn"`
	Subject          string `json:"Subject"`
	Message          string `json:"Message"`
	Timestamp        string `json:"Timestamp"`
	SignatureVersion string `json:"SignatureVersion"`
	Signature        string `json:"Signature"`
	SigningCertURL   string `json:"SigningCertURL"`
	UnsubscribeToken string `json:"UnsubscribeToken"`
	UnsubscribeURL   string `json:"UnsubscribeURL"`
}

type ArkBatchJob struct {
	EventID   string          `json:"EventID"`
	Project   string          `json:"Project"`
	EventName string          `json:"EventName"`
	EventTime string          `json:"EventTime"`
	AccountID int64           `json:"AccountID"`
	JobInfo   json.RawMessage `json:"JobInfo"`
}

type JobInfoFinished struct {
	JobID              string   `json:"JobID"`
	JobName            string   `json:"JobName"`
	Message            string   `json:"Message"`
	FailNum            int64    `json:"FailNum"`
	TotalNum           int64    `json:"TotalNum"`
	SuccessNum         int64    `json:"SuccessNum"`
	FailFileTOSPath    *TOSPath `json:"FailFileTOSPath"`
	SuccessFileTOSPath *TOSPath `json:"SuccessFileTOSPath"`
}

type JobInfoFailed struct {
	JobID   string `json:"JobID"`
	JobName string `json:"JobName"`
	Message string `json:"Message"`
}

type TOSPath struct {
	BucketName string `json:"BucketName"`
	ObjectKey  string `json:"ObjectKey"`
}

type BatchJobs struct {
	Jobs []ArkBatchJob `json:"jobs"`
}
