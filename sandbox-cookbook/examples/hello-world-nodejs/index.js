/**
 * veFaaS Sandbox Quick Start - Node.js
 *
 * Minimal flow: Create sandbox -> Execute code -> Get result -> Destroy sandbox
 */

require('dotenv').config();
const { Service } = require('@volcengine/openapi');

async function main() {
    const functionId = process.env.SANDBOX_APP_ID;
    const endpoint = (process.env.SANDBOX_ENDPOINT || '').replace(/\/+$/, '');

    // Initialize management client
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
        data: {
            FunctionId: functionId,
            CpuMilli: 500,
            MemoryMB: 1024,
            Timeout: 1800,
            TimeoutUnit: 'second'
        }
    });
    const sandboxId = createResp.Result?.SandboxId;
    console.log(`Sandbox created: ${sandboxId}`);

    console.log('Executing Python code...');
    const execResp = await fetch(`${endpoint}/v1/code/execute`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-faas-instance-name': sandboxId
        },
        body: JSON.stringify({
            language: 'python',
            code: "print('Hello from veFaaS Sandbox!')\nresult = sum(range(100))\nprint(f'1+2+...+99 = {result}')",
            timeout: 10
        })
    });
    const execData = (await execResp.json()).data;
    console.log(`stdout: ${execData.stdout.trim()}`);

    console.log(`Destroying sandbox: ${sandboxId}`);
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
