"""
Sandbox Manager - Lifecycle Management Example (Python SDK)

Create, describe, list, extend timeout, and destroy sandboxes
"""

import asyncio
import os

import volcenginesdkcore
from volcenginesdkcore.api_client import ApiClient
from volcenginesdkvefaas import (
    VEFAASApi,
    CreateSandboxRequest,
    DescribeSandboxRequest,
    ListSandboxesRequest,
    KillSandboxRequest,
    SetSandboxTimeoutRequest,
)
from dotenv import load_dotenv

load_dotenv()


async def main():
    config = volcenginesdkcore.Configuration()
    config.ak = os.getenv("VOLC_ACCESS_KEY")
    config.sk = os.getenv("VOLC_SECRET_KEY")
    config.region = os.getenv("VEFAAS_REGION", "cn-beijing")
    api = VEFAASApi(ApiClient(config))

    function_id = os.getenv("SANDBOX_APP_ID")

    print("=== Create sandbox ===")
    resp = await asyncio.to_thread(
        api.create_sandbox,
        CreateSandboxRequest(
            function_id=function_id,
            cpu_milli=500, memory_mb=1024,
            timeout=1800, timeout_unit="second",
        ),
    )
    sandbox_id = resp.sandbox_id
    print(f"Created: {sandbox_id}")

    try:
        print("\n=== Describe sandbox ===")
        info = await asyncio.to_thread(
            api.describe_sandbox,
            DescribeSandboxRequest(function_id=function_id, sandbox_id=sandbox_id),
        )
        print(f"Status: {info.status}")
        print(f"CPU: {info.cpu_milli / 1000}vCPU, Memory: {info.memory_mb / 1024}GiB")

        print("\n=== List active sandboxes ===")
        list_resp = await asyncio.to_thread(
            api.list_sandboxes,
            ListSandboxesRequest(function_id=function_id),
        )
        sandboxes = list_resp.sandboxes
        print(f"Total: {len(sandboxes)} sandbox(es)")
        for sb in sandboxes[:5]:
            print(f"  - {sb.id}")
            print(f"    Status: {sb.status}, CPU: {sb.cpu_milli / 1000}vCPU, Memory: {sb.memory_mb / 1024}GiB")
            print(f"    Created: {sb.created_at}, Expires: {sb.expire_at}")

        print("\n=== Extend timeout ===")
        await asyncio.to_thread(
            api.set_sandbox_timeout,
            SetSandboxTimeoutRequest(function_id=function_id, sandbox_id=sandbox_id, timeout=60),
        )
        print("Timeout extended successfully")

    finally:
        print(f"\n=== Destroy sandbox: {sandbox_id} ===")
        await asyncio.to_thread(
            api.kill_sandbox,
            KillSandboxRequest(function_id=function_id, sandbox_id=sandbox_id),
        )
        print("Sandbox destroyed.")


if __name__ == "__main__":
    asyncio.run(main())
