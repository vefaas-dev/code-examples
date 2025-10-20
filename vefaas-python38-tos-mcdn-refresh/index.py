# Copyright (c) 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from mcdn import request

# AccessKey and SecretKey of your MCDN account
AK = "AK"
SK = "SK"

# list of URLs to refresh / preload, max 20 urls
# https://www.volcengine.com/docs/6766/127750
UPDATE_URL_LIST = [
    "http://domain1.com/",
    "http://domain2.com/",
]


def handler(event, context):
    print(f"received new request, event content: {event}")
    print(json.dumps(event, sort_keys=True, indent=4))

    # TOS trigger event ref: https://bytedance.feishu.cn/wiki/wikcn0KSWFoMRtj8B2PMY4UZmOh
    uri = event["data"]["events"][0]["tos"]["object"]["key"]

    update_url_str = ""
    for url in UPDATE_URL_LIST:
        update_url_str += url + uri + "\n"

    refresh_request_body = {
        "Urls": update_url_str,
        "Type": "file",
    }

    refresh_response_body = request(
        "POST", {}, {}, AK, SK, "SubmitRefreshTask", refresh_request_body
    )
    print(refresh_response_body)

    if "Error" in refresh_response_body["ResponseMetadata"]:
        # 刷新失败
        err = (
            "刷新失败: " + refresh_response_body["ResponseMetadata"]["Error"]["Message"]
        )
        result = {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": err}),
        }
        return result

    # 执行预热步骤
    print("刷新已成功")

    # ==== MCDN Preload code below, uncomment the codes below to enable ====
    # preload_request_body = {
    #     "Urls": update_url_str,
    # }
    # preload_response_body = request("POST", {}, {}, AK, SK, "SubmitPreloadTask", preload_request_body)
    # print(preload_response_body)
    # if "Error" in preload_response_body["ResponseMetadata"]:
    #     # 预热失败
    #     err = "预热失败: " + preload_response_body["ResponseMetadata"]["Error"]["Message"]
    #     result = {
    #         'statusCode': 400,
    #         'headers': {
    #             'Content-Type': 'application/json'
    #         },
    #         'body': json.dumps({
    #             'message': err
    #         })
    #     }
    #     print(err)
    #     return result
    # print("预热已成功")

    result = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "message": {
                    "message": "success",
                }
            }
        ),
    }
    return result
