"""
Code Sandbox - Package Manager Example (Python SDK)

Install and verify pip packages in a sandbox
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
        headers={"x-faas-instance-name": sandbox_id}, timeout=120.0
    ) as client:

        print("\n--- Install cowsay ---")
        r = await client.post(f"{endpoint}/v1/shell/exec", json={
            "command": "pip install cowsay", "timeout": 120,
        })
        print(r.json()["data"]["output"])

        print("\n--- Verify installation ---")
        r = await client.post(f"{endpoint}/v1/shell/exec", json={
            "command": "python -c 'import cowsay; cowsay.cow(\"Hello from Sandbox!\")'", "timeout": 10,
        })
        print(r.json()["data"]["output"])

        print("--- Package info ---")
        r = await client.post(f"{endpoint}/v1/shell/exec", json={
            "command": "pip show cowsay", "timeout": 10,
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
