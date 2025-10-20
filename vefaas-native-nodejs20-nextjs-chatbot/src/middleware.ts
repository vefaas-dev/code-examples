// Copyright (c) 2024 Bytedance Ltd. and/or its affiliates
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { NextResponse, NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
    const { pathname, searchParams } = request.nextUrl;
    const token = searchParams.get('token');
    const expected = process.env.AUTH_KEY;

    // 对首页与两个接口做校验，放行静态资源和其它路径
    const needCheck =
        pathname === '/' ||
        pathname === '/api/chat' ||
        pathname === '/api/models';

    if (!needCheck) {
        return NextResponse.next();
    }

    // 从 Referer 中尝试获取 token
    const referer = request.headers.get('referer') || '';
    let tokenFromReferer: string | null = null;
    try {
        const refUrl = new URL(referer);
        tokenFromReferer = refUrl.searchParams.get('token');
    } catch {
        tokenFromReferer = null;
    }

    // 首页必须显式携带 token
    if (pathname === '/') {
        if (!token || !expected || token !== expected) {
            return new NextResponse('Unauthorized: token required or invalid', { status: 401 });
        }
        return NextResponse.next();
    }

    // API 接口：优先使用 query 中的 token；若缺失则尝试从 referer 补齐并重写 URL
    const candidate = token || tokenFromReferer;

    if (!candidate || !expected || candidate !== expected) {
        return new NextResponse('Unauthorized: token required or invalid', { status: 401 });
    }

    // 若原始请求未携带 query，则重写为带上 token 的 URL
    if (!token) {
        request.nextUrl.searchParams.set('token', candidate);
        return NextResponse.rewrite(request.nextUrl);
    }

    return NextResponse.next();
}

export const config = {
    matcher: ['/', '/api/:path*'],
};