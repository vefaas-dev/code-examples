# Vue 3 + TypeScript + Vite

这个模板可以帮助你快速开始使用 Vue 3 和 TypeScript 在 Vite 中进行开发。该模板使用了 Vue 3 的 `<script setup>` 单文件组件，请查看 [script setup 文档](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) 了解更多信息。

了解更多关于推荐的项目设置和 IDE 支持，请参考 [Vue 文档 TypeScript 指南](https://vuejs.org/guide/typescript/overview.html#project-setup)。

## 项目结构

项目采用简洁的结构：

```
├── src/           # Vue 源代码目录
├── public/        # 静态资源目录
└── server/        # 函数托管服务（使用 serve-handler 托管构建后的静态资源）
```

### 目录说明
- **src/** - Vue 应用源码，包含组件、样式等
- **public/** - 公共静态资源，如图片、图标等
- **server/** - 函数服务入口，使用 serve-handler 托管构建后的文件

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

