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

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime
import uvicorn

app = FastAPI(open_api_url=None, docs_url=None, redoc_url=None)


# 返回一个html页面
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastAPI Hello World</title>
    <style>
        :root {
            --vp-c-brand: #009688;
            --vp-c-brand-light: #4db6ac;
            --vp-c-brand-lighter: #b2dfdb;
            --vp-c-text-1: #213547;
            --vp-c-text-2: #476582;
            --vp-c-text-3: #7c8b9c;
            --vp-c-bg: #ffffff;
            --vp-c-bg-alt: #f6f6f7;
            --vp-c-bg-elv: #ffffff;
            --vp-c-divider: #e2e2e3;
            --vp-c-border: #c2c2c4;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            font-size: 16px;
            line-height: 1.7;
            color: var(--vp-c-text-1);
            background-color: var(--vp-c-bg);
        }

        .container {
            max-width: 1152px;
            margin: 0 auto;
            padding: 0 24px;
        }

        .hero {
            padding: 48px 0 64px;
            text-align: center;
        }

        .hero h1 {
            font-size: 48px;
            font-weight: 900;
            line-height: 1.1;
            margin: 0 0 16px;
            background: linear-gradient(315deg, var(--vp-c-brand) 25%, var(--vp-c-brand-light));
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero .tagline {
            font-size: 20px;
            color: var(--vp-c-text-2);
            margin: 0 0 32px;
            max-width: 576px;
            margin-left: auto;
            margin-right: auto;
        }

        .hero .actions {
            display: flex;
            gap: 16px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .btn {
            display: inline-block;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            text-decoration: none;
            border-radius: 8px;
            transition: all 0.25s;
            border: 2px solid transparent;
        }

        .btn-brand {
            background-color: var(--vp-c-brand);
            color: white;
        }

        .btn-brand:hover {
            background-color: var(--vp-c-brand-light);
        }

        .btn-alt {
            background-color: var(--vp-c-bg-alt);
            color: var(--vp-c-text-1);
            border-color: var(--vp-c-border);
        }

        .btn-alt:hover {
            border-color: var(--vp-c-brand);
        }

        .content {
            padding: 0 0 64px;
        }

        .content h2 {
            font-size: 32px;
            font-weight: 600;
            margin: 48px 0 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--vp-c-divider);
        }

        .content h3 {
            font-size: 24px;
            font-weight: 600;
            margin: 32px 0 16px;
            color: var(--vp-c-text-1);
        }

        .content p {
            margin: 16px 0;
            color: var(--vp-c-text-2);
        }

        .api-card {
            background-color: var(--vp-c-bg-alt);
            border: 1px solid var(--vp-c-border);
            border-radius: 12px;
            padding: 24px;
            margin: 24px 0;
        }

        .api-card h4 {
            margin: 0 0 12px;
            font-size: 18px;
            font-weight: 600;
            color: var(--vp-c-text-1);
        }

        .api-card .method {
            display: inline-block;
            background-color: var(--vp-c-brand);
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 8px;
        }

        .api-card .method.post {
            background-color: #ff9800;
        }

        .api-card .method.put {
            background-color: #2196f3;
        }

        .api-card .method.delete {
            background-color: #f44336;
        }

        .api-card .endpoint {
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            background-color: var(--vp-c-bg-elv);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 14px;
        }

        .code-block {
            background-color: var(--vp-c-bg-elv);
            border: 1px solid var(--vp-c-border);
            border-radius: 8px;
            padding: 16px;
            margin: 16px 0;
            overflow-x: auto;
        }

        .code-block pre {
            margin: 0;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
            line-height: 1.5;
            color: var(--vp-c-text-1);
        }

        .tip {
            background-color: var(--vp-c-brand-lighter);
            border-left: 4px solid var(--vp-c-brand);
            padding: 16px;
            margin: 24px 0;
            border-radius: 0 8px 8px 0;
        }

        .tip p {
            margin: 0;
            color: var(--vp-c-text-1);
        }

        .tip strong {
            color: var(--vp-c-brand);
        }

        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
            margin: 32px 0;
        }

        .feature-card {
            background-color: var(--vp-c-bg-alt);
            border: 1px solid var(--vp-c-border);
            border-radius: 12px;
            padding: 24px;
            text-align: center;
        }

        .feature-card h3 {
            margin: 0 0 16px;
            color: var(--vp-c-brand);
        }

        @media (max-width: 768px) {
            .hero h1 {
                font-size: 36px;
            }
            
            .hero .tagline {
                font-size: 18px;
            }
            
            .container {
                padding: 0 16px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>FastAPI Hello World</h1>
            <p class="tagline">
                A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
            </p>
            <div class="actions">
                <a href="https://fastapi.tiangolo.com/" class="btn btn-brand" target="_blank">Get Started</a>
                <a href="https://fastapi.tiangolo.com/tutorial/" class="btn btn-alt" target="_blank">Documentation</a>
            </div>
        </div>

        <div class="content">
            <h2>Welcome</h2>
            <p>
                If you see this page, the FastAPI web server is successfully installed and working. 
                FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ 
                based on standard Python type hints.
            </p>

            <div class="tip">
                <p><strong>Tip:</strong> This is a basic Hello World application. You can start building your API by creating endpoints and models with automatic interactive API documentation.</p>
            </div>


            <h2>API Endpoints</h2>

            <div class="api-card">
                <h4>
                    <span class="method">GET</span>
                    <span class="endpoint">/ping</span>
                </h4>
                <p><strong>Description:</strong> Health check endpoint to verify the service is running</p>
                <p><strong>Response:</strong></p>
                <div class="code-block">
                    <pre>{
  "message": "pong",
  "timestamp": "2024-01-15T10:30:45.123Z",
  "status": "success"
}</pre>
                </div>
            </div>
          
            <h2>Interactive API Documentation</h2>
            <p>
                FastAPI automatically generates interactive API documentation. Once your FastAPI server is running, 
                you can access the interactive documentation at:
            </p>
            <ul>
                <li><strong>Swagger UI:</strong> <code>root path + /docs</code></li>
                <li><strong>ReDoc:</strong> <code>root path + /redoc</code></li>
            </ul>

            <div class="tip">
                <p><strong>Pro Tip:</strong> FastAPI automatically validates request/response data, generates OpenAPI schema, and provides type hints for better IDE support!</p>
            </div>
        </div>
    </div>
</body>
</html>"""


@app.get("/ping")
def read_ping():
    return {
        "message": "pong",
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "success",
    }


# 启动服务

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
