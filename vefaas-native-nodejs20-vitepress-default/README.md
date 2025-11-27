# VitePress Documentation Site

This is a VitePress-based documentation site template for quickly building modern static documentation websites.

## Development, Build, and Deployment

### 1. Development Phase

Normal development workflow:
```bash
# Install dependencies
npm install

# Start development server
npm run docs:dev
```

### 2. Build Phase

After development is complete, build the production version:
```bash
# Run build script to compile the application
./build.sh
```

### 3. Local Testing

After the build is complete, test locally:
```bash
./run.sh
```

### 4. Deploy to FaaS

Simply upload this code package to the FaaS platform

## Writing Documentation

Documentation is written in Markdown and supports the following features:

- Standard Markdown syntax
- Vue component embedding
- Code highlighting
- Custom containers
- Mathematical formulas

For more documentation writing guides, refer to the [VitePress Official Documentation](https://vitepress.dev/).
