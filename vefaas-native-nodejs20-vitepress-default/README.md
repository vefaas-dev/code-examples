# VitePress 文档站点

这是一个基于 VitePress 的文档站点模板，用于快速构建现代化的静态文档网站。

## 开发、构建和部署

### 1. 开发阶段

正常开发流程：
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run docs:dev
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

### 4. 部署到 FaaS

直接将这个代码包上传到 FaaS 平台即可

## 文档编写

文档使用 Markdown 编写，支持以下特性：

- 标准 Markdown 语法
- Vue 组件嵌入
- 代码高亮
- 自定义容器
- 数学公式

更多文档编写指南请参考 [VitePress 官方文档](https://vitepress.dev/)。