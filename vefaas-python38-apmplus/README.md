# veFaaS Python 3.8 APMPlus Sample

## 1. Install Dependencies

- Install dependencies of apmplus_server_sdk_python by veFaaS

- Install apmplus_server_sdk_python itself

> Python 3.8 is required.

```bash
git clone git@code.byted.org:byteapm/apmplus_server_sdk_python.git -b feat/refactor && \
cd apmplus_server_sdk_python && \
python -m pip install . --target ../site-packages && \
cd .. && \
rm -rf apmplus_server_sdk_python
```

- Install ark

> Cross-platform, can be installed locally

> Q: Is this a general amplus SDK? Why does it depend on ark?
> A: It was originally developed for ark, and instrumentation was done for the ark package. Information like request_id also relies on their context, so it depends on the ark package. This is indeed not very reasonable. We'll figure out how to remove this dependency later.

Follow [the instruction](https://bytedance.larkoffice.com/wiki/EelBw62BeiXchwkCoc4cIRADndg) to install ark.

```sh
python -m pip install ark-0.1.34-py3-none-any.whl --target site-packages

python -m pip install ark-0.1.34-py3-none-any.whl --target site-packages --index-url https://mirrors.volces.com/pypi/simple/
```
