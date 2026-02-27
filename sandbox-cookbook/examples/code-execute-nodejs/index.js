/**
 * Code Sandbox - Code Execution Example (Node.js)
 *
 * Execute Python / Node.js / Shell code in a sandbox
 */

require('dotenv').config();
const { Service } = require('@volcengine/openapi');

async function main() {
    const functionId = process.env.SANDBOX_APP_ID;
    const endpoint = (process.env.SANDBOX_ENDPOINT || '').replace(/\/+$/, '');

    const service = new Service({
        serviceName: 'vefaas',
        defaultVersion: '2024-06-06',
        host: 'open.volcengineapi.com',
        region: process.env.VEFAAS_REGION || 'cn-beijing'
    });
    service.setAccessKeyId(process.env.VOLC_ACCESS_KEY);
    service.setSecretKey(process.env.VOLC_SECRET_KEY);

    console.log('Creating sandbox...');
    const createResp = await service.fetchOpenAPI({
        Action: 'CreateSandbox',
        Version: '2024-06-06',
        method: 'POST',
        params: {},
        headers: { 'Content-Type': 'application/json' },
        data: { FunctionId: functionId, CpuMilli: 500, MemoryMB: 1024, Timeout: 1800, TimeoutUnit: 'second' }
    });
    const sandboxId = createResp.Result?.SandboxId;
    console.log(`Sandbox created: ${sandboxId}`);

    const headers = { 'Content-Type': 'application/json', 'x-faas-instance-name': sandboxId };

    console.log('\n--- Python ---');
    let r = await fetch(`${endpoint}/v1/code/execute`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
            language: 'python',
            code: "import json, platform\nprint(json.dumps({'python': platform.python_version()}, indent=2))",
            timeout: 10
        })
    });
    console.log((await r.json()).data.stdout);

    console.log('--- Node.js ---');
    r = await fetch(`${endpoint}/v1/code/execute`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
            language: 'javascript',
            code: 'console.log(JSON.stringify({ node: process.version, pid: process.pid }, null, 2))',
            timeout: 10
        })
    });
    console.log((await r.json()).data.stdout);

    console.log('--- Shell ---');
    r = await fetch(`${endpoint}/v1/shell/exec`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ command: 'uname -a && whoami && pwd', timeout: 10 })
    });
    console.log((await r.json()).data.output);

    console.log(`\nDestroying sandbox: ${sandboxId}`);
    await service.fetchOpenAPI({
        Action: 'KillSandbox',
        Version: '2024-06-06',
        method: 'POST',
        params: {},
        headers: { 'Content-Type': 'application/json' },
        data: { FunctionId: functionId, SandboxId: sandboxId }
    });
    console.log('Done.');
}

main().catch(console.error);
