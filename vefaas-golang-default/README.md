# Golang Function Template

This repository provides a Golang function template that can be directly deployed to veFaaS.

## Runtime Environment
- veFaaS (Linux/Debian, Golang environment)
- The platform runs the main binary (refer to build.sh for how to generate an executable file for Linux systems)

## Deploy to veFaaS
- Generate deployment package: Run `./build_and_zip.sh`
- Upload the deployment package to the veFaaS console
- Deploy the function and check the logs to confirm successful startup
