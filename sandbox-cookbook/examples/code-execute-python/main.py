"""
Code Sandbox - Code Execution Example (Python SDK)

Execute Python / Node.js / Shell code in a sandbox
"""

import asyncio
import os

import volcenginesdkcore
from volcenginesdkcore.api_client import ApiClient
from volcenginesdkvefaas import VEFAASApi, CreateSandboxRequest, KillSandboxRequest
import httpx
from dotenv import load_dotenv

load_dotenv()


async def main():
    config = volcenginesdkcore.Configuration()
    config.ak = os.getenv("VOLC_ACCESS_KEY")
    config.sk = os.getenv("VOLC_SECRET_KEY")
    config.region = os.getenv("VEFAAS_REGION", "cn-beijing")
    api = VEFAASApi(ApiClient(config))

    function_id = os.getenv("SANDBOX_APP_ID")
    endpoint = os.getenv("SANDBOX_ENDPOINT", "").rstrip("/")

    print("Creating sandbox...")
    resp = await asyncio.to_thread(
        api.create_sandbox,
        CreateSandboxRequest(
            function_id=function_id,
            cpu_milli=500, memory_mb=1024,
            timeout=1800, timeout_unit="second",
        ),
    )
    sandbox_id = resp.sandbox_id
    print(f"Sandbox created: {sandbox_id}")

    async with httpx.AsyncClient(
        headers={"x-faas-instance-name": sandbox_id}, timeout=60.0
    ) as client:

        print("\n--- Python ---")
        r = await client.post(f"{endpoint}/v1/code/execute", json={
            "language": "python",
            "code": "import json, platform\nprint(json.dumps({'python': platform.python_version(), 'os': platform.platform()}, indent=2))",
            "timeout": 10,
        })
        print(r.json()["data"]["stdout"])

        print("--- Node.js ---")
        r = await client.post(f"{endpoint}/v1/code/execute", json={
            "language": "javascript",
            "code": "console.log(JSON.stringify({ node: process.version, pid: process.pid }, null, 2))",
            "timeout": 10,
        })
        print(r.json()["data"]["stdout"])

        print("--- Shell ---")
        r = await client.post(f"{endpoint}/v1/shell/exec", json={
            "command": "echo 'Current directory:' && pwd && ls -la /home/tiger",
            "timeout": 10,
        })
        print(r.json()["data"]["output"])

    print(f"\nDestroying sandbox: {sandbox_id}")
    await asyncio.to_thread(
        api.kill_sandbox,
        KillSandboxRequest(function_id=function_id, sandbox_id=sandbox_id),
    )
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
