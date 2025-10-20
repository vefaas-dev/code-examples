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
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"os"

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

	switch ceType := ce.Type(); ceType {
	case events.FaasSnsEvent:
		var snsEvents SnsEvents
		err := json.Unmarshal(ce.Data(), &snsEvents)
		if err != nil {
			errMsg := fmt.Sprintf("failed to unmarshal cloudevent payload, error: %v", err)
			fmt.Fprintln(os.Stderr, errMsg)
			return &events.EventResponse{
				StatusCode: http.StatusBadRequest,
				Body:       []byte(errMsg),
			}, nil
		}

		// extract message data from sns event and write to rocketmq topic in a single batch
		batchJobs := BatchJobs{Jobs: make([]ArkBatchJob, 0)}
		for _, snsEvent := range snsEvents.Records {
			var batchJob ArkBatchJob
			if err := json.Unmarshal([]byte(snsEvent.Sns.Message), &batchJob); err != nil {
				errMsg := fmt.Sprintf("failed to unmarshal sns message field, error: %v", err)
				fmt.Fprintln(os.Stderr, errMsg)
				// can do additional handling here
				continue
			}

			switch batchJob.EventName {
			case "BatchJobFinished":
				var jobInfo JobInfoFinished
				if err := json.Unmarshal(batchJob.JobInfo, &jobInfo); err != nil {
					errMsg := fmt.Sprintf("failed to unmarshal job info finished, error: %v", err)
					fmt.Fprintln(os.Stderr, errMsg)
					// can do additional handling here
					continue
				}
				fmt.Printf("received BatchJobFinished, job info: %v\n", jobInfo)
				// Do something with with jobInfo
			case "BatchJobFailed":
				var jobInfo JobInfoFailed
				if err := json.Unmarshal(batchJob.JobInfo, &jobInfo); err != nil {
					errMsg := fmt.Sprintf("failed to unmarshal job info failed, error: %v", err)
					fmt.Fprintln(os.Stderr, errMsg)
					// can do additional handling here
					continue
				}
				fmt.Printf("received BatchJobFailed, job info: %v\n", jobInfo)
				// Do something with with jobInfo
			default:
				fmt.Fprintf(os.Stderr, "unknown event name: %s\n", batchJob.EventName)
				continue
			}

			batchJobs.Jobs = append(batchJobs.Jobs, batchJob)
		}

		// send to rocketmq in a byte format using {"jobs": [{ // Ark batch job 1 }, { // Ark batch job 2 }]}
		payloadData, err := json.Marshal(batchJobs)
		if err != nil {
			errMsg := fmt.Sprintf("failed to marshal batch jobs, error: %v", err)
			fmt.Fprintln(os.Stderr, errMsg)
			return &events.EventResponse{
				StatusCode: http.StatusInternalServerError,
				Body:       []byte(errMsg),
			}, nil
		}

		topic := os.Getenv("TOPIC")
		res, err := WriteToTopic(ctx, topic, payloadData)
		if err != nil {
			fmt.Fprintf(os.Stderr, "error writing to topic %s: %v\n", topic, err)
			return &events.EventResponse{StatusCode: http.StatusInternalServerError}, nil
		}

		fmt.Printf("send message to topic %s success: result = %s\n", topic, res.String())

		body, _ := json.Marshal(map[string]string{"message": "Successfully sent to topic " + topic})
		return &events.EventResponse{
			StatusCode: http.StatusOK,
			Body:       body,
		}, err
	default:
		errMsg := fmt.Sprintf("unknown cloudevent type %q, request id: %s, request data: %s",
			ceType,
			vefaascontext.RequestIdFromContext(ctx),
			ce.Data(),
		)
		fmt.Fprintln(os.Stderr, errMsg)
		return nil, errors.New(errMsg)
	}
}
