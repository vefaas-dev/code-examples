# AI Coding Assistant

Use LLM to generate code and execute it in a sandbox.

## What It Does

- Sends a task description to LLM (Doubao via Volcengine Ark)
- LLM generates Python code
- Code is executed in a sandbox via `/v1/code/execute`
- Execution result is printed

```python
task = "Calculate the sum of 1+2+3+...+50 and print the result"

completion = await llm.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task},
    ],
)
code = completion.choices[0].message.content.strip()

result = await client.post(f"{endpoint}/v1/code/execute", json={
    "language": "python", "code": code,
})
print(result.json()["data"]["stdout"])
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

Requires sandbox credentials and `ARK_API_KEY`. Optionally set `ARK_BASE_URL` and `ARK_MODEL` (defaults to `doubao-seed-2-0-pro-260215`).

### 4. Run

```bash
python main.py
```

## Reference

- [Sandbox API Documentation](https://www.volcengine.com/docs/6662/1806654)
