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

import json


def handler(event, context):
    # Log incoming request.
    #
    # NOTE: the log here is only for debug purpose. It's recommended to delete those debug/info
    # logs and only print log where error occurs after your business logic is verified and ready to
    # go production, nor the log amount may be too huge.
    print(f"received new request, event content: {event}")
    print(f"context: {context}")

    result = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Hello veFaaS from Python 3.9!"}),
    }
    return result
