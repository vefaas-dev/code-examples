# Next.js Chatbot 项目

这是一个基于 Next.js 的聊天机器人应用模板，使用 App Router，支持服务端渲染（SSR）和独立可部署（standalone）构建，适配原生 Node.js 20 运行时的函数服务部署场景。

## 项目结构

项目结构示意：

```
├── src/                      # 应用源码根目录
│   ├── app/                  # App Router 页面与路由
│   ├── components/           # 复用的 UI 组件
│   ├── lib/                  # 工具方法与通用逻辑
│   └── middleware.ts         # 中间件
├── public/                   # 静态资源目录（图片、图标等）
├── next.config.ts            # Next.js 配置（output: 'standalone', runtime: 'nodejs'）
├── build.sh                  # 构建脚本（生成 .next/standalone）
├── run.sh                    # 启动脚本（node .next/standalone/server.js）
├── package.json              # 项目配置与 npm 脚本
├── tsconfig.json             # TypeScript 配置
├── eslint.config.mjs         # ESLint 配置
├── postcss.config.mjs        # PostCSS 配置
├── components.json           # 组件/样式相关配置（如 UI 体系）
└── README.md                 # 项目说明
```

### 目录说明
- **src/app/** - 使用 Next.js App Router 构建页面与路由
- **src/components/** - 通用 UI 组件
- **src/lib/** - 工具函数与业务逻辑封装
- **src/middleware.ts** - 中间件定义（如鉴权、请求处理）
- **public/** - 静态公共资源
- **next.config.ts** - Next.js 核心配置（output: 'standalone'，runtime: 'nodejs'）
- **.next/standalone/** - 构建后的独立运行产物（由 build.sh 生成）
- **run.sh** - 运行入口脚本，执行 node .next/standalone/server.js
- **package.json** - 依赖与脚本管理

## 开发、构建和部署

### 1. 开发阶段

正常开发流程：
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 2. 构建阶段

开发完成后，构建生产版本：
```bash
# 运行构建脚本编译应用
./build.sh
```

### 3. 本地测试

构建完成后，本地测试：
```bash
./run.sh
```

### 4. 部署到函数服务

直接将这个代码包上传到 FaaS 平台即可

查看 [Next.js 部署文档](https://nextjs.org/docs/app/building-your-application/deploying) 了解更多详情。