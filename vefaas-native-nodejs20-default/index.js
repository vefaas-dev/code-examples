// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
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

const express = require("express");
const process = require("process");
const fs = require("fs");
const path = require("path");

const content = fs.readFileSync("./static/index.html").toString();

const port = process.env._FAAS_RUNTIME_PORT || 8000;

const app = express();

app.use(express.static(path.resolve(__dirname, "./static")));

app.get("/v1/ping", (req, res) => {
  res.send("ok");
});

app.get("*", (req, res) => {
  res.header("Content-Type", "text/html;charset=utf-8");

  res.send(content);
});

app
  .listen(port, "0.0.0.0", () => {
    console.log("start success.");
  })
  .on("error", (e) => {
    console.error(e.code, e.message);
  });
