# Golang TOS Trigger Function Template

This repository provides a Golang TOS trigger function template that can be directly deployed to veFaaS.

## Runtime Environment
- veFaaS (Linux/Debian, Golang environment)
- The platform invokes the function entry point `handler`

## Deploy to veFaaS
- Generate deployment package: Run `./build_and_zip.sh`
- Upload the deployment package to the veFaaS console
- Deploy the function and check the logs to confirm successful startup
