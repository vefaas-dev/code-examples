# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
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

import json
import os
import logging
from apmplus_server.sdk import Initializer
from apmplus_server.sdk.decorators import task

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize APM before any other operations
headers = {
    "x-byteapm-appkey": os.getenv("APMPLUS_APPKEY", "1ab5dd5d4aabaa7abf6b786a7dd5ed81"),
}


Initializer.init(
    app_name="vefaas-python38-apmplus-app",
    api_endpoint="http://apmplus-cn-beijing.volces.com:4317",
    headers=headers,
)


@task()
def handler(event, context):
    # Log incoming request.
    #
    # NOTE: the log here is only for debug purpose. It's recommended to delete those debug/info
    # logs and only print log where error occurs after your business logic is verified and ready to
    # go production, nor the log amount may be too huge.
    print(f"received new request, event content: {event}")

    result = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Hello veFaaS along with APMPlus!"}),
    }

    logging.info("I am going to print something by logging!")

    return result
