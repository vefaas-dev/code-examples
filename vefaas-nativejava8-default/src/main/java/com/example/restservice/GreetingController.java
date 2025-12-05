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

package com.example.restservice;

import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.web.bind.annotation.*;

@RestController
public class GreetingController {
    private static final String template = "Hello, %s!";
    private final AtomicLong counter = new AtomicLong();

    @GetMapping(value = {"", "/"})
    public Greeting get(@RequestParam(value = "name", defaultValue = "World?") String name,
                        @RequestHeader Map<String, String> requestHeaders) {
        System.out.println("request headers: " + requestHeaders);
        return new Greeting(counter.incrementAndGet(), String.format(template, name));
    }

    @PostMapping(value = {"", "/"})
    public Greeting post(@RequestParam(value = "name", defaultValue = "World?") String name,
                         @RequestHeader Map<String, String> requestHeaders,
                         @RequestBody(required=false) String requestBody) {
        String eventType = requestHeaders.getOrDefault("ce-type", "");
        switch (eventType) {
            case "bytefaas.timer.event":
                System.out.println("received timer event, request body is: " + requestBody);
                break;
            case "bytefaas.kafka.event":
            case "bytefaas.rocketmq.event":
            case "bytefaas.tos.event":
                String topic = requestHeaders.get("ce-topic");
                String consumerGroup = requestHeaders.get("ce-consumergroup");
                int badStatusRetryNum = Integer.parseInt(requestHeaders.get("ce-retries_for_bad_status_requests"));
                System.out.printf("received %s event. topic: %s group: %s retry: %d\n request payload: %s", eventType,topic, consumerGroup, badStatusRetryNum, requestBody);
                break;
            default:
                System.out.printf("received regular http post request, request body is: %s", eventType, requestBody);
        }
        return new Greeting(counter.incrementAndGet(), String.format(template, name));
    }
}