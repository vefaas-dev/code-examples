# Node.js 14 Function Template

This repository provides a Node.js function template that can be directly deployed to veFaaS.

## Runtime Environment
- veFaaS (Linux/Debian, Node.js 14 environment)
- Expose handler through `exports.handler(event, context)` as the platform's entry point

## Deploy to veFaaS (Platform Dependency Installation)
- Ensure `package.json` includes the required dependencies
- Generate deployment package: Run `./zip.sh`
- Upload the deployment package to the veFaaS console
- In the console, if dependencies are used, click "Install Dependencies". The platform will install the dependencies in the Node.js 14 environment to the runtime directory
- Deploy the function and check the logs to confirm successful startup
