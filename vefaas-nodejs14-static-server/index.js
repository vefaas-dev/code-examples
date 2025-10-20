// Copyright (c) 2024 Bytedance Ltd. and/or its affiliates
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

const path = require("path");
const fs = require("fs/promises");
const mime = require("mime-types");
const conf = require("./conf.json");

const root = conf.root || "./static";
const index = conf.index || "index.html";
const notfound = conf.notfound || "404.html";
const maxage = conf.maxage || 0;

const toBool = [() => true, () => false];
const isExists = async (path) => await fs.access(path).then(...toBool);

const getFullPath = (pathname) => {
  const paths = [process.cwd(), root, pathname];
  if (!mime.lookup(pathname)) paths.push(index);
  return path.join(...paths);
};

const render404 = async () => {
  const page404 = path.join(process.cwd(), root, notfound);
  const data = await fs.readFile(page404);
  return {
    statusCode: 200,
    headers: { "content-type": "text/html;" },
    body: data,
  };
};

const renderError = (err) => ({
  statusCode: 500,
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ code: 500, message: err }),
});

const useStatic = async (event) => {
  try {
    const fullPath = getFullPath(event.path);
    const exist = await isExists(fullPath);
    const contentType = mime.lookup(path.extname(fullPath));

    if (exist && contentType) {
      const data = await fs.readFile(fullPath);
      return {
        statusCode: 200,
        headers: {
          "content-type": contentType,
          "cache-control": ["public", `max-age=${maxage}`].join(","),
        },
        body: data,
      };
    }
    return await render404();
  } catch (err) {
    console.error(err);
    return renderError(err);
  }
};

exports.handler = async (event, context) => {
  console.log(`received new request, request id: %s`, context.requestId);

  return await useStatic(event);
};
