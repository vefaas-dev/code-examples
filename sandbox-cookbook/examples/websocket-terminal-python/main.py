"""
WebSocket Terminal Example (Python SDK)

Connect to sandbox shell via WebSocket and execute commands
Protocol: JSON messages over ws://.../v1/shell/ws
  - Send: {"type": "input", "data": "command\n"}
  - Recv: {"type": "output", "data": "..."} / {"type": "session_id", "data": "..."} / {"type": "ping", ...}
"""

import asyncio
import json
import os

import volcenginesdkcore
from volcenginesdkcore.api_client import ApiClient
from volcenginesdkvefaas import VEFAASApi, CreateSandboxRequest, KillSandboxRequest
import websockets
from dotenv import load_dotenv

load_dotenv()

config = volcenginesdkcore.Configuration()
config.ak = os.getenv("VOLC_ACCESS_KEY")
config.sk = os.getenv("VOLC_SECRET_KEY")
config.region = os.getenv("VEFAAS_REGION", "cn-beijing")
api = VEFAASApi(ApiClient(config))

function_id = os.getenv("SANDBOX_APP_ID")
endpoint = os.getenv("SANDBOX_ENDPOINT", "").rstrip("/")
ws_endpoint = endpoint.replace("https://", "wss://").replace("http://", "ws://")


async def main():
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
    print(f"Sandbox created: {sandbox_id}\n")

    async with websockets.connect(
        f"{ws_endpoint}/v1/shell/ws",
        additional_headers={"x-faas-instance-name": sandbox_id},
    ) as ws:

        # Wait for initial prompt
        while True:
            try:
                msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=3))
            except asyncio.TimeoutError:
                break
            if msg["type"] == "output":
                print(msg["data"], end="", flush=True)
            elif msg["type"] == "ping":
                await ws.send(json.dumps({"type": "pong", "timestamp": msg["data"]}))

        # Execute commands
        for cmd in ["echo 'Hello from WebSocket!'", "uname -a", "pwd && ls -la"]:
            print(f"\n$ {cmd}")
            await ws.send(json.dumps({"type": "input", "data": cmd + "\n"}))
            while True:
                try:
                    msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=3))
                except asyncio.TimeoutError:
                    break
                if msg["type"] == "output":
                    print(msg["data"], end="", flush=True)
                elif msg["type"] == "ping":
                    await ws.send(json.dumps({"type": "pong", "timestamp": msg["data"]}))

    print(f"\nDestroying sandbox: {sandbox_id}")
    await asyncio.to_thread(
        api.kill_sandbox,
        KillSandboxRequest(function_id=function_id, sandbox_id=sandbox_id),
    )
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
