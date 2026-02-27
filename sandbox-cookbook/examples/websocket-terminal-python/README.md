# WebSocket Terminal (Python)

Interactive shell terminal via WebSocket connection to a sandbox.

## What It Does

- Connects to the sandbox shell via WebSocket at `/v1/shell/ws`
- Uses JSON message protocol for input/output
- Sends commands and receives real-time terminal output
- Handles `ping/pong` heartbeat to keep the connection alive

```python
ws_url = endpoint.replace("https://", "wss://").replace("http://", "ws://") + "/v1/shell/ws"
async with websockets.connect(ws_url, additional_headers={"x-faas-instance-name": sandbox_id}) as ws:
    # Send a command
    await ws.send(json.dumps({"type": "input", "data": "echo Hello\n"}))

    # Receive output
    msg = json.loads(await ws.recv())
    if msg["type"] == "output":
        print(msg["data"])
    elif msg["type"] == "ping":
        await ws.send(json.dumps({"type": "pong", "timestamp": msg["data"]}))
```

## Setup & Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a Sandbox application

If you don't have one yet, [create a Code Sandbox application](https://console.volcengine.com/vefaas/region:vefaas+cn-beijing/sandbox/create?imageGroup=Code&quickStart=true) in the veFaaS console, and note the **Function ID** and **Endpoint**.

> 📖 See the full [Prerequisites](../../README.md#2-prerequisites) guide for details.

### 3. Configure environment

```bash
cp .env.template .env
```

### 4. Run

```bash
python main.py
```

## Reference

- [Sandbox API Documentation](https://www.volcengine.com/docs/6662/1806654)
- [Shell Terminal Guide](https://sandbox.agent-infra.com/guide/basic/shell)
