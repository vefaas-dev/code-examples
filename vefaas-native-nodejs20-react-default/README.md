# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with Hot Module Replacement (HMR) and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Project Structure

The project uses a simple structure:

```
├── src/           # React source code directory
├── public/        # Static assets directory
└── server/        # Function hosting service (uses serve-handler to host built static assets)
```

### Directory Description
- **src/** - React application source code, including components, styles, etc.
- **public/** - Public static assets such as images, icons, etc.
- **server/** - Function service entry point, uses serve-handler to host built files

## Expanding the ESLint Configuration

If you are developing a production application, it's recommended to update the configuration to enable type-aware lint rules.

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
