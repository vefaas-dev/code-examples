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

#! /bin/bash
set -ex
cd `dirname $0`

# check dependencies
npm install
# output: 'standalone'
npm run build

if [ -d .next/standalone/vefaas-native-nodejs20-nextjs-chatbot ]; then
  cp -R .next/standalone/vefaas-native-nodejs20-nextjs-chatbot/. .next/standalone/
  rm -rf .next/standalone/vefaas-native-nodejs20-nextjs-chatbot
fi

# https://nextjs.org/docs/pages/api-reference/config/next-config-js/output#automatically-copying-traced-files
cp -r public .next/standalone/ && cp -r .next/static .next/standalone/.next/
