"""
Code Sandbox - File Operations Example (Python SDK)

Write, append, read, and list files in a sandbox
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
        headers={"x-faas-instance-name": sandbox_id}, timeout=30.0
    ) as client:

        print("\n--- Write file ---")
        r = await client.post(f"{endpoint}/v1/file/write", json={
            "file": "/home/tiger/hello.txt",
            "content": "Hello from veFaaS Sandbox!\nLine 2\n",
        })
        print(f"Write result: {r.json()['data']}")

        print("\n--- Append content ---")
        r = await client.post(f"{endpoint}/v1/file/write", json={
            "file": "/home/tiger/hello.txt",
            "content": "Appended line 3\n",
            "append": True,
        })
        print(f"Append result: {r.json()['data']}")

        print("\n--- Read file ---")
        r = await client.post(f"{endpoint}/v1/file/read", json={
            "file": "/home/tiger/hello.txt",
        })
        print(f"Content:\n{r.json()['data']['content']}")

        print("--- Read lines 1-2 ---")
        r = await client.post(f"{endpoint}/v1/file/read", json={
            "file": "/home/tiger/hello.txt",
            "start_line": 1, "end_line": 2,
        })
        print(f"Content:\n{r.json()['data']['content']}")

        print("--- List /home/tiger ---")
        r = await client.post(f"{endpoint}/v1/file/list", json={
            "path": "/home/tiger", "max_depth": 2,
        })
        files = r.json()["data"]["files"]
        for f in files[:10]:
            if f["is_directory"]:
                print(f"  dir  {f['name']}/")
            else:
                print(f"  file {f['name']} ({f['size']} bytes)")

    print(f"\nDestroying sandbox: {sandbox_id}")
    await asyncio.to_thread(
        api.kill_sandbox,
        KillSandboxRequest(function_id=function_id, sandbox_id=sandbox_id),
    )
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
