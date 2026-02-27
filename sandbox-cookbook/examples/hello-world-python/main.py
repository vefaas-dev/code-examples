"""
veFaaS Sandbox Quick Start - Python SDK

Minimal flow: Create sandbox -> Execute code -> Get result -> Destroy sandbox
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
            cpu_milli=500,
            memory_mb=1024,
            timeout=1800,
            timeout_unit="second",
        ),
    )
    sandbox_id = resp.sandbox_id
    print(f"Sandbox created: {sandbox_id}")

    print("Executing Python code...")
    async with httpx.AsyncClient(
        headers={"x-faas-instance-name": sandbox_id}, timeout=30.0
    ) as client:
        r = await client.post(
            f"{endpoint}/v1/code/execute",
            json={
                "language": "python",
                "code": "print('Hello from veFaaS Sandbox!')\nresult = sum(range(100))\nprint(f'1+2+...+99 = {result}')",
                "timeout": 10,
            },
        )
        data = r.json()["data"]
        print(f"stdout: {data['stdout'].strip()}")

    print(f"Destroying sandbox: {sandbox_id}")
    await asyncio.to_thread(
        api.kill_sandbox,
        KillSandboxRequest(function_id=function_id, sandbox_id=sandbox_id),
    )
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
