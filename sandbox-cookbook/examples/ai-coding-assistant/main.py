"""
AI Coding Assistant - Generate and execute code with LLM + Sandbox

Flow: Define a task -> LLM generates Python code -> Sandbox executes -> Show result
"""

import asyncio
import os

import volcenginesdkcore
from volcenginesdkcore.api_client import ApiClient
from volcenginesdkvefaas import VEFAASApi, CreateSandboxRequest, KillSandboxRequest
import httpx
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a Python programming assistant. The user will describe a task, and you output executable Python code.
Requirements:
- Output only pure Python code, no markdown formatting
- The code must print its results
- No explanations, just code"""

config = volcenginesdkcore.Configuration()
config.ak = os.getenv("VOLC_ACCESS_KEY")
config.sk = os.getenv("VOLC_SECRET_KEY")
config.region = os.getenv("VEFAAS_REGION", "cn-beijing")
api = VEFAASApi(ApiClient(config))

function_id = os.getenv("SANDBOX_APP_ID")
endpoint = os.getenv("SANDBOX_ENDPOINT", "").rstrip("/")

llm = AsyncOpenAI(
    api_key=os.getenv("ARK_API_KEY", ""),
    base_url=os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
)
model = os.getenv("ARK_MODEL", "doubao-seed-2-0-pro-260215")


async def main():
    task = "Calculate the sum of 1+2+3+...+50 and print the result"

    print("Creating sandbox...")
    resp = await asyncio.to_thread(
        api.create_sandbox,
        CreateSandboxRequest(
            function_id=function_id,
            cpu_milli=1000, memory_mb=2048,
            timeout=1800, timeout_unit="second",
        ),
    )
    sandbox_id = resp.sandbox_id
    print(f"Sandbox created: {sandbox_id}\n")

    print(f"Task: {task}")
    print("Generating code...")
    completion = await llm.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task},
        ],
    )
    code = completion.choices[0].message.content.strip()
    code = code.removeprefix("```python").removeprefix("```").removesuffix("```").strip()
    print(f"\n--- Generated code ---\n{code}\n")

    print("Executing in sandbox...")
    async with httpx.AsyncClient(
        headers={"x-faas-instance-name": sandbox_id}, timeout=60.0
    ) as client:
        r = await client.post(f"{endpoint}/v1/code/execute", json={
            "language": "python", "code": code, "timeout": 30,
        })
    data = r.json()["data"]
    if data["stdout"]:
        print(f"Output:\n{data['stdout']}")
    if data.get("stderr"):
        print(f"stderr:\n{data['stderr']}")

    print(f"Destroying sandbox: {sandbox_id}")
    await asyncio.to_thread(
        api.kill_sandbox,
        KillSandboxRequest(function_id=function_id, sandbox_id=sandbox_id),
    )
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
