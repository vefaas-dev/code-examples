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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import requests  #
from stream_unzip import stream_unzip  #
import tempfile
import gc  #
import zipfile

# TOS sdk reference: https://www.volcengine.com/docs/6349/93480
import tos
import time
import threading

# AccessKey and SecretKey of your MCDN account
ak = ""
sk = ""

# TOS endpoints & region reference: https://www.volcengine.com/docs/6349/107356
endpoint = "tos-cn-beijing.ivolces.com"
region = "cn-beijing"

# by default unzipped file will be uploaded to this directory
destination = "uncompressed"


def unzip_and_upload(bucket_name, object_key, signed_url, client):
    try:
        response = requests.get(signed_url, stream=True)
        response.raise_for_status()
        start_time = time.time()

        for filename, file_size, file_iter in stream_unzip(response.raw):
            if isinstance(filename, bytes):
                filename = filename.decode("utf-8")

            new_prefix = os.path.join(destination, object_key.replace(".zip", ""))
            upload_key = os.path.join(new_prefix, filename)
            print(f"Uploading: {upload_key} ({file_size} bytes)")
            client.put_object(bucket_name, upload_key, content=file_iter)

            gc.collect()
            print(f"Uploaded: {upload_key}, GC done")

        duration = time.time() - start_time
        print(f"✅ All files uploaded in {duration:.2f}s")
    except Exception as e:
        print(f"❌ unzip_and_upload failed: {e}")


def handler(event, context):
    print("received new request, event content:\n")
    print(json.dumps(event, sort_keys=True, indent=4))

    # vefaas 特俗
    if event["eventType"] == "http" and event["path"] == "/ping":
        time.sleep(900)
        return
    if event["eventType"] == "timer":
        time.sleep(900)
        return

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

    client = tos.TosClientV2(ak, sk, endpoint, region)
    # Create a pre-signed URL to download the zip file
    signed_url = client.pre_signed_url(
        http_method=tos.HttpMethodType.Http_Method_Get,
        bucket=bucket_name,
        key=object_key,
        expires=3600,  # URL expiration time in seconds (1 hour)
    ).signed_url
    t = threading.Thread(
        target=unzip_and_upload,
        args=(bucket_name, object_key, signed_url, client),
        daemon=True,
    )
    t.start()

    result = {
        "statusCode": 202,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "message": {
                    "message": "uploading file in the background",
                }
            }
        ),
    }
    return result
