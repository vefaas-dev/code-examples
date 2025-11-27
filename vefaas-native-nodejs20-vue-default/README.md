# Vue 3 + TypeScript + Vite

This template helps you get started quickly with Vue 3 and TypeScript in Vite. The template uses Vue 3's `<script setup>` Single File Components. Check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

For more information on recommended project setup and IDE support, refer to the [Vue Docs TypeScript Guide](https://vuejs.org/guide/typescript/overview.html#project-setup).

## Project Structure

The project uses a simple structure:

```
├── src/           # Vue source code directory
├── public/        # Static assets directory
└── server/        # Function hosting service (uses serve-handler to host built static assets)
```

### Directory Description
- **src/** - Vue application source code, including components, styles, etc.
- **public/** - Public static assets such as images, icons, etc.
- **server/** - Function service entry point, uses serve-handler to host built files

# Deploy to Function Service

## Development, Build, and Deployment

### 1. Development Phase

Normal development workflow:
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### 2. Build Phase

After development is complete, build the production version:
```bash
# Run build script to compile the application
./build.sh
```

### 3. Local Testing

After the build is complete, test locally by running run.sh:
```bash
./run.sh
```

### 4. Deploy to FaaS

Simply upload this code package to the FaaS platform
