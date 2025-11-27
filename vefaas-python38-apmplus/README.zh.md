# veFaaS Python 3.8 APMPlus Sample

## 1. Install Dependencies

- Install dependencies of apmplus_server_sdk_python by veFaaS

- install apmplus_server_sdk_python itself

> Python 3.8 is needed.

```bash
git clone git@code.byted.org:byteapm/apmplus_server_sdk_python.git -b feat/refactor && \ 
cd apmplus_server_sdk_python && \
python -m pip install . --target ../site-packages && \
cd .. && \
rm -rf apmplus_server_sdk_python
```

- install ark

> 跨平台，可以本地安装好

> Q: 这是一个通用的 amplus sdk 吧？为什么依赖 ark?
> A: 之前是针对 ark 开发的，然后针对 ark 包做了instrumentation,  request_id 这些信息也依赖他们的 context 获取，所以会依赖 ark 包，确实不是很合理，后面我们想下怎么解除这个依赖吧。

Follow [the instruction](https://bytedance.larkoffice.com/wiki/EelBw62BeiXchwkCoc4cIRADndg) to install ark.

```sh
python -m pip install ark-0.1.34-py3-none-any.whl --target site-packages

python -m pip install ark-0.1.34-py3-none-any.whl --target site-packages --index-url https://mirrors.volces.com/pypi/simple/
```
