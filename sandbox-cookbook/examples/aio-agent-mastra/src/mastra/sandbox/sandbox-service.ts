import { Service } from '@volcengine/openapi';

export class SandboxService {
  private static instance: SandboxService | null = null;

  private sandboxId: string | undefined = process.env.SANDBOX_INSTANCE_NAME;
  private createPromise: Promise<void> | null = null;
  private readonly functionId = process.env.SANDBOX_APP_ID;
  private readonly baseUrl = (process.env.SANDBOX_ENDPOINT || '').replace(/\/+$/, '');

  private constructor() {}

  static getInstance(): SandboxService {
    if (!SandboxService.instance) {
      SandboxService.instance = new SandboxService();
    }
    return SandboxService.instance;
  }

  private headers(): Record<string, string> {
    const h: Record<string, string> = { 'Content-Type': 'application/json' };
    if (this.sandboxId) h['x-faas-instance-name'] = this.sandboxId;
    return h;
  }

  private getVolcService() {
    const svc = new Service({
      serviceName: 'vefaas',
      defaultVersion: '2024-06-06',
      host: 'open.volcengineapi.com',
      region: process.env.VEFAAS_REGION || 'cn-beijing',
    });
    (svc as any).setAccessKeyId(process.env.VOLC_ACCESS_KEY);
    (svc as any).setSecretKey(process.env.VOLC_SECRET_KEY);
    return svc;
  }

  private async create(): Promise<void> {
    if (!this.functionId) throw new Error('SANDBOX_APP_ID is not set');
    const svc = this.getVolcService();
    const resp = await (svc as any).fetchOpenAPI({
      Action: 'CreateSandbox',
      Version: '2024-06-06',
      method: 'POST',
      params: {},
      headers: { 'Content-Type': 'application/json' },
      data: { FunctionId: this.functionId, CpuMilli: 2000, MemoryMB: 4096, Timeout: 1800, TimeoutUnit: 'second' },
    });
    const id = resp.Result?.SandboxId as string | undefined;
    if (!id) throw new Error('Failed to create sandbox: no SandboxId returned');
    this.sandboxId = id;
  }

  private async ensureReady(): Promise<void> {
    if (this.sandboxId) return;
    if (this.createPromise) return this.createPromise;
    this.createPromise = this.create().finally(() => { this.createPromise = null; });
    return this.createPromise;
  }

  async get(path: string): Promise<any> {
    await this.ensureReady();
    const res = await fetch(`${this.baseUrl}${path}`, { headers: this.headers() });
    if (!res.ok) throw new Error(`API error: ${res.status} ${await res.text()}`);
    return res.json();
  }

  async post(path: string, body: unknown): Promise<any> {
    await this.ensureReady();
    const res = await fetch(`${this.baseUrl}${path}`, {
      method: 'POST',
      headers: this.headers(),
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`API error: ${res.status} ${await res.text()}`);
    return res.json();
  }
}
