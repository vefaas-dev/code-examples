### Usage
Place static resource files in the `static` directory and deploy the function.

### Configuration
To adjust the configuration, modify the `conf.json` file:

```javascript
{
  "root": "./static",      // Static server root directory
  "index": "index.html",   // Default HTML file
  "notfound": "404.html",  // 404 HTML file
  "maxage": 604800         // Expiration time, default is 0
}
```
