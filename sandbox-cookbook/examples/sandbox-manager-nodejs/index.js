/**
 * Sandbox Manager - Lifecycle Management Example (Node.js)
 *
 * Create, describe, list, extend timeout, and destroy sandboxes
 */

require('dotenv').config();
const { Service } = require('@volcengine/openapi');

async function main() {
    const functionId = process.env.SANDBOX_APP_ID;

    const service = new Service({
        serviceName: 'vefaas',
        defaultVersion: '2024-06-06',
        host: 'open.volcengineapi.com',
        region: process.env.VEFAAS_REGION || 'cn-beijing'
    });
    service.setAccessKeyId(process.env.VOLC_ACCESS_KEY);
    service.setSecretKey(process.env.VOLC_SECRET_KEY);

    // Helper for management API calls
    const callAPI = (action, data) =>
        service.fetchOpenAPI({
            Action: action,
            Version: '2024-06-06',
            method: 'POST',
            params: {},
            data,
            headers: { 'Content-Type': 'application/json' }
        });

    console.log('=== Create sandbox ===');
    const createResp = await callAPI('CreateSandbox', {
        FunctionId: functionId,
        CpuMilli: 500,
        MemoryMB: 1024,
        Timeout: 1800,
        TimeoutUnit: 'second'
    });
    const sandboxId = createResp.Result?.SandboxId;
    console.log(`Created: ${sandboxId}`);

    try {
        console.log('\n=== Describe sandbox ===');
        const descResp = await callAPI('DescribeSandbox', { FunctionId: functionId, SandboxId: sandboxId });
        console.log(JSON.stringify(descResp.Result, null, 2));

        console.log('\n=== List active sandboxes ===');
        const listResp = await callAPI('ListSandboxes', { FunctionId: functionId });
        const sandboxes = listResp.Result.Sandboxes;
        console.log(`Total: ${sandboxes.length} sandbox(es)`);
        sandboxes.slice(0, 5).forEach(sb => console.log(`  - ${sb.SandboxId} (${sb.Status})`));

        console.log('\n=== Extend timeout ===');
        const extResp = await callAPI('SetSandboxTimeout', {
            FunctionId: functionId,
            SandboxId: sandboxId,
            Timeout: 60
        });
        console.log('Result:', extResp.Result);
    } finally {
        console.log(`\n=== Destroy sandbox: ${sandboxId} ===`);
        await callAPI('KillSandbox', { FunctionId: functionId, SandboxId: sandboxId });
        console.log('Sandbox destroyed.');
    }
}

main().catch(console.error);
