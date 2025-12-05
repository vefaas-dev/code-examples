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

// See https://www.volcengine.com/docs/6349/128981.
type TosEvents struct {
	Events []TosEvent `json:"events"`
}
type TosEvent struct {
	EventName    string `json:"eventName"`
	EventSource  string `json:"eventSource"`
	EventTime    string `json:"eventTime"`
	EventVersion string `json:"eventVersion"`
	Tos          struct {
		Bucket struct {
			Trn           string `json:"trn,omitempty"`
			Name          string `json:"name,omitempty"`
			OwnerIdentify string `json:"ownerIdentify,omitempty"`
		} `json:"bucket,omitempty"`
		Object struct {
			Etag      string `json:"eTag,omitempty"`
			Key       string `json:"key,omitempty"`
			Size      int64  `json:"size,omitempty"`
			VersionId string `json:"versionId,omitempty"`
		} `json:"object,omitempty"`
		TosSchemaVersion string `json:"tosSchemaVersion"`
		NotificationId   string `json:"ruleId"`
		Region           string `json:"region"`
		RequestParams    struct {
			SourceIPAddress string `json:"sourceIPAddress,omitempty"`
		} `json:"requestParameters,omitempty"`
		ResponseElements struct {
			TosRequestID string `json:"requestId,omitempty"`
		} `json:"responseElements,omitempty"`
		UserIdentity struct {
			PrincipalId string `json:"principalId,omitempty"`
		} `json:"userIdentity,omitempty"`
		CustomCallbackParams CallbackVar         `json:"xVars,omitempty"`
		ArchiveEventData     *ArchiveEventData   `json:"archiveEventData,omitempty"`
		LifecycleEventData   *LifecycleEventData `json:"lifecycleEventData,omitempty"`
	} `json:"tos"`
}

type LifecycleEventData struct {
	TransitionEventData struct {
		DestinationStorageClass string `json:"destinationStorageClass,omitempty"`
	} `json:"transitionEventData,omitempty"`
}

type ArchiveEventData struct {
	RestoreEventData struct {
		LifecycleRestorationExpiryTime string `json:"restorationExpiryTime,omitempty"`
		LifecycleRestoreStorageClass   string `json:"restoreStorageClass,omitempty"`
	} `json:"restoreEventData,omitempty"`
}

type CallbackVar map[string]interface{}
