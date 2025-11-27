# Next.js Project

This is a modern React application template based on Next.js, supporting Server-Side Rendering and Static Generation.

## Project Structure

Project structure:

```
├── app/           # Next.js application source (App Router)
├── public/        # Static assets directory
└── build/         # Build output directory (for function service deployment)
```

### Directory Description
- **app/** - Next.js application source code, using App Router architecture
- **public/** - Public static assets such as images, icons, etc.
- **build/** - Static build output for function service hosting

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

After the build is complete, test locally:
```bash
./run.sh
```

### 4. Deploy to Function Service

Simply upload this code package to the FaaS platform
