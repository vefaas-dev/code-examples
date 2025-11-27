# React + TypeScript + Vite

这个模板提供了在 Vite 中使用 React 的最小化配置，支持热模块替换（HMR）和一些 ESLint 规则。

目前有两个官方插件可用：

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) 使用 [Babel](https://babeljs.io/) 实现快速刷新
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) 使用 [SWC](https://swc.rs/) 实现快速刷新

## 项目结构

项目采用简洁的结构：

```
├── src/           # React 源代码目录
├── public/        # 静态资源目录
└── server/        # 函数托管服务（使用 serve-handler 托管构建后的静态资源）
```

### 目录说明
- **src/** - React 应用源码，包含组件、样式等
- **public/** - 公共静态资源，如图片、图标等
- **server/** - 函数服务入口，使用 serve-handler 托管构建后的文件

## 扩展 ESLint 配置

如果你正在开发生产级应用，建议更新配置以启用类型感知的 lint 规则。

# 部署到函数服务

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

构建完成后，本地可通过执行 run.sh 测试：
```bash
./run.sh
```

### 4. 部署到 FaaS

直接将这个代码包上传到 FaaS 平台即可

