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

import { streamText, UIMessage, convertToModelMessages } from 'ai';
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';

// Allow streaming responses up to 30 seconds
export const maxDuration = 30;

export async function POST(req: Request) {
    const {
        messages,
        model,
    }: {
        messages: UIMessage[];
        model: string;
    } = await req.json();

    const gateway = createOpenAICompatible({
        name: 'volcengine',
        apiKey: process.env.ARK_API_KEY,
        baseURL: `${process.env.ARK_BASE_URL ?? 'https://ark.cn-beijing.volces.com/api/v3'}`,
    });

    const result = streamText({
        model: gateway(model),
        messages: convertToModelMessages(messages),
        system:
            '你是一个乐于助人的助手，能够回答问题并帮助完成任务',
    });

    return result.toUIMessageStreamResponse({
        sendSources: true,
        sendReasoning: true,
    });
}