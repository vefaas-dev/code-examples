### 使用方式
将静态资源文件放到 `static` 目录下，发布函数即可

### 配置
如果需要调整配置，可以修复 `conf.json` 配置

```javascript
{
  "root": "./static", // static server 根目录
  "index": "index.html", // 默认的 HTML 文件
  "notfound": "404.html", // 404 HTML 文件
  "maxage": 604800 // 过期时间，默认为 0
}
```