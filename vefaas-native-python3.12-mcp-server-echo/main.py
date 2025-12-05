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

"""
FastMCP Echo Server
"""

import os
import argparse
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP(
    "Echo Server",
    host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_SERVER_PORT", "8000")),
    streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"),
)


@mcp.tool()
def hello_tool(name: str) -> str:
    """Say hello"""
    return f"Hello, {name}!"


@mcp.tool()
def echo_tool(text: str) -> str:
    """Echo the input text"""
    return text


@mcp.resource("echo://static")
def echo_resource() -> str:
    return "Echo!"


@mcp.resource("echo://{text}")
def echo_template(text: str) -> str:
    """Echo the input text"""
    return f"Echo: {text}"


@mcp.prompt("echo")
def echo_prompt(text: str) -> str:
    return text


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the Echo MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["streamable-http", "stdio"],
        default="streamable-http",
        help="Transport protocol to use (streamable-http or stdio)",
    )

    args = parser.parse_args()

    try:
        # Run the MCP server
        logger.info(f"Starting Echo MCP Server with {args.transport} transport")
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Echo MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
