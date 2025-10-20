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
import os
import json
import tempfile
import zipfile

# TOS sdk reference: https://www.volcengine.com/docs/6349/93480
import tos

# AccessKey and SecretKey of your MCDN account
ak = "your_access_key"
sk = "your_secret_key"

# TOS endpoints & region reference: https://www.volcengine.com/docs/6349/107356
endpoint = "tos-cn-beijing.ivolces.com"
region = "cn-beijing"

# by default unzipped file will be uploaded to this directory
destination = "uncompressed"


def handler(event, context):
    print("received new request, event content:\n")
    print(json.dumps(event, sort_keys=True, indent=4))

    # TOS trigger event schema reference: https://www.volcengine.com/docs/6662/127868
    object_key = event["data"]["events"][0]["tos"]["object"]["key"]
    bucket_name = event["data"]["events"][0]["tos"]["bucket"]["name"]
    base_file_name = os.path.basename(object_key)

    _, file_extension = os.path.splitext(base_file_name)

    # filter out non-zip file
    if file_extension != ".zip":
        print("Unsupported file extension: {}".format(object_key))
        return

    # filter out files already in {destination} location, avoid duplicate file upload
    if object_key.split(os.path.sep)[0] == destination:
        print(
            "File {} uploaded to {}, intentionally ignore files uploaded to this location".format(
                object_key, destination
            )
        )
        return

    temp_dir = tempfile.TemporaryDirectory()
    file_name = os.path.join(temp_dir.name, base_file_name)

    # Download file
    try:
        # Create tos client
        client = tos.TosClientV2(ak, sk, endpoint, region)
        print(
            "Downloading package from :{}/{} into local dir: {}".format(
                bucket_name, object_key, file_name
            )
        )
        client.get_object_to_file(bucket_name, object_key, file_name)
    except tos.exceptions.TosClientError as e:
        # most likely caused by client side configuration error, or client-side networking issue
        raise Exception(
            "TOS client error, message:{}, cause: {}".format(e.message, e.cause)
        )
    except tos.exceptions.TosServerError as e:
        # TOS server side exception
        raise Exception("TOS server error, code: {}".format(e.code))
    except Exception as e:
        raise Exception("Unknown error: {}".format(e))

    newPrefix = os.path.join(destination, object_key.replace(".zip", ""))
    # opening the zip file in READ mode
    with zipfile.ZipFile(file_name, "r") as zip_file:
        # printing all the contents of the zip file
        for name in zip_file.namelist():
            file = zip_file.open(name)
            r_data = file.read()
            if r_data:  # filter folder
                result = client.put_object(
                    bucket_name, os.path.join(newPrefix, name), content=r_data
                )
            file.close()

    result = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "message": {
                    "message": "uploaded file prpcessed successfully",
                }
            }
        ),
    }
    return result
