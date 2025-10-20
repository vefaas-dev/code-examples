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

import { FastMCP } from "fastmcp";
import { z } from "zod";

const server = new FastMCP({
  name: "Echo Server",
  version: "1.0.0",
});

server.addTool({
  name: "hello_tool",
  description: "Say hello",
  parameters: z.object({
    name: z.string(),
  }),
  execute: async (args) => {
    return `Hello, ${args.name}!`;
  },
});

server.addTool({
  name: "echo_tool",
  description: "Echo the input text",
  parameters: z.object({
    text: z.string(),
  }),
  execute: async (args) => {
    return args.text;
  },
});

server.addPrompt({
  name: "echo",
  description: "Echo the input text",
  load: async ({ text }) => {
    return text;
  },
  arguments: [
    {
      name: "text",
      description: "Text to echo",
      required: true,
    },
  ],
});

server.addResource({
  uri: "echo://static",
  name: "Echo Static",
  mimeType: "text/plain",
  async load() {
    return {
      text: "Echo!",
    };
  },
});

server.addResourceTemplate({
  uriTemplate: "echo://{text}",
  name: "Echo Template",
  description: "Echo the input text",
  mimeType: "text/plain",
  arguments: [
    {
      name: "text",
      description: "Text to echo",
      required: true,
    },
  ],
  async load({ text }) {
    return {
      text: `Echo: ${text}`,
    };
  },
});

server.start({
  transportType: "httpStream",
  httpStream: {
    port: process.env.MCP_SERVER_PORT,
    host: process.env.MCP_SERVER_HOST,
    endpoint: process.env.STREAMABLE_HTTP_PATH,
    stateless: true,
  },
});
